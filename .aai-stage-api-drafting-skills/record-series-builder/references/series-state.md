# Series State

AAI owns objective, authorized scope, constraints, takeover, and status
labels. This record is domain state only.

```yaml
packet_root: path
volumes: list of markdown identities
architecture: volume names and section order
handoffs: required on every non-final volume
outputs:
  markdown: required
  docx: only if recipient rules require or permit
  pdf: only if filing or requested
index_path: index.md when two or more volumes exist
inventory_status: CURRENT | STALE-FLAGGED | BLOCKED
invariance: list of source/render checks
residue: flagged paths not approved for delete
coverage: COMPLETE | PARTIAL
missing_capabilities: list of absent sibling skills or tools
```

Rules:

- Inventory before architecture.
- Do not delete residue without authorization.
- Flagged duplicates are not dropped records.
- `coverage: COMPLETE` requires intended outputs only, current index if
  multi-volume, and named invariance results for every rendered legal volume.
- Failed extraction makes the package non-final, not filing-ready.
