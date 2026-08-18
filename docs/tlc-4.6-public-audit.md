# TLC 4.6 public audit telemetry

Public repositories cannot call a private reusable workflow. TLC 4.6 therefore
uses a small public evaluator in this public repository.

The evaluator is bound to exact canonical, installed, non-enforcing package
0.19.0 and remains audit telemetry only. It uses GitHub read APIs to resolve the
live repository, pull request, base, head, and changed-file list. It does not
check out, import, build, install, or execute pull-request code. It has no
secret, status write, OIDC, attestation, settings, deployment, or runtime
permission. Its output grants no lifecycle credit.

A public caller must pin the reusable workflow to the full reviewed 40-character
commit that contains the public release. Tags, branches, private workflow
targets, and zero-job runs do not satisfy the public telemetry proof.

```yaml
jobs:
  tlc-4-6-public:
    uses: transpara-ai/workflows/.github/workflows/tlc-4.6-public-reusable.yml@REVIEWED_40_HEX_COMMIT
    with:
      pr_number: ${{ github.event.pull_request.number }}
      base_sha: ${{ github.event.pull_request.base.sha }}
      head_sha: ${{ github.event.pull_request.head.sha }}
```

The example token is a marker, not a mutable ref. Replace it only with the
exact reviewed default-branch commit after this release receives separate
Tier 3 Human approval and merges.
