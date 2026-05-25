# Review Guidelines

Maintainers should review dataset entries for registry validity, benchmark
clarity, and reproducibility.

## Scientific Review

- Is the molecular system described clearly enough for ML users?
- Are MD engine, topology, trajectory source, and preprocessing provenance
  documented?
- Are limitations and known biases stated?

## Task Semantics

- Does the entry represent a trajectory-learning task dataset?
- Is the task type part of the supported ontology?
- Are target events and horizons defined precisely?
- Are labels described as operational definitions generated from rules or
  presets?

## Splits And Leakage

- Is the split policy one of the supported policies?
- Does the split avoid obvious leakage across frames, trajectories, runs,
  protein families, or ligand scaffolds?
- Random frame splits should be challenged unless there is a strong benchmark
  justification.

## Reproducibility

- Are external downloads provided instead of committed large files?
- Are SHA-256 hashes syntactically valid?
- Are licenses and citations present?
- Does `metadata.json` agree with the dataset directory name?
- Does the entry pass `python scripts/validate_entry.py datasets/<name>`?

## Merge Criteria

Merge only when schema validation passes, required documentation is present, and
the entry's benchmark semantics are clear enough for independent ML users.
