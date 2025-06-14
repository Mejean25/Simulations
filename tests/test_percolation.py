import numpy as np
from src.models.percolation import label_clusters, find_spanning_label


def test_label_clusters_small_grid():
    grid = np.array([
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1]
    ], dtype=bool)
    labels = label_clusters(grid)
    expected = np.array([
        [1, 1, 0],
        [1, 0, 2],
        [0, 2, 2]
    ])
    assert np.array_equal(labels, expected)


def test_find_spanning_label_detects_span():
    grid = np.array([
        [1, 0, 0],
        [1, 0, 0],
        [1, 0, 0]
    ], dtype=bool)
    labels = label_clusters(grid)
    span = find_spanning_label(labels)
    assert span == 1


def test_find_spanning_label_returns_none():
    grid = np.array([
        [1, 1, 0],
        [0, 0, 0],
        [0, 1, 1]
    ], dtype=bool)
    labels = label_clusters(grid)
    span = find_spanning_label(labels)
    assert span is None

