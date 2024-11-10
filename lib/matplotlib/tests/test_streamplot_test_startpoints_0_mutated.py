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

def test_startpoints_0_mutated():
    X, Y, U, V = velocity_field()
    start_x, start_y = np.meshgrid(np.linspace(X.min(), X.max(), 5), np.linspace(Y.min(), Y.max(), 5))
    start_points = np.column_stack([start_x.ravel(), start_y.ravel()])
    plt.streamplot(X, Y, U, V, start_points=start_points, broken_streamlines=False)
    plt.plot(start_x, start_y, 'ok')