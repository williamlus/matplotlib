import contextlib
from collections import namedtuple
import datetime
from decimal import Decimal
from functools import partial
import inspect
import io
from itertools import product
import platform
from types import SimpleNamespace
import dateutil.tz
import numpy as np
from numpy import ma
from cycler import cycler
import pytest
import matplotlib
import matplotlib as mpl
from matplotlib import rc_context, patheffects
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.font_manager as mfont_manager
import matplotlib.markers as mmarkers
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib.projections.geo import HammerAxes
from matplotlib.projections.polar import PolarAxes
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import mpl_toolkits.axisartist as AA
from numpy.testing import assert_allclose, assert_array_equal, assert_array_almost_equal
from matplotlib.testing.decorators import image_comparison, check_figures_equal, remove_ticks_and_titles
from matplotlib.testing._markers import needs_usetex

def contour_dat():
    x = np.linspace(-3, 5, 150)
    y = np.linspace(-3, 5, 120)
    z = np.cos(x) + np.sin(y[:, np.newaxis])
    return (x, y, z)

def _params(c=None, xsize=2, *, edgecolors=None, **kwargs):
    return (c, edgecolors, kwargs if kwargs is not None else {}, xsize)
_result = namedtuple('_result', 'c, colors')
del _params
del _result

def _bxp_test_helper(stats_kwargs={}, transform_stats=lambda s: s, bxp_kwargs={}):
    np.random.seed(937)
    logstats = mpl.cbook.boxplot_stats(np.random.lognormal(mean=1.25, sigma=1.0, size=(37, 4)), **stats_kwargs)
    fig, ax = plt.subplots()
    if bxp_kwargs.get('orientation', 'vertical') == 'vertical':
        ax.set_yscale('log')
    else:
        ax.set_xscale('log')
    if not bxp_kwargs.get('patch_artist', False):
        mpl.rcParams['boxplot.boxprops.linewidth'] = mpl.rcParams['lines.linewidth']
    ax.bxp(transform_stats(logstats), **bxp_kwargs)

def _rc_test_bxp_helper(ax, rc_dict):
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    with matplotlib.rc_context(rc_dict):
        ax.boxplot([x, x])
    return ax

def generate_errorbar_inputs():
    base_xy = cycler('x', [np.arange(5)]) + cycler('y', [np.ones(5)])
    err_cycler = cycler('err', [1, [1, 1, 1, 1, 1], [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], np.ones(5), np.ones((2, 5)), None])
    xerr_cy = cycler('xerr', err_cycler)
    yerr_cy = cycler('yerr', err_cycler)
    empty = (cycler('x', [[]]) + cycler('y', [[]])) * cycler('xerr', [[], None]) * cycler('yerr', [[], None])
    xerr_only = base_xy * xerr_cy
    yerr_only = base_xy * yerr_cy
    both_err = base_xy * yerr_cy * xerr_cy
    return [*xerr_only, *yerr_only, *both_err, *empty]

@pytest.fixture(params=['x', 'y'])
def shared_axis_remover(request):

    def _helper_x(ax):
        ax2 = ax.twinx()
        ax2.remove()
        ax.set_xlim(0, 15)
        r = ax.xaxis.get_major_locator()()
        assert r[-1] > 14

    def _helper_y(ax):
        ax2 = ax.twiny()
        ax2.remove()
        ax.set_ylim(0, 15)
        r = ax.yaxis.get_major_locator()()
        assert r[-1] > 14
    return {'x': _helper_x, 'y': _helper_y}[request.param]

@pytest.fixture(params=['gca', 'subplots', 'subplots_shared', 'add_axes'])
def shared_axes_generator(request):
    if request.param == 'gca':
        fig = plt.figure()
        ax = fig.gca()
    elif request.param == 'subplots':
        fig, ax = plt.subplots()
    elif request.param == 'subplots_shared':
        fig, ax_lst = plt.subplots(2, 2, sharex='all', sharey='all')
        ax = ax_lst[0][0]
    elif request.param == 'add_axes':
        fig = plt.figure()
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    return (fig, ax)

class _Translation(mtransforms.Transform):
    input_dims = 1
    output_dims = 1

    def __init__(self, dx):
        self.dx = dx

    def transform(self, values):
        return values + self.dx

    def inverted(self):
        return _Translation(-self.dx)

def color_boxes(fig, ax):
    """
    Helper for the tests below that test the extents of various Axes elements
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bbaxis = []
    for nn, axx in enumerate([ax.xaxis, ax.yaxis]):
        bb = axx.get_tightbbox(renderer)
        if bb:
            axisr = mpatches.Rectangle((bb.x0, bb.y0), width=bb.width, height=bb.height, linewidth=0.7, edgecolor='y', facecolor='none', transform=None, zorder=3)
            fig.add_artist(axisr)
        bbaxis += [bb]
    bbspines = []
    for nn, a in enumerate(['bottom', 'top', 'left', 'right']):
        bb = ax.spines[a].get_window_extent(renderer)
        spiner = mpatches.Rectangle((bb.x0, bb.y0), width=bb.width, height=bb.height, linewidth=0.7, edgecolor='green', facecolor='none', transform=None, zorder=3)
        fig.add_artist(spiner)
        bbspines += [bb]
    bb = ax.get_window_extent()
    rect2 = mpatches.Rectangle((bb.x0, bb.y0), width=bb.width, height=bb.height, linewidth=1.5, edgecolor='magenta', facecolor='none', transform=None, zorder=2)
    fig.add_artist(rect2)
    bbax = bb
    bb2 = ax.get_tightbbox(renderer)
    rect2 = mpatches.Rectangle((bb2.x0, bb2.y0), width=bb2.width, height=bb2.height, linewidth=3, edgecolor='red', facecolor='none', transform=None, zorder=1)
    fig.add_artist(rect2)
    bbtb = bb2
    return (bbaxis, bbspines, bbax, bbtb)

def test_specgram_11_mutated():
    """Test axes.specgram in default (psd) mode."""
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    n = 1000
    Fs = 10.0
    fstims = [[Fs / 4, Fs / 5, Fs / 11], [Fs / 4.7, Fs / 5.6, Fs / 11.9]]
    NFFT_freqs = int(10 * Fs / np.min(fstims))
    x = np.arange(0, n, 1 / Fs)
    y_freqs = np.concatenate(np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1))
    NFFT_noise = int(10 * Fs / 11)
    np.random.seed(0)
    y_noise = np.concatenate([np.random.standard_normal(n), np.random.rand(n)])
    all_sides = ['default', 'onesided', 'twosided']
    for y, NFFT in [(y_freqs, NFFT_freqs), (y_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides)
        for ax, sides in zip(plt.figure(layout='tight').subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, scale='linear', norm=matplotlib.colors.LogNorm())