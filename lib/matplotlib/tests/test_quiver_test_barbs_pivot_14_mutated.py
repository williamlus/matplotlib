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

@image_comparison(['barbs_pivot_test_image.png'], remove_text=True)
def test_barbs_pivot_14_mutated():
    x = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, x)
    U, V = (12 * X, 12 * Y)
    fig, ax = plt.subplots()
    ax.barbs(X, Y, U, V, fill_empty=False, rounding=False, pivot=1.7, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.3))
    ax.scatter(X, Y, s=49, c='black')
# Mutation info: fill_empty = True -> fill_empty = False (Call ax.barbs)