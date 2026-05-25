# Dataset Requirements

Each dataset entry under `datasets/<dataset_name>/` describes one standardized
trajectory-learning task dataset.

## Naming

- Use lowercase snake case.
- The directory name must match `metadata.json` field `dataset_name`.
- Prefer names that include the benchmark task semantics, such as
  `ligand_unbinding_future_500`.

## Required Files

- `dataset_card.md`: human-readable scientific and benchmark documentation.
- `metadata.json`: machine-readable registry metadata.
- `manifest.json`: package internals and array/path layout.
- `download.yaml`: external download locations.
- `checksums.json`: SHA-256 hashes and optional byte sizes.

## Optional Files

- `citation.bib`
- `label_statistics.json`
- `baseline_metrics.json`
- `preview.png`

## Dataset Card Requirements

The card should explain:

- scientific system description
- MD engine and source data provenance
- topology and trajectory sources
- label definitions and generation method
- benchmark task
- split policy
- intended ML use
- limitations
- citations
- license

Include wording equivalent to:

> Labels are rule-based operational labels generated from predefined event
> definitions and should not be interpreted as universal biological truth
> without reviewing the event configuration.

## Metadata Requirements

`metadata.json` must include:

- `dataset_name`
- `version`
- `task`
- `system`
- `storage_profile`
- `coordinate_storage`
- `splits`
- `statistics`
- `license`

Core fields are validated strictly. Use `extensions` for additional
domain-specific metadata.

## Checksums

All hashes must be SHA-256 hex digests. Downloadable package assets in
`download.yaml` should have corresponding checksum entries in `checksums.json`
when practical.

## Licenses And Citations

Entries must identify the dataset license and cite upstream simulations,
software, papers, or data sources needed for scientific provenance.
