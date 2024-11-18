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

@image_comparison(['quiver_with_key_test_image.png'])
def test_quiver_with_key_13_mutated():
    fig, ax = plt.subplots()
    ax.margins(0.1)
    Q = draw_quiver(ax)
    ax.quiverkey(Q, 0.5, 0.95, 2, '$2\\, \\mathrm{m}\\, \\mathrm{s}^{-1}$', angle=-10, coordinates='inches', labelpos='W', fontproperties={'weight': 'bold', 'size': 'large'})
# Mutation info: coordinates = <ast.Constant object at 0x7fc3240e3890> -> coordinates = inches (Call ax.quiverkey)