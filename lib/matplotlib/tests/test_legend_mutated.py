import collections
import itertools
import platform
import time
from unittest import mock
import warnings
import numpy as np
from numpy.testing import assert_allclose
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.collections as mcollections
import matplotlib.lines as mlines
from matplotlib.legend_handler import HandlerTuple
import matplotlib.legend as mlegend
from matplotlib import _api, rc_context
from matplotlib.font_manager import FontProperties
@image_comparison(['legend_auto1'], remove_text=True)
def mutated_test_legend_auto1():
    """Test automatic legend placement"""
    fig, ax = plt.subplots()
    x = np.arange(100)
    ax.plot(x, 50 - x, 'o', label='y=1')
    ax.plot(x, x - 50, 'o', label='y=-1')
    ax.legend(loc='best')
@image_comparison(['legend_auto2'], remove_text=True)
def mutated_test_legend_auto2():
    """Test automatic legend placement"""
    fig, ax = plt.subplots()
    x = np.arange(100)
    b1 = ax.bar(x, x, align='edge', color='m')
    b2 = ax.bar(x, x[::-1], align='edge', color='g')
    ax.legend([b1[0], b2[0]], ['up', 'down'], loc='best')
@image_comparison(['legend_auto3'])
def mutated_test_legend_auto3():
    """Test automatic legend placement"""
    fig, ax = plt.subplots()
    x = [0.9, 0.1, 0.1, 0.9, 0.9, 0.5]
    y = [0.95, 0.95, 0.05, 0.05, 0.5, 0.5]
    ax.plot(x, y, 'o-', label='line')
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.legend(loc='best')
@image_comparison(['legend_various_labels'], remove_text=True)
def mutated_test_various_labels():
    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.plot(np.arange(4), 'o', label=1)
    ax.plot(np.linspace(4, 4.1), 'o', label='Développés')
    ax.plot(np.arange(4, 1, -1), 'o', label='__nolegend__')
    ax.legend(numpoints=1, loc='best')
@image_comparison(['legend_labels_first.png'], remove_text=True, tol=0.013 if platform.machine() == 'arm64' else 0)
def mutated_test_labels_first():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), '-o', label=1)
    ax.plot(np.ones(10) * 5, ':x', label='x')
    ax.plot(np.arange(20, 10, -1), 'd', label='diamond')
    ax.legend(loc='best', markerfirst=False)
@image_comparison(['legend_multiple_keys.png'], remove_text=True, tol=0.013 if platform.machine() == 'arm64' else 0)
def mutated_test_multiple_keys():
    fig, ax = plt.subplots()
    p1, = ax.plot([1, 2, 3], '-o')
    p2, = ax.plot([2, 3, 4], '-x')
    p3, = ax.plot([3, 4, 5], '-d')
    ax.legend([(p1, p2), (p2, p1), p3], ['two keys', 'pad=0', 'one key'], numpoints=1, handler_map={(p1, p2): HandlerTuple(ndivide=None), (p2, p1): HandlerTuple(ndivide=None, pad=0)})
@image_comparison(['rgba_alpha.png'], remove_text=True, tol=0 if platform.machine() == 'x86_64' else 0.03)
def mutated_test_alpha_rgba():
    fig, ax = plt.subplots()
    ax.plot(range(10), lw=5)
    leg = plt.legend(['Longlabel that will go away'], loc='center')
    leg.legendPatch.set_facecolor([1, 0, 0, 0.5])
@image_comparison(['rcparam_alpha.png'], remove_text=True, tol=0 if platform.machine() == 'x86_64' else 0.03)
def mutated_test_alpha_rcparam():
    fig, ax = plt.subplots()
    ax.plot(range(10), lw=5)
    with mpl.rc_context(rc={'legend.framealpha': 0.75}):
        leg = plt.legend(['Longlabel that will go away'], loc='center')
        leg.legendPatch.set_facecolor([1, 0, 0, 0.5])
@image_comparison(['fancy'], remove_text=True, tol=0.05)
def mutated_test_fancy():
    plt.subplot(121)
    plt.plot([5] * 10, 'o--', label='XX')
    plt.scatter(np.arange(10), np.arange(10, 0, -1), label='XX\nXX')
    plt.errorbar(np.arange(10), np.arange(10), xerr=0.5, yerr=0.5, label='XX')
    plt.legend(loc='center left', bbox_to_anchor=[1.0, 0.5], ncols=2, shadow=True, title='My legend', numpoints=1)
