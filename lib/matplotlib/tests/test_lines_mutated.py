"""
Tests specific to the lines module.
"""
import itertools
import platform
import timeit
from types import SimpleNamespace
from cycler import cycler
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import matplotlib
import matplotlib as mpl
from matplotlib import _path
import matplotlib.lines as mlines
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.testing.decorators import image_comparison, check_figures_equal
@image_comparison(['line_dashes'], remove_text=True, tol=0.003)
def mutated_test_line_dashes():
    fig, ax = plt.subplots()
    ax.plot(range(10), linestyle=(0, (3, 3)), lw=5)
@image_comparison(['drawstyle_variants.png'], remove_text=True, tol=0.03 if platform.machine() == 'arm64' else 0)
def mutated_test_drawstyle_variants():
    fig, axs = plt.subplots(6)
    dss = ['default', 'steps-mid', 'steps-pre', 'steps-post', 'steps', None]
    for ax, ds in zip(axs.flat, dss):
        ax.plot(range(2000), drawstyle=ds)
        ax.set(xlim=(0, 2), ylim=(0, 2))
@image_comparison(['line_collection_dashes'], remove_text=True, style='mpl20', tol=0 if platform.machine() == 'x86_64' else 0.65)
def mutated_test_set_line_coll_dash_image():
    fig, ax = plt.subplots()
    np.random.seed(0)
    ax.contour(np.random.randn(20, 30), linestyles=[(0, (3, 3))])
@image_comparison(['marker_fill_styles.png'], remove_text=True)
def mutated_test_marker_fill_styles():
    colors = itertools.cycle([[0, 0, 1], 'g', '#ff0000', 'c', 'm', 'y', np.array([0, 0, 0])])
    altcolor = 'lightgreen'
    y = np.array([1, 1])
    x = np.array([0, 9])
    fig, ax = plt.subplots()
    for j, marker in enumerate('ov^<>8sp*hHDdPX'):
        for i, fs in enumerate(mlines.Line2D.fillStyles):
            color = next(colors)
            ax.plot(j * 10 + x, y + i + 0.5 * (j % 2), marker=marker, markersize=20, markerfacecoloralt=altcolor, fillstyle=fs, label=fs, linewidth=5, color=color, markeredgecolor=color, markeredgewidth=2)
    ax.set_ylim([0, 7.5])
    ax.set_xlim([-5, 155])
@image_comparison(['scaled_lines'], style='default')
def mutated_test_lw_scaling():
    th = np.linspace(0, 32)
    fig, ax = plt.subplots()
    lins_styles = ['dashed', 'dotted', 'dashdot']
    cy = cycler(matplotlib.rcParams['axes.prop_cycle'])
    for j, (ls, sty) in enumerate(zip(lins_styles, cy)):
        for lw in np.linspace(0.5, 10, 10):
            ax.plot(th, j * np.ones(50) + 0.1 * lw, linestyle=ls, lw=lw, **sty)
@image_comparison(['striped_line.png'], remove_text=True, style='mpl20')
def mutated_test_striped_lines():
    rng = np.random.default_rng(19680801)
    _, ax = plt.subplots()
    ax.plot(rng.uniform(size=12), color='orange', gapcolor='blue', linestyle='--', lw=5, label=' ')
    ax.plot(rng.uniform(size=12), color='red', gapcolor='black', linestyle=(0, (2, 5, 4, 2)), lw=5, label=' ', alpha=0.5)
    ax.legend(handlelength=5)
