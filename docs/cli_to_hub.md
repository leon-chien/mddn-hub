# CLI To Hub Metadata Flow

The `mddatanet` CLI creates standardized ML-ready trajectory datasets. The Hub
organizes and validates the metadata exported by that CLI.

## Expected Flow

```bash
mddatanet convert ...
mddatanet analyze ...
mddatanet split ...
mddatanet validate --hub-ready ...
mddatanet export-manifest \
  --input dataset.mddatanet.zip \
  --out hub_entry/
```

The export step should generate:

- `dataset_card.md`
- `metadata.json`
- `manifest.json`
- `download.yaml`
- `checksums.json`
- optional `citation.bib`
- optional `label_statistics.json`

After export, the contributor uploads large files externally and copies the
metadata folder into this repository under `datasets/<dataset_name>/`.

## Hub Responsibilities

The Hub validates metadata shape, ontology membership, split semantics, checksum
format, and URL syntax. It does not open or process the large external packages
during normal registry validation.
