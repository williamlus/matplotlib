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

@image_comparison(['quiver_key_pivot.png'], remove_text=True)
def test_quiver_key_pivot_13_mutated():
    fig, ax = plt.subplots()
    u, v = np.mgrid[0:2 * np.pi:10j, 0:2 * np.pi:10j]
    q = ax.quiver(np.sin(u), np.cos(v))
    ax.set_xlim(-2, 11)
    ax.set_ylim(-2, 11, auto=True)
    ax.quiverkey(q, 0.5, 1, 1, 'N', labelpos='N')
    ax.quiverkey(q, 1, 0.5, 1, 'E', labelpos='E')
    ax.quiverkey(q, 0.5, 0, 1, 'S', labelpos='S')
    ax.quiverkey(q, 0, 0.5, 1, 'W', labelpos='W')
# Mutation info: Added auto = True (Call ax.set_ylim)