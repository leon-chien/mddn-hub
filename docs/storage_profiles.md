# Storage Profiles

Storage profiles describe how a Hub entry references the data needed by ML
users. They do not imply that the Hub hosts large files.

## Profiles

- `metadata_only`: the entry documents task semantics but does not provide a
  complete downloadable package.
- `compressed`: a compressed external package is available, such as a
  `.mddatanet.zip` file.
- `external_coordinates`: metadata and labels are packaged, while coordinates
  are stored as separate external assets.
- `full_package_external`: all required ML-ready package artifacts are hosted
  externally and referenced by URL.

Use `download.yaml` and `checksums.json` to describe external assets and
verification metadata.
