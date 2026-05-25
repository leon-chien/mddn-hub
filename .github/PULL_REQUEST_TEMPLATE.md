# Dataset Submission Checklist

## Dataset Entry

- [ ] This PR adds or updates a dataset entry under `datasets/<dataset_name>/`.
- [ ] Required files are present: `dataset_card.md`, `metadata.json`,
      `manifest.json`, `download.yaml`, and `checksums.json`.
- [ ] Optional files such as `citation.bib`, `label_statistics.json`, and
      `baseline_metrics.json` are included when available.
- [ ] The dataset directory name matches `metadata.json` field `dataset_name`.

## Hub Boundary

- [ ] No large trajectory files, `.mddatanet.zip` packages, Zarr stores, or
      downloaded data artifacts are committed.
- [ ] Large package or coordinate files are hosted externally and referenced in
      `download.yaml`.
- [ ] `checksums.json` contains matching SHA-256 metadata for downloadable
      assets.

## Scientific And Benchmark Metadata

- [ ] The dataset card describes the molecular system, provenance, task,
      labels, split policy, limitations, license, and citations.
- [ ] Labels are described as reproducible operational definitions generated
      from rules, presets, or explicit analysis configuration.
- [ ] The split policy is leakage-aware and belongs to the supported Hub
      ontology.
- [ ] License and citation metadata are present.

## Local Validation

- [ ] `python scripts/validate_entry.py datasets/<dataset_name>`
- [ ] `python scripts/validate_all.py`
- [ ] `python scripts/build_index.py`
- [ ] `python scripts/build_index.py --check`
