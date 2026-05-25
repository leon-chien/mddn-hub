# MDDataNet Hub

MDDataNet Hub is a standardized registry and benchmark ecosystem for molecular
dynamics trajectory-learning datasets. It is the metadata side of MDDataNet:
the [MDDataNet CLI](https://github.com/leon-chien/mddn-cli) creates
`.mddatanet.zip` packages, contributors upload those packages to external
storage, and the Hub records the metadata and download links needed to discover,
validate, and train on them.

It is not a trajectory hosting platform. The Hub stores metadata, schemas, task
semantics, validation rules, dataset cards, provenance, checksums,
`registry/index.json`, and external download locations. Large trajectory
packages live in external storage systems such as Hugging Face Datasets, Zenodo,
S3, Cloudflare R2, institutional storage, or MDRepo.

The primary object in this repository is a trajectory-learning task dataset,
for example:

- `ligand_unbinding_future_500`
- `dimerization_future_1000`
- `protein_unfolding_future_1000`
- `salt_bridge_breaking_future_200`

## What The Hub Indexes

- Datasets and dataset cards
- Task ontology and benchmark semantics
- Label definitions and operational event rules
- Split policies designed to reduce leakage
- Metadata, provenance, licenses, citations, and checksums
- External package and asset download locations

## What The Hub Does Not Do

- Host petabyte-scale trajectory archives
- Run molecular dynamics simulations
- Execute HPC preprocessing jobs
- Act as the canonical topology or trajectory archive
- Replace scientific review of operational labels

## Ecosystem Architecture

MDDataNet is organized into three layers:

1. `mddatanet` CLI/library
   - Converts raw MD into standardized ML-ready packages.
   - Generates labels, future-event labels, splits, and Hub manifests.
   - Validates local `.mddatanet.zip` packages.
   - Exposes Python loaders.

2. External storage providers
   - Store large package, trajectory, coordinate, or topology files.
   - Examples: Hugging Face Datasets, Zenodo, S3, Cloudflare R2,
     institutional HPC storage, and MDRepo.

3. `mddatanet-hub`
   - Indexes metadata and task semantics.
   - Validates dataset entries through schemas and CI.
   - Documents benchmark expectations and contribution review rules.
   - Provides a future substrate for search, website browsing, and leaderboards.

## End-To-End Model

The intended registry workflow is deliberately small and reproducible:

1. The `mddatanet` CLI creates a validated `.mddatanet.zip` package.
2. The contributor uploads the package to external storage.
3. The contributor exports Hub metadata with `mddatanet export-manifest`.
4. The Hub stores only the metadata folder, download links, checksums, schemas,
   dataset card, and generated registry index.
5. Users read `download.yaml`, download and verify the package, then train with
   `MDDataNetDataset`.

```python
from mddatanet import MDDataNetDataset

dataset = MDDataNetDataset(
    "ligand_unbinding_demo.mddatanet.zip",
    window_length=64,
    target="ligand_unbinding_future_500",
)
```

## Use The CLI With The Hub

Install the CLI from the sibling project when working locally:

```bash
cd ../mddn-cli
python -m pip install -e ".[dev]"
```

Create a demo package or a real package with the CLI, then validate it:

```bash
mddatanet demo --out-dir outputs
mddatanet validate outputs/ligand_unbinding_demo.mddatanet.zip
```

Export Hub metadata after uploading the package to external storage. If the
package is not uploaded yet, the CLI writes a schema-valid placeholder URL that
can be replaced before review.

```bash
mddatanet export-manifest outputs/ligand_unbinding_demo.mddatanet.zip \
  --out ligand_unbinding_demo_from_cli \
  --dataset-id ligand_unbinding_demo_from_cli \
  --download-url https://example.org/ligand_unbinding_demo.mddatanet.zip
```

Submit the exported metadata by copying the folder into
`datasets/<dataset_name>/`, then validate the registry:

```bash
cp -R ligand_unbinding_demo_from_cli datasets/
python scripts/validate_entry.py datasets/ligand_unbinding_demo_from_cli
python scripts/validate_all.py
python scripts/build_index.py
python scripts/build_index.py --check
```

Users train by reading `download.yaml`, downloading and verifying the package,
and loading it with `MDDataNetDataset`. See
[docs/training_from_hub.md](docs/training_from_hub.md).

To prove the local CLI and Hub work together end to end, run:

```bash
python scripts/e2e_cli_hub_demo.py
```

## Repository Layout

```text
datasets/
  <dataset_name>/
    dataset_card.md
    metadata.json
    manifest.json
    download.yaml
    checksums.json
schemas/
scripts/
docs/
registry/
  index.json
```

Each directory under `datasets/` is a metadata package for one
trajectory-learning task dataset. Required files and validation rules are
described in [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md).

The generated [registry/index.json](registry/index.json) is the machine-readable
catalog assembled from all validated dataset entries.

## Hub V0 Status

Hub v0 is a working registry milestone:

- README explains the Hub purpose and boundary.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains the dataset PR flow.
- [DATASET_REQUIREMENTS.md](DATASET_REQUIREMENTS.md) explains required files.
- [REVIEW_GUIDELINES.md](REVIEW_GUIDELINES.md) explains maintainer review.
- JSON schemas validate dataset entries.
- CI runs `python scripts/validate_all.py` and
  `python scripts/build_index.py --check`.
- `registry/index.json` exists and is checked for freshness.
- At least one CLI-exported dataset entry validates.
- [docs/training_from_hub.md](docs/training_from_hub.md) shows how to train
  from Hub metadata with `download.yaml` and `MDDataNetDataset`.

## Quick Validation

Install the validation dependencies, then run:

```bash
python scripts/validate_entry.py datasets/ligand_unbinding_demo
python scripts/validate_all.py
python scripts/build_index.py --check
python scripts/e2e_cli_hub_demo.py
```

The same validation and index freshness checks run in GitHub Actions for pull
requests and pushes to `main`.

## Contributing

Contributors should create and validate MDDataNet packages locally, upload large
files to an external storage provider, export Hub metadata from the CLI, then
submit only the metadata entry to this repository.

See [CONTRIBUTING.md](CONTRIBUTING.md) and
[docs/contribution_flow.md](docs/contribution_flow.md).
