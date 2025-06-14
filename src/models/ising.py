#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 22:39:35 2025

@author: leapcube
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def run(config):
    L = config['lattice_size']
    steps = config['steps']
    seed = config['seed']
    np.random.seed(seed)

    os.makedirs(config['output_dir'], exist_ok=True)

    temperatures = np.linspace(1.0, 4.0, 16)
    avg_magnetizations = []

    for T in temperatures:
        lattice = np.random.choice([-1, 1], size=(L, L))

        def delta_energy(i, j):
            neighbors = lattice[(i+1)%L, j] + lattice[i, (j+1)%L] +                         lattice[(i-1)%L, j] + lattice[i, (j-1)%L]
            return 2 * lattice[i, j] * neighbors

        for _ in range(steps):
            i, j = np.random.randint(0, L, 2)
            dE = delta_energy(i, j)
            if dE < 0 or np.random.rand() < np.exp(-dE / T):
                lattice[i, j] *= -1

        magnetization = np.abs(np.sum(lattice)) / (L * L)
        avg_magnetizations.append(magnetization)

        plt.figure()
        plt.imshow(lattice, cmap='coolwarm')
        plt.title(f'Ising Model at T={T:.2f}, M={magnetization:.2f}')
        plt.axis('off')
        plt.savefig(f"{config['output_dir']}/ising_T{T:.2f}.png")
        plt.close()

    # Plot magnetization vs. temperature
    plt.figure()
    plt.plot(temperatures, avg_magnetizations, marker='o')
    plt.title('Magnetization vs Temperature')
    plt.xlabel('Temperature T')
    plt.ylabel('Average Magnetization')
    plt.grid(True)
    plt.savefig(f"{config['output_dir']}/ising_magnetization_vs_T.png")
    plt.close()
