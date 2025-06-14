#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 22:39:35 2025

@author: leapcube
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange
import os

def _metropolis_step(lattice, beta):
    """Perform one Metropolis update."""
    L = lattice.shape[0]
    i, j = np.random.randint(0, L, 2)
    neighbors = (
        lattice[(i + 1) % L, j]
        + lattice[(i - 1) % L, j]
        + lattice[i, (j + 1) % L]
        + lattice[i, (j - 1) % L]
    )
    dE = 2 * lattice[i, j] * neighbors
    if dE <= 0 or np.random.rand() < np.exp(-beta * dE):
        lattice[i, j] *= -1


def _wolff_step(lattice, beta):
    """Perform one Wolff cluster update."""
    L = lattice.shape[0]
    i = np.random.randint(0, L)
    j = np.random.randint(0, L)
    spin = lattice[i, j]
    cluster = {(i, j)}
    stack = [(i, j)]
    p_add = 1 - np.exp(-2 * beta)

    while stack:
        x, y = stack.pop()
        neighbors = [
            ((x + 1) % L, y),
            ((x - 1) % L, y),
            (x, (y + 1) % L),
            (x, (y - 1) % L),
        ]
        for nx, ny in neighbors:
            if (nx, ny) not in cluster and lattice[nx, ny] == spin:
                if np.random.rand() < p_add:
                    cluster.add((nx, ny))
                    stack.append((nx, ny))

    for x, y in cluster:
        lattice[x, y] *= -1


def run(config):
    """Run a 2D Ising simulation using Metropolis or Wolff updates."""
    L = config["lattice_size"]
    steps = config["steps"]
    seed = config["seed"]
    np.random.seed(seed)

    os.makedirs(config["output_dir"], exist_ok=True)

    t_min = config.get("T_min", 1.0)
    t_max = config.get("T_max", 4.0)
    num_temps = config.get("num_temps", 16)
    algorithm = config.get("algorithm", "wolff").lower()

    temperatures = np.linspace(t_min, t_max, num_temps)
    avg_magnetizations = []

    for T in temperatures:
        lattice = np.random.choice([-1, 1], size=(L, L))
        beta = 1.0 / T

        for _ in trange(steps, desc=f"T={T:.2f}", leave=False):
            if algorithm == "wolff":
                _wolff_step(lattice, beta)
            else:
                _metropolis_step(lattice, beta)

        magnetization = np.abs(np.mean(lattice))
        avg_magnetizations.append(magnetization)

        plt.figure()
        plt.imshow(lattice, cmap="coolwarm", vmin=-1, vmax=1)
        plt.title(f"Ising Model at T={T:.2f}, M={magnetization:.2f}")
        plt.axis("off")
        plt.savefig(f"{config['output_dir']}/ising_T{T:.2f}.png")
        plt.close()

    # Plot magnetization vs. temperature
    plt.figure()
    plt.plot(temperatures, avg_magnetizations, marker="o")
    plt.title("Magnetization vs Temperature")
    plt.xlabel("Temperature T")
    plt.ylabel("Average Magnetization")
    plt.grid(True)
    plt.savefig(f"{config['output_dir']}/ising_magnetization_vs_T.png")
    plt.close()

    return np.array(avg_magnetizations)
