import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_array_less
import numpy.ma.testutils as matest
import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.path import Path
from matplotlib.testing.decorators import image_comparison, check_figures_equal

class TestTriangulationParams:
    x = [-1, 0, 1, 0]
    y = [0, -1, 0, 1]
    triangles = [[0, 1, 2], [0, 2, 3]]
    mask = [False, True]

    @pytest.mark.parametrize('args, kwargs, expected', [([x, y], {}, [x, y, None, None]), ([x, y, triangles], {}, [x, y, triangles, None]), ([x, y], dict(triangles=triangles), [x, y, triangles, None]), ([x, y], dict(mask=mask), [x, y, None, mask]), ([x, y, triangles], dict(mask=mask), [x, y, triangles, mask]), ([x, y], dict(triangles=triangles, mask=mask), [x, y, triangles, mask])])
    def test_extract_triangulation_params(self, args, kwargs, expected):
        other_args = [1, 2]
        other_kwargs = {'a': 3, 'b': '4'}
        x_, y_, triangles_, mask_, args_, kwargs_ = mtri.Triangulation._extract_triangulation_params(args + other_args, {**kwargs, **other_kwargs})
        x, y, triangles, mask = expected
        assert x_ is x
        assert y_ is y
        assert_array_equal(triangles_, triangles)
        assert mask_ is mask
        assert args_ == other_args
        assert kwargs_ == other_kwargs
@image_comparison(['tripcolor1.png'])
def mutated_test_tripcolor():
    x = np.asarray([0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0.75])
    y = np.asarray([0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1, 0.75])
    triangles = np.asarray([[0, 1, 3], [1, 4, 3], [1, 2, 4], [2, 5, 4], [3, 4, 6], [4, 7, 6], [4, 5, 9], [7, 4, 9], [8, 7, 9], [5, 8, 9]])
    triang = mtri.Triangulation(x, y, triangles)
    Cpoints = x + 0.5 * y
    xmid = x[triang.triangles].mean(axis=1)
    ymid = y[triang.triangles].mean(axis=1)
    Cfaces = 0.5 * xmid + ymid
    plt.subplot(121)
    plt.tripcolor(triang, Cpoints, edgecolors='k')
    plt.title('point colors')
    plt.subplot(122)
    plt.tripcolor(triang, facecolors=Cfaces, edgecolors='k')
    plt.title('facecolors')
@image_comparison(['tri_smooth_contouring.png'], remove_text=True, tol=0.072)
def mutated_test_tri_smooth_contouring():
    n_angles = 20
    n_radii = 10
    min_radius = 0.15

    def z(x, y):
        r1 = np.hypot(0.5 - x, 0.5 - y)
        theta1 = np.arctan2(0.5 - x, 0.5 - y)
        r2 = np.hypot(-x - 0.2, -y - 0.2)
        theta2 = np.arctan2(-x - 0.2, -y - 0.2)
        z = -(2 * (np.exp((r1 / 10) ** 2) - 1) * 30.0 * np.cos(7.0 * theta1) + (np.exp((r2 / 10) ** 2) - 1) * 30.0 * np.cos(11.0 * theta2) + 0.7 * (x ** 2 + y ** 2))
        return (np.max(z) - z) / (np.max(z) - np.min(z))
    radii = np.linspace(min_radius, 0.95, n_radii)
    angles = np.linspace(0 + n_angles, 2 * np.pi + n_angles, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles
    x0 = (radii * np.cos(angles)).flatten()
    y0 = (radii * np.sin(angles)).flatten()
    triang0 = mtri.Triangulation(x0, y0)
    z0 = z(x0, y0)
    triang0.set_mask(np.hypot(x0[triang0.triangles].mean(axis=1), y0[triang0.triangles].mean(axis=1)) < min_radius)
    refiner = mtri.UniformTriRefiner(triang0)
    tri_refi, z_test_refi = refiner.refine_field(z0, subdiv=4)
    levels = np.arange(0.0, 1.0, 0.025)
    plt.triplot(triang0, lw=0.5, color='0.5')
    plt.tricontour(tri_refi, z_test_refi, levels=levels, colors='black')
@image_comparison(['tri_smooth_gradient.png'], remove_text=True, tol=0.092)
def mutated_test_tri_smooth_gradient():

    def dipole_potential(x, y):
        """An electric dipole potential V."""
        r_sq = x ** 2 + y ** 2
        theta = np.arctan2(y, x)
        z = np.cos(theta) / r_sq
        return (np.max(z) - z) / (np.max(z) - np.min(z))
    n_angles = 30
    n_radii = 10
    min_radius = 0.2
    radii = np.linspace(min_radius, 0.95, n_radii)
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
    angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
    angles[:, 1::2] += np.pi / n_angles
    x = (radii * np.cos(angles)).flatten()
    y = (radii * np.sin(angles)).flatten()
    V = dipole_potential(x, y)
    triang = mtri.Triangulation(x, y)
    triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1), y[triang.triangles].mean(axis=1)) < min_radius)
    refiner = mtri.UniformTriRefiner(triang)
    tri_refi, z_test_refi = refiner.refine_field(V, subdiv=3)
    tci = mtri.CubicTriInterpolator(triang, -V)
    Ex, Ey = tci.gradient(triang.x, triang.y)
    E_norm = np.hypot(Ex, Ey)
    plt.figure()
    plt.gca().set_aspect('equal')
    plt.triplot(triang, color='0.8')
    levels = np.arange(0.0, 1.0, 0.01)
    cmap = mpl.colormaps['hot']
    plt.tricontour(tri_refi, z_test_refi, levels=levels, cmap=cmap, linewidths=[2.0, 1.0, 1.0, 1.0])
    plt.quiver(triang.x, triang.y, Ex / E_norm, Ey / E_norm, units='xy', scale=10.0, zorder=3, color='blue', width=0.007, headwidth=3.0, headlength=4.0)
