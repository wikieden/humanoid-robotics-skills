---
name: robot-episode-schema-migration
description: Migrate historical robot, human or simulated episode records when metadata fields, units or annotation semantics change. Use when older recordings must remain readable without inventing action labels, timestamps or outcomes.
metadata:
  title: Migrating Robot Episode Metadata
---

# Migrating Robot Episode Metadata

Identify the oldest supported writer and a real fixture for each incompatible layout. Trace the normal read path from raw record through version dispatch and normalization to one actual consumer. Keep the source record immutable so normalized data can be regenerated and audited.

1. Make a field mapping by meaning. Record units, clock domain, sample rate, source modality and missing-value convention. A legacy instruction without boundaries can become a segment with unknown start and end. An absent outcome remains unknown. Treat an absent version as a particular legacy layout only when the writer history or a reliable signature establishes that interpretation.
2. Separate the handling of a new optional field in a known version from an unsupported version with unknown semantics. Define whether optional fields are preserved, ignored by the reader, or kept in an extension area. If a normalized writer discards them, keep the original bytes available. On ambiguous units or versions, return a specific unsupported result and retain the affected record.
3. Run mixed-version fixtures through the public reader. Check one legacy record with missing annotations, another with actual zero or false values, one current round trip, and one unsupported version. Check ordered streams, native rates, quality flags and stable episode IDs. Applying normalization to its own output should produce the same semantic record.
4. Check the downstream decision most sensitive to a default. A changed loader mask can silently include unlabeled windows in training even when every JSON record validates. For materialized migrations, record the source identity and converter revision, write to a separate output, and publish complete validated batches. A retry should produce one logical output per source.

**Worked case.** A legacy record says “place the marker” and has no start time. A current record says the same thing with a measured start time of zero. After migration both should yield the instruction. Only the second can supervise the segment start. If a downstream filter counts two timed starts, trace the first stage that converted absence into zero.

**Deliverable.** Return the supported-version matrix, information preserved or lost, fixture outcomes, and a before/after count for the affected consumer. For conversion of the recorded sensor and action streams themselves, use [Episode and Training Dataset Audit](../robot-episode-audit/SKILL.md).
