#!/usr/bin/env python3
"""Public, read-only TLC 4.6 pull-request telemetry evaluator.

This process emits non-credit telemetry. It never checks out, imports, builds,
installs, or executes caller-controlled bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ACTION_ROOT = Path(__file__).resolve().parent
CONTROL_ROOT = ACTION_ROOT.parents[2]
SOURCE_RECEIPT = CONTROL_ROOT / "tlc/public-tlc46-source.json"
API_ORIGIN = "https://api.github.com"
SHA1 = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
MAX_CHANGED_FILES = 3000
PACKAGE_IDENTITY = {
    "version": "0.19.0",
    "reviewed_head": "7397a727d563957ff5701887abd842518b58dc72",
    "source_commit": "146c1899edda6908f5e819061d9f8f0f850c7819",
    "manifest_blob": "50ee9f1c776c8b23dfac88b9239f4e12337e3bf3",
    "provenance_sha256": "09093935509ba2dc8f54151dc1fe2a7da3904b4d5e686ca73e3aaaecb955ae9f",
}
POLICY_IDENTITY = {
    "id": "DF-V4.0-CFAR-CFADA-DEV-ARC-GATE-STANDARD",
    "version": "4.6.0",
    "blob": "b0f89a3caf26d956a8e9c82a84fc8c21c303eb1c",
    "sha256": "e884228242cfac5e8e4f019059962512fa4eb1012044a6a13ecdaecc10e37b89",
}


class PublicAuditError(ValueError):
    """Fail-closed public observation failure."""


def stable_json_bytes(value: Any) -> bytes:
    """Stable telemetry encoding, deliberately not a lifecycle-credit receipt."""

    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def load_object(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise PublicAuditError(f"duplicate_json_key:{key}")
            result[key] = value
        return result

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError, PublicAuditError) as exc:
        raise PublicAuditError(f"invalid_json:{path.name}:{exc}") from exc
    if not isinstance(value, dict):
        raise PublicAuditError(f"json_root_not_object:{path.name}")
    return value


def source_receipt() -> dict[str, Any]:
    value = load_object(SOURCE_RECEIPT)
    expected = {
        "schema_version": "transpara.tlc.public-control-source.v1",
        "source_repository": "transpara-ai/platform",
        "package": PACKAGE_IDENTITY,
        "policy": POLICY_IDENTITY,
        "authority_granted": False,
        "lifecycle_credit": False,
        "status": "candidate_non_credit_public_telemetry",
    }
    for key, wanted in expected.items():
        if value.get(key) != wanted:
            raise PublicAuditError(f"source_receipt_mismatch:{key}")
    return value


class GitHubClient:
    def __init__(self, token: str, *, opener=urllib.request.urlopen):
        if not token:
            raise PublicAuditError("github_token_unavailable")
        self.token = token
        self.opener = opener

    def get(self, repository: str, suffix: str) -> Any:
        url = repository_api_url(repository, suffix)
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "transpara-tlc46-public-audit/1",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with self.opener(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            raise PublicAuditError(f"github_api_http:{suffix}:{exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, UnicodeError, json.JSONDecodeError) as exc:
            raise PublicAuditError(f"github_api_failed:{suffix}:{exc}") from exc


def repository_api_url(repository: str, suffix: str) -> str:
    if REPOSITORY.fullmatch(repository) is None:
        raise PublicAuditError("repository_invalid")
    if (suffix and not suffix.startswith("/")) or ".." in suffix:
        raise PublicAuditError("github_api_path_invalid")
    return f"{API_ORIGIN}/repos/{repository}{suffix}"


def exact_public_subject(
    client: GitHubClient,
    *,
    repository: str,
    repository_id: int,
    pr_number: int,
    base: str,
    head: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    metadata = client.get(repository, "")
    if not isinstance(metadata, dict):
        raise PublicAuditError("repository_response_invalid")
    if metadata.get("id") != repository_id or metadata.get("full_name") != repository:
        raise PublicAuditError("repository_identity_mismatch")
    if metadata.get("visibility") != "public" or metadata.get("private") is not False:
        raise PublicAuditError("repository_not_public")

    pull = client.get(repository, f"/pulls/{pr_number}")
    if not isinstance(pull, dict):
        raise PublicAuditError("pull_response_invalid")
    observed = {
        "base": ((pull.get("base") or {}).get("sha")),
        "head": ((pull.get("head") or {}).get("sha")),
        "repository": (((pull.get("base") or {}).get("repo") or {}).get("full_name")),
        "number": pull.get("number"),
    }
    expected = {"base": base, "head": head, "repository": repository, "number": pr_number}
    if observed != expected:
        raise PublicAuditError("live_pull_identity_mismatch")
    changed_files = pull.get("changed_files")
    if not isinstance(changed_files, int) or changed_files < 0 or changed_files > MAX_CHANGED_FILES:
        raise PublicAuditError("changed_file_count_out_of_bounds")

    files: list[dict[str, Any]] = []
    page = 1
    while len(files) < changed_files:
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        rows = client.get(repository, f"/pulls/{pr_number}/files?{query}")
        if not isinstance(rows, list):
            raise PublicAuditError("pull_files_response_invalid")
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("filename"), str):
                raise PublicAuditError("pull_file_row_invalid")
            files.append(
                {
                    "filename": row["filename"],
                    "status": row.get("status"),
                    "additions": row.get("additions"),
                    "deletions": row.get("deletions"),
                    "changes": row.get("changes"),
                    "sha": row.get("sha"),
                }
            )
        if not rows:
            break
        page += 1
        if page > 30:
            break
    if len(files) != changed_files:
        raise PublicAuditError("pull_files_incomplete")
    if len({row["filename"] for row in files}) != len(files):
        raise PublicAuditError("pull_files_duplicate_path")
    return pull, sorted(files, key=lambda row: row["filename"])


def evaluate(
    client: GitHubClient,
    *,
    repository: str,
    repository_id: int,
    pr_number: int,
    base: str,
    head: str,
    observed_at: str,
    environment: dict[str, str],
) -> dict[str, Any]:
    if SHA1.fullmatch(base) is None or SHA1.fullmatch(head) is None:
        raise PublicAuditError("noncanonical_commit")
    if repository_id <= 0 or pr_number <= 0:
        raise PublicAuditError("subject_number_invalid")
    source = source_receipt()
    pull, files = exact_public_subject(
        client,
        repository=repository,
        repository_id=repository_id,
        pr_number=pr_number,
        base=base,
        head=head,
    )
    file_manifest = {row["filename"]: row for row in files}
    return {
        "schema_version": "transpara.tlc.public-audit-telemetry.v1",
        "event_type": "public_audit",
        "subject": {
            "repository_id": repository_id,
            "repository": repository,
            "pull_request": pr_number,
            "base_commit": base,
            "head_commit": head,
            "draft": bool(pull.get("draft")),
        },
        "policy": source["policy"],
        "package": source["package"],
        "observation": {
            "changed_file_count": len(files),
            "changed_file_manifest_sha256": hashlib.sha256(stable_json_bytes(file_manifest)).hexdigest(),
            "api_origin": API_ORIGIN,
            "caller_bytes_executed": False,
            "caller_checkout_performed": False,
        },
        "runner": {
            "repository": environment.get("GITHUB_ACTION_REPOSITORY"),
            "ref": environment.get("GITHUB_ACTION_REF"),
            "workflow_ref": environment.get("GITHUB_WORKFLOW_REF"),
            "run_id": environment.get("GITHUB_RUN_ID"),
            "run_attempt": environment.get("GITHUB_RUN_ATTEMPT"),
        },
        "observed_at": observed_at,
        "authority_granted": False,
        "lifecycle_credit": False,
        "signed_receipt": False,
        "non_authorizations": [
            "no lifecycle gate credit",
            "no status, comment, issue, branch, settings, or repository mutation",
            "no package activation or repository enforcement",
            "no secret, OIDC, attestation, runtime, deployment, EventGraph, Hive, or protected action",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--repository-id", required=True, type=int)
    parser.add_argument("--pr-number", required=True, type=int)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--observed-at")
    args = parser.parse_args()
    observed_at = args.observed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    result = evaluate(
        GitHubClient(os.environ.get("GITHUB_TOKEN", "")),
        repository=args.repository,
        repository_id=args.repository_id,
        pr_number=args.pr_number,
        base=args.base,
        head=args.head,
        observed_at=observed_at,
        environment=dict(os.environ),
    )
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "public-audit-telemetry.json"
    path.write_bytes(stable_json_bytes(result))
    if summary_path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with Path(summary_path).open("a", encoding="utf-8") as handle:
            handle.write("## TLC 4.6 public audit telemetry\n\n")
            handle.write(f"Observed `{args.repository}#{args.pr_number}` at `{args.head}`.\n\n")
            handle.write("This job is audit telemetry only and grants no lifecycle credit.\n")
    print(stable_json_bytes(result).decode(), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PublicAuditError as exc:
        raise SystemExit(f"TLC 4.6 public audit failed closed: {exc}") from exc
