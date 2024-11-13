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

def test_quiver_xy_26_mutated():
    fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
    ax.quiver(0, 0, 1, 1, angles='xy', scale_units='xy', scale=1, pivot='middle')
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
# Mutation info: Added pivot = middle (Call ax.quiver)