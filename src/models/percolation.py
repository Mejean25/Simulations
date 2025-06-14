import numpy as np
import matplotlib.pyplot as plt
import os

def label_clusters(grid):
    L = grid.shape[0]
    labels = np.zeros_like(grid, dtype=int)
    label = 1

    for i in range(L):
        for j in range(L):
            if grid[i, j]:
                neighbors = []
                if i > 0 and labels[i-1, j] > 0:
                    neighbors.append(labels[i-1, j])
                if j > 0 and labels[i, j-1] > 0:
                    neighbors.append(labels[i, j-1])
                if neighbors:
                    min_label = min(neighbors)
                    labels[i, j] = min_label
                    for n in neighbors:
                        labels[labels == n] = min_label
                else:
                    labels[i, j] = label
                    label += 1
    return labels

def find_spanning_label(labels):
    top_labels = set(labels[0, labels[0, :] > 0])
    bottom_labels = set(labels[-1, labels[-1, :] > 0])
    span_labels = top_labels & bottom_labels
    return span_labels.pop() if span_labels else None

def run(config):
    L = config['lattice_size']
    seed = config['seed']
    os.makedirs(config['output_dir'], exist_ok=True)
    np.random.seed(seed)

    probabilities = np.linspace(0.4, 0.7, 7)
    max_cluster_sizes = []

    for idx, p in enumerate(probabilities):
        grid = np.random.rand(L, L) < p
        labels = label_clusters(grid)

        # Cluster sizes (excluding 0 = unoccupied)
        unique, counts = np.unique(labels[labels > 0], return_counts=True)
        cluster_sizes = dict(zip(unique, counts))
        max_cluster_size = max(cluster_sizes.values()) if cluster_sizes else 0
        max_cluster_sizes.append(max_cluster_size)

        # Check for spanning cluster
        span_label = find_spanning_label(labels)
        rgb_image = np.zeros((L, L, 3), dtype=float)
        rgb_image[labels > 0] = [0.5, 0.5, 0.5]  # grey background
        if span_label:
            rgb_image[labels == span_label] = [0.0, 0.0, 1.0]  # blue spanning cluster

        plt.figure()
        plt.imshow(rgb_image, interpolation='nearest')
        title = f'p = {p:.2f}, Max Cluster = {max_cluster_size}'
        if span_label:
            title += " (spanning)"
        plt.title(title)
        plt.axis("off")
        plt.savefig(f"{config['output_dir']}/percolation_p{int(p*100)}.png")
        plt.close()

    # Plot max cluster size vs. probability
    plt.figure()
    plt.plot(probabilities, max_cluster_sizes, marker='o')
    plt.title('Max Cluster Size vs Probability')
    plt.xlabel('Occupation Probability p')
    plt.ylabel('Max Cluster Size')
    plt.grid(True)
    plt.savefig(f"{config['output_dir']}/max_cluster_vs_p.png")
