#!/usr/bin/env python3
"""Verify the candidate TLC 4.6 public release without network or GitHub writes."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tlc/public-tlc46-release-manifest.json"
WORKFLOW = ROOT / ".github/workflows/tlc-4.6-public-reusable.yml"
ACTION = ROOT / ".github/actions/tlc-4.6-public/action.yml"
RUNNER = ROOT / ".github/actions/tlc-4.6-public/run.py"
SHA1 = re.compile(r"^[0-9a-f]{40}$")
PUBLIC_REUSABLE = re.compile(
    r"^transpara-ai/workflows/\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml@([0-9a-f]{40})$"
)


class VerificationError(ValueError):
    """Candidate release validation failure."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise VerificationError(f"duplicate_json_key:{key}")
            result[key] = value
        return result

    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError, VerificationError) as exc:
        raise VerificationError(f"invalid_json:{path.name}:{exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"json_root_not_object:{path.name}")
    return value


def reusable_ref_reasons(value: str, *, jobs_started: int | None = None) -> list[str]:
    reasons: list[str] = []
    match = PUBLIC_REUSABLE.fullmatch(value)
    if match is None:
        reasons.append("public_reusable_ref_invalid")
    elif match.group(1) == "0" * 40:
        reasons.append("public_reusable_commit_missing")
    if value.startswith("transpara-ai/.github/"):
        reasons.append("private_control_plane_target")
    if jobs_started is not None and jobs_started < 1:
        reasons.append("public_workflow_zero_jobs")
    return sorted(set(reasons))


def changed_paths(base: str) -> list[str]:
    if SHA1.fullmatch(base) is None:
        raise VerificationError("review_base_invalid")
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode:
        raise VerificationError(f"review_base_unavailable:{proc.stderr.strip()}")
    return sorted(line for line in proc.stdout.splitlines() if line)


def verify() -> None:
    manifest = load_object(MANIFEST)
    if manifest.get("schema_version") != "transpara.tlc.public-release-manifest.v1":
        raise VerificationError("release_manifest_schema_invalid")
    if manifest.get("status") != "candidate_unpublished" or manifest.get("authority_granted") is not False:
        raise VerificationError("candidate_boundary_invalid")

    reviewed = manifest.get("reviewed_files")
    if not isinstance(reviewed, dict):
        raise VerificationError("reviewed_files_invalid")
    for relative, expected in reviewed.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise VerificationError("reviewed_file_row_invalid")
        path = ROOT / relative
        if not path.is_file() or sha256(path) != expected:
            raise VerificationError(f"reviewed_file_digest_mismatch:{relative}")

    allowlist = manifest.get("reviewed_change_allowlist")
    if not isinstance(allowlist, list) or len(set(allowlist)) != len(allowlist):
        raise VerificationError("reviewed_change_allowlist_invalid")
    if changed_paths(str(manifest.get("review_base"))) != sorted(allowlist):
        raise VerificationError("reviewed_change_allowlist_mismatch")

    action_commit = str(manifest.get("action_commit"))
    if SHA1.fullmatch(action_commit) is None or action_commit == "0" * 40:
        raise VerificationError("action_commit_invalid")
    immutable = manifest.get("immutable_action_paths")
    if not isinstance(immutable, list) or not immutable:
        raise VerificationError("immutable_action_paths_invalid")
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "diff", "--quiet", action_commit, "HEAD", "--", *immutable],
        check=False,
    )
    if proc.returncode:
        raise VerificationError("immutable_action_bytes_changed_after_pin")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    required = (
        "on:\n  workflow_call:",
        "permissions:\n  contents: read\n  pull-requests: read",
        "timeout-minutes: 30",
        "cancel-in-progress: true",
        f"transpara-ai/workflows/.github/actions/tlc-4.6-public@{action_commit}",
        "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
    )
    missing = [value for value in required if value not in workflow]
    if missing:
        raise VerificationError(f"workflow_binding_missing:{missing}")
    forbidden_workflow = (
        "actions/checkout@",
        "pull_request_target:",
        "statuses: write",
        "id-token: write",
        "attestations: write",
        "secrets: inherit",
        "@main",
        "@master",
        "run: ${{",
    )
    present = [value for value in forbidden_workflow if value in workflow]
    if present:
        raise VerificationError(f"unsafe_workflow_construct:{present}")

    source = RUNNER.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(RUNNER))
    forbidden_imports = {"subprocess", "importlib", "socket", "requests", "httpx"}
    imported = {
        name.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for name in (node.names if isinstance(node, ast.Import) else [ast.alias(name=node.module or "")])
    }
    if forbidden_imports & imported:
        raise VerificationError(f"forbidden_runner_import:{sorted(forbidden_imports & imported)}")
    forbidden_source = ("os.system(", "eval(", "exec(", "shell=True", "github.com/", "raw.githubusercontent.com")
    if found := [value for value in forbidden_source if value in source]:
        raise VerificationError(f"forbidden_runner_primitive:{found}")
    action = ACTION.read_text(encoding="utf-8")
    if "secrets." in action or "id-token" in action or "attestations" in action:
        raise VerificationError("public_action_permission_or_secret_reference")

    if manifest.get("network_endpoints") != ["https://api.github.com"]:
        raise VerificationError("network_endpoint_allowlist_invalid")
    if manifest.get("private_evidence_included") is not False:
        raise VerificationError("private_evidence_boundary_invalid")
    if manifest.get("organization_inventory_included") is not False:
        raise VerificationError("organization_inventory_boundary_invalid")

    secret_patterns = (
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
        re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
        re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"),
    )
    for relative in allowlist:
        text = (ROOT / relative).read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in secret_patterns):
            raise VerificationError(f"sensitive_material_detected:{relative}")


def main() -> int:
    verify()
    print("TLC 4.6 public control-plane candidate verification passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        raise SystemExit(f"TLC 4.6 public control-plane verification failed: {exc}") from exc

