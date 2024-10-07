import numpy as np
from numpy.testing import assert_array_almost_equal
import pytest
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
import matplotlib.transforms as mtransforms
@image_comparison(['streamplot_startpoints'], remove_text=True, style='mpl20', extensions=['png'])
def mutated_test_startpoints():
    X, Y, U, V = velocity_field()
    start_x, start_y = np.meshgrid(np.linspace(X.min(), X.max(), 5), np.linspace(Y.min(), Y.max(), 5))
    start_points = np.column_stack([start_x.ravel(), start_y.ravel()])
    plt.streamplot(X, Y, U, V, start_points=start_points)
    plt.plot(start_x, start_y, 'ok')
@image_comparison(['streamplot_colormap'], remove_text=True, style='mpl20', tol=0.022)
def mutated_test_colormap():
    X, Y, U, V = velocity_field()
    plt.streamplot(X, Y, U, V, color=U, density=0.6, linewidth=2, cmap=plt.cm.autumn)
    plt.colorbar()
@image_comparison(['streamplot_linewidth'], remove_text=True, style='mpl20', tol=0.004)
def mutated_test_linewidth():
    X, Y, U, V = velocity_field()
    speed = np.hypot(U, V)
    lw = 5 * speed / speed.max()
    ax = plt.figure().subplots()
    ax.streamplot(X, Y, U, V, density=[0.5, 1], color='k', linewidth=lw)
@image_comparison(['streamplot_masks_and_nans'], remove_text=True, style='mpl20')
def mutated_test_masks_and_nans():
    X, Y, U, V = velocity_field()
    mask = np.zeros(U.shape, dtype=bool)
    mask[40:60, 80:120] = 1
    U[:20, :40] = np.nan
    U = np.ma.array(U, mask=mask)
    ax = plt.figure().subplots()
    with np.errstate(invalid='ignore'):
        ax.streamplot(X, Y, U, V, color=U, cmap=plt.cm.Blues)
@image_comparison(['streamplot_maxlength.png'], remove_text=True, style='mpl20', tol=0.302)
def mutated_test_maxlength():
    x, y, U, V = swirl_velocity_field()
    ax = plt.figure().subplots()
    ax.streamplot(x, y, U, V, maxlength=10.0, start_points=[[0.0, 1.5]], linewidth=2, density=2)
    assert ax.get_xlim()[-1] == ax.get_ylim()[-1] == 3
    ax.set(xlim=(None, 3.2555988021882305), ylim=(None, 3.078326760195413))
@image_comparison(['streamplot_maxlength_no_broken.png'], remove_text=True, style='mpl20', tol=0.302)
def mutated_test_maxlength_no_broken():
    x, y, U, V = swirl_velocity_field()
    ax = plt.figure().subplots()
    ax.streamplot(x, y, U, V, maxlength=10.0, start_points=[[0.0, 1.5]], linewidth=2, density=2, broken_streamlines=False)
    assert ax.get_xlim()[-1] == ax.get_ylim()[-1] == 3
    ax.set(xlim=(None, 3.2555988021882305), ylim=(None, 3.078326760195413))
@image_comparison(['streamplot_direction.png'], remove_text=True, style='mpl20', tol=0.073)
def mutated_test_direction():
    x, y, U, V = swirl_velocity_field()
    plt.streamplot(x, y, U, V, integration_direction='backward', maxlength=1.5, start_points=[[1.5, 0.0]], linewidth=2, density=2)
