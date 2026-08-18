#!/usr/bin/env python3
"""Tests for the inert TLC 4.6 public audit control plane."""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = load_module("tlc46_public_runner", ROOT / ".github/actions/tlc-4.6-public/run.py")
verifier = load_module("tlc46_public_verifier", ROOT / "scripts/verify_tlc46_public_control_plane.py")
BASE = "1" * 40
HEAD = "2" * 40


class FakeClient:
    def __init__(self, *, public: bool = True, head_repository: str = "fork-owner/wiki"):
        self.public = public
        self.head_repository = head_repository

    def get(self, repository: str, suffix: str):
        if suffix == "":
            return {
                "id": 77,
                "full_name": repository,
                "visibility": "public" if self.public else "private",
                "private": not self.public,
            }
        if suffix == "/pulls/3":
            return {
                "number": 3,
                "draft": False,
                "changed_files": 2,
                "base": {"sha": BASE, "repo": {"full_name": repository}},
                "head": {"sha": HEAD, "repo": {"full_name": self.head_repository}},
            }
        if suffix.startswith("/pulls/3/files?"):
            return [
                {"filename": "README.md", "status": "modified", "additions": 1, "deletions": 0, "changes": 1, "sha": "3" * 40},
                {"filename": "docs/a.md", "status": "added", "additions": 2, "deletions": 0, "changes": 2, "sha": "4" * 40},
            ]
        raise AssertionError(f"unexpected API suffix {suffix}")


class PublicControlPlaneTests(unittest.TestCase):
    def evaluate(self, client=None):
        return runner.evaluate(
            client or FakeClient(),
            repository="transpara-ai/wiki",
            repository_id=77,
            pr_number=3,
            base=BASE,
            head=HEAD,
            observed_at="2026-08-18T15:00:00Z",
            environment={
                "GITHUB_ACTION_REPOSITORY": "transpara-ai/workflows",
                "GITHUB_ACTION_REF": "666b1a0a2d31d56327c4c0bfde1604c6da1707fb",
                "GITHUB_WORKFLOW_REF": "transpara-ai/wiki/.github/workflows/tlc.yml@refs/pull/3/merge",
                "GITHUB_RUN_ID": "123",
                "GITHUB_RUN_ATTEMPT": "1",
            },
        )

    def test_public_and_forked_pull_request_is_non_credit_telemetry(self):
        result = self.evaluate()
        self.assertEqual(result["subject"]["repository_id"], 77)
        self.assertEqual(result["observation"]["changed_file_count"], 2)
        self.assertFalse(result["observation"]["caller_bytes_executed"])
        self.assertFalse(result["observation"]["caller_checkout_performed"])
        self.assertFalse(result["authority_granted"])
        self.assertFalse(result["lifecycle_credit"])
        self.assertFalse(result["signed_receipt"])
        self.assertEqual(result["package"]["reviewed_head"], "907b1377c2ddf93053d896c99d7899d864f365c2")
        self.assertEqual(
            result["package"]["provenance_sha256"],
            "c91e3a68efd2a62f1029a7aebd868f9554512d12660fdbc4e3acf3e0ca5986d9",
        )
        self.assertTrue(result["package"]["external_canonical"])
        self.assertTrue(result["package"]["installed_non_enforcing"])
        self.assertEqual(runner.stable_json_bytes(result), runner.stable_json_bytes(self.evaluate()))

    def test_repository_metadata_route_is_valid_and_path_escape_is_rejected(self):
        self.assertEqual(
            runner.repository_api_url("transpara-ai/wiki", ""),
            "https://api.github.com/repos/transpara-ai/wiki",
        )
        self.assertEqual(
            runner.repository_api_url("transpara-ai/wiki", "/pulls/3"),
            "https://api.github.com/repos/transpara-ai/wiki/pulls/3",
        )
        with self.assertRaisesRegex(runner.PublicAuditError, "github_api_path_invalid"):
            runner.repository_api_url("transpara-ai/wiki", "pulls/3")
        with self.assertRaisesRegex(runner.PublicAuditError, "github_api_path_invalid"):
            runner.repository_api_url("transpara-ai/wiki", "/../private")

    def test_private_repository_and_live_identity_drift_fail(self):
        with self.assertRaisesRegex(runner.PublicAuditError, "repository_not_public"):
            self.evaluate(FakeClient(public=False))
        with self.assertRaisesRegex(runner.PublicAuditError, "live_pull_identity_mismatch"):
            runner.evaluate(
                FakeClient(),
                repository="transpara-ai/wiki",
                repository_id=77,
                pr_number=3,
                base=BASE,
                head="5" * 40,
                observed_at="2026-08-18T15:00:00Z",
                environment={},
            )

    def test_public_reusable_ref_and_zero_job_fail_closed(self):
        good = "transpara-ai/workflows/.github/workflows/tlc-4.6-public-reusable.yml@" + "a" * 40
        self.assertEqual(verifier.reusable_ref_reasons(good, jobs_started=1), [])
        self.assertIn(
            "private_control_plane_target",
            verifier.reusable_ref_reasons("transpara-ai/.github/.github/workflows/tlc.yml@" + "a" * 40),
        )
        self.assertIn("public_reusable_ref_invalid", verifier.reusable_ref_reasons(good.rsplit("@", 1)[0] + "@main"))
        self.assertIn("public_workflow_zero_jobs", verifier.reusable_ref_reasons(good, jobs_started=0))

    def test_release_manifest_and_disclosure_boundary(self):
        verifier.verify()

    def test_release_manifest_requires_every_allowlisted_nonself_file_digest(self):
        manifest = json.loads((ROOT / "tlc/public-tlc46-release-manifest.json").read_text(encoding="utf-8"))
        manifest["reviewed_files"].pop(".github/actions/tlc-4.6-public/run.py")
        with self.assertRaisesRegex(verifier.VerificationError, "reviewed_file_set_mismatch"):
            verifier.validate_reviewed_file_sets(manifest)

    def test_public_runner_network_endpoint_allowlist_is_exact(self):
        source = (ROOT / ".github/actions/tlc-4.6-public/run.py").read_text(encoding="utf-8")
        self.assertEqual(verifier.runner_network_endpoints(source), ["https://api.github.com"])
        self.assertEqual(
            verifier.runner_network_endpoints(source + '\nEXTRA = "https://example.invalid"\n'),
            ["https://api.github.com", "https://example.invalid"],
        )


if __name__ == "__main__":
    unittest.main()
