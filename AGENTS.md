# AGENTS.md

This repository is the MDDataNet Hub: a metadata registry and benchmark
ecosystem for molecular dynamics trajectory-learning datasets.

## Core Boundary

Preserve the Hub boundary in every change:

- The Hub stores metadata, schemas, docs, checksums, citations, and external
  download locations.
- The Hub does not store large trajectory archives, topology collections,
  `.mddatanet.zip` packages, Zarr stores, or raw simulation outputs.
- The Hub does not run MD simulations, cloud preprocessing, or HPC jobs.
- The primary registry object is a trajectory-learning task dataset, not a
  simulation, trajectory file, or topology file.

## Change Discipline

- Keep schemas, validators, docs, and example dataset entries synchronized.
- Prefer strict validation for core metadata and an `extensions` object for
  scientific fields that may evolve.
- Add new task types, split policies, or storage profiles in the docs and
  schemas together.
- Do not weaken validation to make one entry pass unless the rule is genuinely
  wrong for the registry.
- Keep dataset names lowercase snake case and aligned with their directory name.
- Make operational label definitions explicit; labels generated from rules or
  presets must not be presented as universal biological truth.

## Validation

Before finishing changes that touch dataset entries, schemas, scripts, or docs,
run:

```bash
python scripts/validate_entry.py datasets/ligand_unbinding_demo
python scripts/validate_all.py
```

If validation dependencies are missing, install the project dependencies from
`pyproject.toml` in a local environment.

## Large Files

Never commit large data artifacts. Keep these outside the repo and reference
them through `download.yaml` plus `checksums.json`:

- `.mddatanet.zip`
- `.zarr/` stores or `.zarr.zip`
- trajectory formats such as `.xtc`, `.dcd`, `.trr`, `.nc`, `.h5`, `.hdf5`
- topology-heavy data dumps or downloaded package caches

## Review Focus

When reviewing or modifying entries, check:

- scientific system and provenance clarity
- task type and target event semantics
- label-generation method and limitations
- split policy and leakage risk
- license, citation, and external download metadata
- checksum format and reproducibility fields
- schema and CI validation status
