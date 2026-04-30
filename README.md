# Simulations and Algorithm Visualizations

This repository contains Python simulations and algorithm visualizations.

The existing simulation runner currently supports two Monte Carlo models:

- **Percolation**: cluster identification and spanning analysis across a range of
  occupation probabilities.
- **Ising**: two-dimensional Ising model with a temperature sweep producing
  lattice snapshots and a magnetization vs. temperature plot.

It also contains starter workspaces for new visual algorithm explorations:

- **Reinforcement Learning**: bandits, gridworlds, value iteration, Q-learning,
  policy gradients, and Monte Carlo control.
- **Probabilistic Robotics**: Bayes filters, Kalman filters, particle filters,
  occupancy grids, localization, and SLAM basics.

## Running simulations

Run `python run.py` to execute the simulation configured in
`config/default.yaml`. Modify this YAML file to change the model or parameters.
Results are saved as PNG images in `data/outputs/` which is ignored by git.

## Repository layout

- `src/` - shared simulation code and existing Monte Carlo models
- `tests/` - automated tests for the existing simulation models
- `config/` - YAML configuration for `run.py`
- `Reinforcement Learning/` - RL visualization notebooks, scripts, and notes
- `Probabilistic Robotics/` - robotics visualization notebooks, scripts, and notes
