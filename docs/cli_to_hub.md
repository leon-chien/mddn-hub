# CLI To Hub Metadata Flow

The `mddatanet` CLI creates standardized ML-ready trajectory datasets. The Hub
organizes and validates the metadata exported by that CLI.

## Expected Flow

```bash
mddatanet convert ...
mddatanet analyze ...
mddatanet split ...
mddatanet validate dataset.mddatanet.zip
mddatanet export-manifest dataset.mddatanet.zip \
  --out hub_entry/ \
  --download-url https://example.org/dataset.mddatanet.zip
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

## End-To-End Proof

The Hub includes a local proof script that exercises the current ecosystem
without modifying tracked dataset entries:

```bash
python scripts/e2e_cli_hub_demo.py
```

The script runs `mddatanet demo`, exports a Hub manifest, copies the exported
metadata into a temporary Hub datasets overlay, validates the entry, builds and
checks a temporary index, and loads the package with `MDDataNetDataset`.

Expected output ends with lines similar to:

```text
MDDataNet ecosystem proof complete
package: /tmp/.../cli_outputs/ligand_unbinding_demo.mddatanet.zip
exported files: baseline_metrics.json, checksums.json, dataset_card.md, download.yaml, label_statistics.json, manifest.json, metadata.json
hub validation: OK
temporary index: OK
loader item: coordinates_shape=(2, 5, 3) label=True valid=True
```
