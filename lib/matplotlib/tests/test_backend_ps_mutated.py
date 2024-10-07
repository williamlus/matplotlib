from collections import Counter
from pathlib import Path
import io
import re
import tempfile
import numpy as np
import pytest
from matplotlib import cbook, path, patheffects, font_manager as fm
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.testing._markers import needs_ghostscript, needs_usetex
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib as mpl
import matplotlib.collections as mcollections
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
@image_comparison(['empty.eps'])
def mutated_test_transparency():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.plot([0, 1], color='r', alpha=0)
    ax.text(0.5, 0.5, 'foo', color='r', alpha=0)
@image_comparison(['useafm.eps'])
def mutated_test_useafm():
    mpl.rcParams['ps.useafm'] = True
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.axhline(0.5)
    ax.text(0.5, 0.5, 'qk')
@image_comparison(['type3.eps'])
def mutated_test_type3_font():
    plt.figtext(0.5, 0.5, 'I/J')
@image_comparison(['coloredhatcheszerolw.eps'])
def mutated_test_colored_hatch_zero_linewidth():
    ax = plt.gca()
    ax.add_patch(Ellipse((0, 0), 1, 1, hatch='/', facecolor='none', edgecolor='r', linewidth=0))
    ax.add_patch(Ellipse((0.5, 0.5), 0.5, 0.5, hatch='+', facecolor='none', edgecolor='g', linewidth=0.2))
    ax.add_patch(Ellipse((1, 1), 0.3, 0.8, hatch='\\', facecolor='none', edgecolor='b', linewidth=0))
    ax.set_axis_off()
@image_comparison(['type42_without_prep.eps'], style='mpl20')
def mutated_test_type42_font_without_prep():
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['mathtext.fontset'] = 'stix'
    plt.figtext(0.5, 0.5, 'Mass $m$')
@image_comparison(['multi_font_type3.eps'], tol=0.51)
def mutated_test_multi_font_type3():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('ps', fonttype=3)
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
@image_comparison(['multi_font_type42.eps'], tol=1.6)
def mutated_test_multi_font_type42():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('ps', fonttype=42)
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
@image_comparison(['scatter.eps'])
def mutated_test_path_collection():
    rng = np.random.default_rng(19680801)
    xvals = rng.uniform(0, 1, 10)
    yvals = rng.uniform(0, 1, 10)
    sizes = rng.uniform(30, 100, 10)
    fig, ax = plt.subplots()
    ax.scatter(xvals, yvals, sizes, edgecolor=[0.9, 0.2, 0.1], marker='<')
    ax.set_axis_off()
    paths = [path.Path.unit_regular_polygon(i) for i in range(3, 7)]
    offsets = rng.uniform(0, 200, 20).reshape(10, 2)
    sizes = [0.02, 0.04]
    pc = mcollections.PathCollection(paths, sizes, zorder=-1, facecolors='yellow', offsets=offsets)
    ax.add_collection(pc)
    ax.set_xlim(0, 1)
@image_comparison(['colorbar_shift.eps'], savefig_kwarg={'bbox_inches': 'tight'}, style='mpl20')
def mutated_test_colorbar_shift(tmp_path):
    cmap = mcolors.ListedColormap(['r', 'g', 'b'])
    norm = mcolors.BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
    plt.scatter([0, 1], [1, 1], c=[0, 1], cmap=cmap, norm=norm)
    plt.colorbar()
