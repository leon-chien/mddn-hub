# Contributing To MDDataNet Hub

Thank you for contributing to MDDataNet Hub. This repository accepts metadata
entries for standardized molecular dynamics trajectory-learning task datasets.
It does not accept large trajectory files or generated package archives.

## Contribution Flow

1. Create the dataset package locally with the `mddatanet` CLI.
2. Generate labels, future-event labels, and leakage-aware splits.
3. Validate the local package.
4. Upload large files to an external storage provider.
5. Export Hub metadata from the CLI.
6. Copy the exported metadata folder into `datasets/<dataset_name>/`.
7. Run Hub validation locally.
8. Open a pull request.

Example CLI flow:

```bash
mddatanet convert ...
mddatanet analyze ...
mddatanet split ...
mddatanet validate --hub-ready ...
mddatanet export-manifest --input dataset.mddatanet.zip --out hub_entry/
```

## Required Files

Every dataset entry must include:

- `dataset_card.md`
- `metadata.json`
- `manifest.json`
- `download.yaml`
- `checksums.json`

Optional files include:

- `citation.bib`
- `label_statistics.json`
- `baseline_metrics.json`
- `preview.png`

## Validation

Run:

```bash
python scripts/validate_entry.py datasets/<dataset_name>
python scripts/validate_all.py
```

Pull requests must pass the same validation in CI.

## Large File Policy

Do not commit trajectory archives, Zarr stores, `.mddatanet.zip` packages, or
downloaded datasets. Store large files externally and reference them from
`download.yaml`.

## Label Semantics

Labels must be documented as operational definitions generated from rules,
presets, or explicit analysis configuration. Dataset cards should avoid
presenting these labels as universal biological truth.
