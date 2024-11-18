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

@image_comparison(['quiver_single_test_image.png'], remove_text=True)
def test_quiver_single_1_mutated():
    fig, ax = plt.subplots(sharex=True)
    ax.margins(0.1)
    ax.quiver([1], [1], [2], [2])
# Mutation info: Added sharex = True (Call plt.subplots)