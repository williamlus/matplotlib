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

@image_comparison(baseline_images=['panecolor_rcparams.png'], remove_text=True, style='mpl20')
def test_panecolor_rcparams_12_mutated():
    with plt.rc_context({'axes3d.xaxis.panecolor': 'r', 'axes3d.yaxis.panecolor': 'g', 'axes3d.zaxis.panecolor': 'b'}):
        fig = plt.figure(figsize=(1, 1))
        fig.add_subplot(projection='mollweide')
# Mutation info: projection = '3d' -> projection = mollweide (Call fig.add_subplot)