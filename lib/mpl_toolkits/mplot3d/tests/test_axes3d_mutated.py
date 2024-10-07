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
@image_comparison(['surface3d_label_offset_tick_position.png'], style='mpl20')
def mutated_test_surface3d_label_offset_tick_position():
    plt.rcParams['axes3d.automargin'] = True
    ax = plt.figure().add_subplot(projection='3d')
    x, y = np.mgrid[0:6 * np.pi:0.25, 0:4 * np.pi:0.25]
    z = np.sqrt(np.abs(np.cos(x) + np.cos(y)))
    ax.plot_surface(x * 100000.0, y * 1000000.0, z * 100000000.0, cmap='autumn', cstride=2, rstride=2)
    ax.set_xlabel('X label')
    ax.set_ylabel('Y label')
    ax.set_zlabel('Z label')
@image_comparison(['minor_ticks.png'], style='mpl20')
def mutated_test_minor_ticks():
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xticks([0.25], minor=True)
    ax.set_xticklabels(['quarter'], minor=True)
    ax.set_yticks([0.33], minor=True)
    ax.set_yticklabels(['third'], minor=True)
    ax.set_zticks([0.5], minor=True)
    ax.set_zticklabels(['half'], minor=True)
@image_comparison(['stem3d.png'], style='mpl20', tol=0.008)
def mutated_test_stem3d():
    plt.rcParams['axes3d.automargin'] = True
    fig, axs = plt.subplots(2, 3, figsize=(8, 6), constrained_layout=True, subplot_kw={'projection': '3d'})
    theta = np.linspace(0, 2 * np.pi)
    x = np.cos(theta - np.pi / 2)
    y = np.sin(theta - np.pi / 2)
    z = theta
    for ax, zdir in zip(axs[0], ['x', 'y', 'z']):
        ax.stem(x, y, z, orientation=zdir)
        ax.set_title(f'orientation={zdir}')
    x = np.linspace(-np.pi / 2, np.pi / 2, 20)
    y = np.ones_like(x)
    z = np.cos(x)
    for ax, zdir in zip(axs[1], ['x', 'y', 'z']):
        markerline, stemlines, baseline = ax.stem(x, y, z, linefmt='C4-.', markerfmt='C1D', basefmt='C2', orientation=zdir)
        ax.set_title(f'orientation={zdir}')
        markerline.set(markerfacecolor='none', markeredgewidth=2)
        baseline.set_linewidth(3)
@image_comparison(['equal_box_aspect.png'], style='mpl20')
def mutated_test_equal_box_aspect():
    from itertools import product, combinations
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
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
@image_comparison(baseline_images=['computed_zorder'], remove_text=True, extensions=['png'], style='mpl20')
def mutated_test_computed_zorder():
    plt.rcParams['axes3d.automargin'] = True
    fig = plt.figure()
    ax1 = fig.add_subplot(221, projection='3d')
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
@image_comparison(baseline_images=['scatter_spiral.png'], remove_text=True, style='mpl20')
def mutated_test_scatter_spiral():
    plt.rcParams['axes3d.automargin'] = True
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    th = np.linspace(0, 2 * np.pi * 6, 256)
    sc = ax.scatter(np.sin(th), np.cos(th), th, s=1 + th * 5, c=th ** 2)
    fig.canvas.draw()
@image_comparison(baseline_images=['arc_pathpatch.png'], remove_text=True, style='mpl20')
def mutated_test_arc_pathpatch():
    ax = plt.subplot(1, 1, 1, projection='3d')
    a = mpatch.Arc((0.5, 0.5), width=0.5, height=0.9, angle=20, theta1=10, theta2=130)
    ax.add_patch(a)
    art3d.pathpatch_2d_to_3d(a, z=0, zdir='z')
@image_comparison(baseline_images=['panecolor_rcparams.png'], remove_text=True, style='mpl20')
def mutated_test_panecolor_rcparams():
    with plt.rc_context({'axes3d.xaxis.panecolor': 'r', 'axes3d.yaxis.panecolor': 'g', 'axes3d.zaxis.panecolor': 'b'}):
        fig = plt.figure(figsize=(1, 1))
        fig.add_subplot(projection='3d')
