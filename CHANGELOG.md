# Changelog

All notable changes to MDDataNet Hub will be documented here.

## 0.1.0 - Unreleased

### Added

- Metadata registry scaffold for MDDataNet trajectory-learning datasets.
- JSON schemas and validation scripts for Hub dataset entries.
- Generated `registry/index.json` catalog with CI freshness checks.
- CLI-exported ligand unbinding demo entry that validates against Hub schemas.
- Dataset contribution, review, split policy, storage profile, and training
  documentation.
- End-to-end CLI-to-Hub proof script for demo package creation, manifest export,
  Hub validation, index generation, and `MDDataNetDataset` loading.

### Notes

- Hub stores metadata, download links, checksums, cards, schemas, and registry
  indexes. It does not host large trajectories, run preprocessing jobs, provide
  a hosted API, or implement distributed workers.
