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

def test_maxlength_no_broken_4_mutated():
    x, y, U, V = swirl_velocity_field()
    ax = plt.figure(frameon=False).subplots()
    ax.streamplot(x, y, U, V, maxlength=10.0, start_points=[[0.0, 1.5]], linewidth=2, density=2, broken_streamlines=False)
    assert ax.get_xlim()[-1] == ax.get_ylim()[-1] == 3
    ax.set(xlim=(None, 3.2555988021882305), ylim=(None, 3.078326760195413))
# Mutation info: Added frameon = False (Call plt.figure)