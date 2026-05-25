# Training From Hub Metadata

MDDataNet Hub entries tell ML users where a package lives and how to interpret
its task metadata. The Hub does not host large package files directly.

## Read Download Metadata

Each dataset entry includes `download.yaml`. The `package` asset points to the
external `.mddatanet.zip` package.

```python
from pathlib import Path

import yaml

entry_dir = Path("datasets/ligand_unbinding_demo_from_cli")
download = yaml.safe_load((entry_dir / "download.yaml").read_text())

package_url = download["package"]["url"]
expected_sha256 = download["package"]["sha256"]
print(package_url, expected_sha256)
```

Download the package from `package_url` using your preferred HTTP client or
storage provider tool, then verify the file against `expected_sha256` before
training.

```python
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


package_path = Path("ligand_unbinding_demo.mddatanet.zip")
assert sha256_file(package_path) == expected_sha256
```

## Load With MDDataNetDataset

Use the package with the `mddatanet` Python loader.

```python
from mddatanet import MDDataNetDataset

dataset = MDDataNetDataset(
    "ligand_unbinding_demo.mddatanet.zip",
    window_length=64,
    target="ligand_unbinding_future_2",
)

item = dataset[0]
coordinates = item["coordinates"]
label = item["label"]
valid = item["valid"]
```

The target name should match the task metadata and package label arrays. For
future-event prediction, the common pattern is:

```text
frames t-W:t -> predict event in t:t+H
```

## Linked Or External Coordinates

Some packages use external coordinate storage. In those cases, `download.yaml`
may include additional assets such as `coordinates` or `topology`. Download and
verify those assets before training coordinate-based models.

The Hub entry remains metadata-first: it records where assets live, how to check
them, and how to interpret the ML task. It does not run downloads, uploads,
preprocessing jobs, or hosted training services.
