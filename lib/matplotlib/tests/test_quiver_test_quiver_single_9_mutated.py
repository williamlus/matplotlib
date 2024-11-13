import platform
import sys
import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison

def draw_quiver(ax, **kwargs):
    X, Y = np.meshgrid(np.arange(0, 2 * np.pi, 1), np.arange(0, 2 * np.pi, 1))
    U = np.cos(X)
    V = np.sin(Y)
    Q = ax.quiver(U, V, **kwargs)
    return Q

def test_quiver_single_9_mutated():
    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.quiver([1], [1], [2], [2], units='height')
# Mutation info: Added units = height (Call ax.quiver)