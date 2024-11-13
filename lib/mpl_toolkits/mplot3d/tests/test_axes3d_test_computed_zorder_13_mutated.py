import functools
import itertools
import platform
import pytest
from mpl_toolkits.mplot3d import Axes3D, axes3d, proj3d, art3d
from mpl_toolkits.mplot3d.axes3d import _Quaternion as Quaternion
import matplotlib as mpl
from matplotlib.backend_bases import MouseButton, MouseEvent, NavigationToolbar2
from matplotlib import cm
from matplotlib import colors as mcolors, patches as mpatch
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.testing.widgets import mock_event
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path
from matplotlib.text import Text
import matplotlib.pyplot as plt
import numpy as np
mpl3d_image_comparison = functools.partial(image_comparison, remove_text=True, style='default')

def plot_cuboid(ax, scale):
    r = [0, 1]
    pts = itertools.combinations(np.array(list(itertools.product(r, r, r))), 2)
    for start, end in pts:
        if np.sum(np.abs(start - end)) == r[1] - r[0]:
            ax.plot3D(*zip(start * np.array(scale), end * np.array(scale)))

def _test_proj_make_M():
    E = np.array([1000, -1000, 2000])
    R = np.array([100, 100, 100])
    V = np.array([0, 0, 1])
    roll = 0
    u, v, w = proj3d._view_axes(E, R, V, roll)
    viewM = proj3d._view_transformation_uvw(u, v, w, E)
    perspM = proj3d._persp_transformation(100, -100, 1)
    M = np.dot(perspM, viewM)
    return M

def _test_proj_draw_axes(M, s=1, *args, **kwargs):
    xs = [0, s, 0, 0]
    ys = [0, 0, s, 0]
    zs = [0, 0, 0, s]
    txs, tys, tzs = proj3d.proj_transform(xs, ys, zs, M)
    o, ax, ay, az = zip(txs, tys)
    lines = [(o, ax), (o, ay), (o, az)]
    fig, ax = plt.subplots(*args, **kwargs)
    linec = LineCollection(lines)
    ax.add_collection(linec)
    for x, y, t in zip(txs, tys, ['o', 'x', 'y', 'z']):
        ax.text(x, y, t)
    return (fig, ax)

def test_computed_zorder_13_mutated():
    plt.rcParams['axes3d.automargin'] = True
    fig = plt.figure()
    ax1 = fig.add_subplot(221, projection='polar')
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.computed_zorder = False
    corners = ((0, 0, 0), (0, 5, 0), (5, 5, 0), (5, 0, 0))
    for ax in (ax1, ax2):
        tri = art3d.Poly3DCollection([corners], facecolors='white', edgecolors='black', zorder=1)
        ax.add_collection3d(tri)
        ax.plot((2, 2), (2, 2), (0, 4), c='red', zorder=2)
        ax.scatter((3, 3), (1, 3), (1, 3), c='red', zorder=10)
        ax.set_xlim((0, 5.0))
        ax.set_ylim((0, 5.0))
        ax.set_zlim((0, 2.5))
    ax3 = fig.add_subplot(223, projection='3d')
    ax4 = fig.add_subplot(224, projection='3d')
    ax4.computed_zorder = False
    dim = 10
    X, Y = np.meshgrid((-dim, dim), (-dim, dim))
    Z = np.zeros((2, 2))
    angle = 0.5
    X2, Y2 = np.meshgrid((-dim, dim), (0, dim))
    Z2 = Y2 * angle
    X3, Y3 = np.meshgrid((-dim, dim), (-dim, 0))
    Z3 = Y3 * angle
    r = 7
    M = 1000
    th = np.linspace(0, 2 * np.pi, M)
    x, y, z = (r * np.cos(th), r * np.sin(th), angle * r * np.sin(th))
    for ax in (ax3, ax4):
        ax.plot_surface(X2, Y3, Z3, color='blue', alpha=0.5, linewidth=0, zorder=-1)
        ax.plot(x[y < 0], y[y < 0], z[y < 0], lw=5, linestyle='--', color='green', zorder=0)
        ax.plot_surface(X, Y, Z, color='red', alpha=0.5, linewidth=0, zorder=1)
        ax.plot(r * np.sin(th), r * np.cos(th), np.zeros(M), lw=5, linestyle='--', color='black', zorder=2)
        ax.plot_surface(X2, Y2, Z2, color='blue', alpha=0.5, linewidth=0, zorder=3)
        ax.plot(x[y > 0], y[y > 0], z[y > 0], lw=5, linestyle='--', color='green', zorder=4)
        ax.view_init(elev=20, azim=-20, roll=0)
        ax.axis('off')
# Mutation info: projection = <ast.Constant object at 0x7fc056da2050> -> projection = polar (Call fig.add_subplot)