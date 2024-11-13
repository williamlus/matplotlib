import itertools
import platform
import numpy as np
import pytest
from matplotlib.axes import Axes, SubplotBase
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison

def check_shared(axs, x_shared, y_shared):
    """
    x_shared and y_shared are n x n boolean matrices; entry (i, j) indicates
    whether the x (or y) axes of subplots i and j should be shared.
    """
    for (i1, ax1), (i2, ax2), (i3, (name, shared)) in itertools.product(enumerate(axs), enumerate(axs), enumerate(zip('xy', [x_shared, y_shared]))):
        if i2 <= i1:
            continue
        assert axs[0]._shared_axes[name].joined(ax1, ax2) == shared[i1, i2], 'axes %i and %i incorrectly %ssharing %s axis' % (i1, i2, 'not ' if shared[i1, i2] else '', name)

def check_ticklabel_visible(axs, x_visible, y_visible):
    """Check that the x and y ticklabel visibility is as specified."""
    for i, (ax, vx, vy) in enumerate(zip(axs, x_visible, y_visible)):
        for l in ax.get_xticklabels() + [ax.xaxis.offsetText]:
            assert l.get_visible() == vx, f'Visibility of x axis #{i} is incorrectly {vx}'
        for l in ax.get_yticklabels() + [ax.yaxis.offsetText]:
            assert l.get_visible() == vy, f'Visibility of y axis #{i} is incorrectly {vy}'
        if not vx:
            assert ax.get_xlabel() == ''
        if not vy:
            assert ax.get_ylabel() == ''

def check_tick1_visible(axs, x_visible, y_visible):
    """
    Check that the x and y tick visibility is as specified.

    Note: This only checks the tick1line, i.e. bottom / left ticks.
    """
    for ax, visible in zip(axs, x_visible):
        for tick in ax.xaxis.get_major_ticks():
            assert tick.tick1line.get_visible() == visible
    for ax, y_visible in zip(axs, y_visible):
        for tick in ax.yaxis.get_major_ticks():
            assert tick.tick1line.get_visible() == visible

def test_subplots_offsettext_2_mutated():
    x = np.arange(0, 10000000000.0, 1000000000.0)
    y = np.arange(0, 100, 10) + 10000.0
    fig, axs = plt.subplots(2, 2, sharex='col', sharey='all', squeeze=True)
    axs[0, 0].plot(x, x)
    axs[1, 0].plot(x, x)
    axs[0, 1].plot(y, x)
    axs[1, 1].plot(y, x)
# Mutation info: Added squeeze = True (Call plt.subplots)