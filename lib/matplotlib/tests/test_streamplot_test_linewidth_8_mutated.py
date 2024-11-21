import numpy as np
from numpy.testing import assert_array_almost_equal
import pytest
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
import matplotlib.transforms as mtransforms

def velocity_field():
    Y, X = np.mgrid[-3:3:100j, -3:3:200j]
    U = -1 - X ** 2 + Y
    V = 1 + X - Y ** 2
    return (X, Y, U, V)

def swirl_velocity_field():
    x = np.linspace(-3.0, 3.0, 200)
    y = np.linspace(-3.0, 3.0, 100)
    X, Y = np.meshgrid(x, y)
    a = 0.1
    U = np.cos(a) * -Y - np.sin(a) * X
    V = np.sin(a) * -Y + np.cos(a) * X
    return (x, y, U, V)

@image_comparison(['streamplot_linewidth'], remove_text=True, style='mpl20', tol=0.004)
def test_linewidth_8_mutated():
    X, Y, U, V = velocity_field()
    speed = np.hypot(U, V)
    lw = 5 * speed / speed.max()
    ax = plt.figure(layout='compressed').subplots()
    ax.streamplot(X, Y, U, V, density=[0.5, 1], color='k', linewidth=lw)
# Mutation info: Added layout = compressed (Call plt.figure)