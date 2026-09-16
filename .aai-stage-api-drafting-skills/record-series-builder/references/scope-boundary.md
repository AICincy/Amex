# Scope Boundary

This package organizes document packets into matched volumes. It does not
implement the AAI profile's typed evidence objects.

| Profile object | This package |
| --- | --- |
| Source file | Yes: inventory path, hash, flags |
| Independently identifiable record | No. Do not treat one file as one record. |
| Occurrence | No. Duplicate-content flags same bytes, not distinct occurrences. |
| Attachment / multipart | No |
| Record reference vs production | No |
| Locator grammar | No |
| Review-state transitions | No; AAI owns status labels |

If the user asks for record-level identity, occurrence preservation, or
attachment graphs, say this skill cannot produce that state. Inventory the
files. Keep coverage PARTIAL. Do not deduplicate away a second occurrence
just because hashes match.

Dedup flags are residue warnings. They are not authority to drop a copy.
