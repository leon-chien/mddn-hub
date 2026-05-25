# Ligand Unbinding Demo

## Summary

`ligand_unbinding_demo` is a non-production example entry that demonstrates the
metadata structure for a future-event prediction dataset. It is intended for Hub
validation and documentation only.

## Scientific System

The example represents a protein-ligand molecular dynamics system with a
placeholder kinase-like receptor and a small-molecule ligand. The system
metadata is illustrative and should not be used as a scientific benchmark.

## Task

The benchmark task is future event prediction: given a trajectory window,
predict whether ligand unbinding occurs within the next 500 frames.

Labels are rule-based operational labels generated from predefined event
definitions and should not be interpreted as universal biological truth without
reviewing the event configuration.

## Label Definition

The demo label is defined as positive when a ligand-protein contact distance
rule crosses a configured unbinding threshold within the future horizon. The
exact event configuration is illustrative.

## Split Policy

The example uses `trajectory_split`, where train, validation, and test examples
come from distinct trajectories.

## Storage

The referenced URLs are stable example URLs and do not point to production
MDDataNet assets. Real submissions must provide externally hosted downloadable
assets and matching SHA-256 checksums.

## Intended Use

Use this entry as a template for metadata structure, validation behavior, and
dataset card content.

## Limitations

This is not a scientific benchmark and should not be used for model comparison.

## License

CC-BY-4.0 for the demo metadata.
