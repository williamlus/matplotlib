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

@image_comparison(['equal_box_aspect.png'], style='mpl20')
def test_equal_box_aspect_16_mutated():
    from itertools import product, combinations
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z)
    r = [-1, 1]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s - e)) == r[1] - r[0]:
            ax.plot3D(*zip(s, e), color='b')
    xyzlim = np.column_stack([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
    XYZlim = [min(xyzlim[0]), max(xyzlim[1])]
    ax.set_xlim3d(XYZlim)
    ax.set_ylim3d(XYZlim)
    ax.set_zlim3d(XYZlim)
    ax.axis('off')
    ax.set_box_aspect((1, 1, 1))
    with pytest.raises(ValueError, match='Argument zoom ='):
        ax.set_box_aspect((1, 1, 1), zoom=-1)
# Mutation info: projection = <ast.Constant object at 0x7fc31fa73750> -> projection = polar (Call fig.add_subplot)