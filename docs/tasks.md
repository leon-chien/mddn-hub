# Task Ontology

MDDataNet Hub indexes trajectory-learning task datasets. A task defines what a
model is expected to learn from standardized molecular dynamics data.

## Supported Task Types

- `future_event_prediction`: predict whether a target event occurs within a
  future horizon.
- `transition_detection`: identify transition points or windows between states.
- `state_classification`: classify frames or windows into operational states.
- `trajectory_forecasting`: predict future coordinates, features, or states.
- `interaction_prediction`: predict molecular interaction events or changes.

## Example Benchmark Tasks

- `ligand_unbinding_future_500`
- `ligand_binding_future_500`
- `dimerization_future_1000`
- `dissociation_future_1000`
- `protein_unfolding_future_1000`
- `native_contact_loss_future_500`

## Label Semantics

Labels are operational definitions generated from event rules, presets, or
explicit analysis configuration. They support reproducible ML benchmarking, but
they should not be interpreted as universal biological truth without reviewing
the event configuration.
