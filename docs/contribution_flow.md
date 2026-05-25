# Contribution Flow

The Hub contribution flow keeps compute-heavy and storage-heavy work outside
this repository.

1. Run the `mddatanet` CLI locally on source MD data.
2. Generate labels and future-event labels from explicit rules or presets.
3. Generate leakage-aware splits.
4. Validate the package locally.
5. Upload large package, coordinate, or topology files to external storage.
6. Export Hub metadata.
7. Copy the metadata directory into `datasets/<dataset_name>/`.
8. Run Hub validation.
9. Open a pull request.

Example:

```bash
mddatanet convert ...
mddatanet analyze ...
mddatanet split ...
mddatanet validate --hub-ready ...
mddatanet export-manifest --input dataset.mddatanet.zip --out hub_entry/
python scripts/validate_entry.py datasets/<dataset_name>
```

Do not commit trajectory files, `.mddatanet.zip` packages, or Zarr stores.
