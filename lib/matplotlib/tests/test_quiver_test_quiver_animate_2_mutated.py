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

def test_quiver_animate_2_mutated():
    fig, ax = plt.subplots(squeeze=True)
    Q = draw_quiver(ax, animated=True)
    ax.quiverkey(Q, 0.5, 0.92, 2, '$2 \\frac{m}{s}$', labelpos='W', fontproperties={'weight': 'bold'})