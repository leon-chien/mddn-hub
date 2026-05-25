# Split Policies

MDDataNet Hub standardizes split semantics to reduce leakage in trajectory
learning benchmarks.

## Supported Policies

- `trajectory_split`: train, validation, and test sets use distinct
  trajectories.
- `run_split`: sets are separated by independent simulation runs.
- `temporal_split`: later time windows are held out from earlier training
  windows.
- `protein_family_split`: related proteins are grouped to test family-level
  generalization.
- `ligand_scaffold_split`: ligand scaffolds are separated to test chemical
  generalization.

## Discouraged Policy

Random frame splits are discouraged because neighboring MD frames are often
strongly correlated. They can inflate benchmark performance through temporal
leakage unless carefully justified.
