# Monte Carlo Simulations

This repository contains simple Monte Carlo simulations implemented in Python.
It currently supports two models:

- **Percolation**: cluster identification and spanning analysis across a range of
  occupation probabilities.
- **Ising**: two-dimensional Ising model with a temperature sweep producing
  lattice snapshots and a magnetization vs. temperature plot.

## Running simulations

Run `python run.py` to execute the simulation configured in
`config/default.yaml`. Modify this YAML file to change the model or parameters.
Results are saved as PNG images in `data/outputs/` which is ignored by git.