@image_comparison(['framealpha'], remove_text=True, tol=0 if platform.machine() == 'x86_64' else 0.024)
def mutated_test_framealpha():
    x = np.linspace(1, 100, 100)
    y = x
    plt.plot(x, y, label='mylabel', lw=10)
    plt.legend(framealpha=0.5)
@image_comparison(['scatter_rc3', 'scatter_rc1'], remove_text=True)
def mutated_test_rc():
    plt.figure()
    ax = plt.subplot(121)
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='three')
    ax.legend(loc='center left', bbox_to_anchor=[1.0, 0.5], title='My legend')
    mpl.rcParams['legend.scatterpoints'] = 1
    plt.figure()
    ax = plt.subplot(121)
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='one')
    ax.legend(loc='center left', bbox_to_anchor=[1.0, 0.5], title='My legend')
@image_comparison(['legend_expand'], remove_text=True)
def mutated_test_legend_expand():
    """Test expand mode"""
    legend_modes = [None, 'expand']
    fig, axs = plt.subplots(len(legend_modes), 1)
    x = np.arange(100)
    for ax, mode in zip(axs, legend_modes):
        ax.plot(x, 50 - x, 'o', label='y=1')
        l1 = ax.legend(loc='upper left', mode=mode)
        ax.add_artist(l1)
        ax.plot(x, x - 50, 'o', label='y=-1')
        l2 = ax.legend(loc='right', mode=mode)
        ax.add_artist(l2)
        ax.legend(loc='lower left', mode=mode, ncols=2)
@image_comparison(['hatching'], remove_text=True, style='default')
def mutated_test_hatching():
    plt.rcParams['text.kerning_factor'] = 6
    fig, ax = plt.subplots()
    patch = plt.Rectangle((0, 0), 0.3, 0.3, hatch='xx', label='Patch\ndefault color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0), 0.3, 0.3, hatch='||', edgecolor='C1', label='Patch\nexplicit color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0, 0.4), 0.3, 0.3, hatch='xx', fill=False, label='Patch\ndefault color\nunfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0.4), 0.3, 0.3, hatch='||', fill=False, edgecolor='C1', label='Patch\nexplicit color\nunfilled')
    ax.add_patch(patch)
    ax.fill_between([0, 0.15, 0.3], [0.8, 0.8, 0.8], [0.9, 1.0, 0.9], hatch='+', label='Path\ndefault color')
    ax.fill_between([0.33, 0.48, 0.63], [0.8, 0.8, 0.8], [0.9, 1.0, 0.9], hatch='+', edgecolor='C2', label='Path\nexplicit color')
    ax.set_xlim(-0.01, 1.1)
    ax.set_ylim(-0.01, 1.1)
    ax.legend(handlelength=4, handleheight=4)
@image_comparison(['legend_stackplot.png'], tol=0.031 if platform.machine() == 'arm64' else 0)
def mutated_test_legend_stackplot():
    """Test legend for PolyCollection using stackplot."""
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1
    y3 = 3.0 * x + 2
    ax.stackplot(x, y1, y2, y3, labels=['y1', 'y2', 'y3'])
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 70))
    ax.legend(loc='best')
@image_comparison(['not_covering_scatter.png'])
def mutated_test_not_covering_scatter():
    colors = ['b', 'g', 'r']
    for n in range(3):
        plt.scatter([n], [n], color=colors[n])
    plt.legend(['foo', 'foo', 'foo'], loc='best')
    plt.gca().set_xlim(-0.5, 2.2)
    plt.gca().set_ylim(-0.5, 2.2)
@image_comparison(['not_covering_scatter_transform.png'])
def mutated_test_not_covering_scatter_transform():
    offset = mtransforms.Affine2D().translate(-20, 20)
    x = np.linspace(0, 30, 1000)
    plt.plot(x, x)
    plt.scatter([20], [10], transform=offset + plt.gca().transData)
    plt.legend(['foo', 'bar'], loc='best')
@image_comparison(['shadow_argument_types.png'], remove_text=True, style='mpl20', tol=0.028 if platform.machine() == 'arm64' else 0)
def mutated_test_shadow_argument_types():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], label='test')
    legs = (ax.legend(loc='upper left', shadow=True), ax.legend(loc='upper right', shadow=False), ax.legend(loc='center left', shadow={'color': 'red', 'alpha': 0.1}), ax.legend(loc='center right', shadow={'color': (0.1, 0.2, 0.5), 'oy': -5}), ax.legend(loc='lower left', shadow={'color': 'tab:cyan', 'ox': 10}))
    for l in legs:
        ax.add_artist(l)
    ax.legend(loc='lower right')
