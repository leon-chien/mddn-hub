# ligand_unbinding_demo

## Summary
Synthetic runtime demo labeled for ligand unbinding.

## System
- Type: protein
- Atoms: 5
- Residues: 2
- Frames: 5
- Runs: 1
- Timestep: 1.0 ps

## Trajectory Storage
- Data mode: hybrid
- Storage profile: compressed
- Coordinates included: yes
- Coordinate path: dataset.zarr/trajectory/positions
- Coordinate dtype: float32
- Compression: zstd
- Chunk frames: 100
- Chunk atoms: 1000
- Stride: 1
- Stored/source frames: 5/5
- Quantized: no

## Source
- Topology: /Users/leonchien/Projects/mddn-cli/outputs/_ligand_unbinding_demo_work/ligand_unbinding_demo.pdb
- Coordinates: none
- Trajectory: unknown

## Features
- ligand_pocket_min_distance

## Events
- ligand_unbinding

## Label Statistics
- ligand_unbinding: event_now positive rate 0.400; valid future positive rate 0.667; valid future frames 3; transitions 1

## Splits
temporal

## Limitations
Labels are reproducible operational definitions derived from trajectory features.
They should not be treated as universal biological truths.
For linked packages, coordinate-based ML models must download the coordinate store listed in `download.yaml`.

## License
unknown

## Reproduce
- `mddatanet demo ligand_unbinding`
- `mddatanet demo ligand_unbinding`
