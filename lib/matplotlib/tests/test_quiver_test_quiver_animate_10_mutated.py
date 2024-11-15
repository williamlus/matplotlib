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

def test_quiver_animate_10_mutated():
    fig, ax = plt.subplots()
    Q = draw_quiver(ax, animated=True)
    ax.quiverkey(Q, 0.5, 0.92, 2, '$2 \\frac{m}{s}$', labelpos='E', fontproperties={'weight': 'bold'})
# Mutation info: labelpos = <ast.Constant object at 0x7fc056e8b410> -> labelpos = E (Call ax.quiverkey)