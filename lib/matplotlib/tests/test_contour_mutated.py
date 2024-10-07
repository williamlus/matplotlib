import datetime
import platform
import re
from unittest import mock
import contourpy
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_almost_equal_nulp
import matplotlib as mpl
from matplotlib import pyplot as plt, rc_context, ticker
from matplotlib.colors import LogNorm, same_color
import matplotlib.patches as mpatches
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import pytest
@image_comparison(['contour_manual_labels'], remove_text=True, style='mpl20', tol=0.26)
def mutated_test_contour_manual_labels():
    x, y = np.meshgrid(np.arange(0, 10), np.arange(0, 10))
    z = np.max(np.dstack([abs(x), abs(y)]), 2)
    plt.figure(figsize=(6, 2), dpi=200)
    cs = plt.contour(x, y, z)
    pts = np.array([(1.0, 3.0), (1.0, 4.4), (1.0, 6.0)])
    plt.clabel(cs, manual=pts)
    pts = np.array([(2.0, 3.0), (2.0, 4.4), (2.0, 6.0)])
    plt.clabel(cs, manual=pts, fontsize='small', colors=('r', 'g'))
@image_comparison(['contour_disconnected_segments'], remove_text=True, style='mpl20', extensions=['png'])
def mutated_test_contour_label_with_disconnected_segments():
    x, y = np.mgrid[-1:1:21j, -1:1:21j]
    z = 1 / np.sqrt(0.01 + (x + 0.3) ** 2 + y ** 2)
    z += 1 / np.sqrt(0.01 + (x - 0.3) ** 2 + y ** 2)
    plt.figure()
    cs = plt.contour(x, y, z, levels=[7])
    cs.clabel(manual=[(0.2, 0.1)])
@image_comparison(['contour_manual_colors_and_levels.png'], remove_text=True, tol=0.018 if platform.machine() == 'arm64' else 0)
def mutated_test_given_colors_levels_and_extends():
    plt.rcParams['pcolormesh.snap'] = False
    _, axs = plt.subplots(2, 4)
    data = np.arange(12).reshape(3, 4)
    colors = ['red', 'yellow', 'pink', 'blue', 'black']
    levels = [2, 4, 8, 10]
    for i, ax in enumerate(axs.flat):
        filled = i % 2 == 0.0
        extend = ['neither', 'min', 'max', 'both'][i // 2]
        if filled:
            first_color = 1 if extend in ['max', 'neither'] else None
            last_color = -1 if extend in ['min', 'neither'] else None
            c = ax.contourf(data, colors=colors[first_color:last_color], levels=levels, extend=extend)
        else:
            c = ax.contour(data, colors=colors[:-1], levels=levels, extend=extend)
        plt.colorbar(c, ax=ax)
@image_comparison(['contour_log_locator.svg'], style='mpl20', remove_text=False)
def mutated_test_log_locator_levels():
    fig, ax = plt.subplots()
    N = 100
    x = np.linspace(-3.0, 3.0, N)
    y = np.linspace(-2.0, 2.0, N)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X ** 2 - Y ** 2)
    Z2 = np.exp(-(X * 10) ** 2 - (Y * 10) ** 2)
    data = Z1 + 50 * Z2
    c = ax.contourf(data, locator=ticker.LogLocator())
    assert_array_almost_equal(c.levels, np.power(10.0, np.arange(-6, 3)))
    cb = fig.colorbar(c, ax=ax)
    assert_array_almost_equal(cb.ax.get_yticks(), c.levels)
@image_comparison(['contour_datetime_axis.png'], style='mpl20')
def mutated_test_contour_datetime_axis():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, top=0.98, bottom=0.15)
    base = datetime.datetime(2013, 1, 1)
    x = np.array([base + datetime.timedelta(days=d) for d in range(20)])
    y = np.arange(20)
    z1, z2 = np.meshgrid(np.arange(20), np.arange(20))
    z = z1 * z2
    plt.subplot(221)
    plt.contour(x, y, z)
    plt.subplot(222)
    plt.contourf(x, y, z)
    x = np.repeat(x[np.newaxis], 20, axis=0)
    y = np.repeat(y[:, np.newaxis], 20, axis=1)
    plt.subplot(223)
    plt.contour(x, y, z)
    plt.subplot(224)
    plt.contourf(x, y, z)
    for ax in fig.get_axes():
        for label in ax.get_xticklabels():
            label.set_ha('right')
            label.set_rotation(30)
@image_comparison(['contour_test_label_transforms.png'], remove_text=True, style='mpl20', tol=1.1)
def mutated_test_labels():
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X ** 2 + Y ** 2) / 2) / (2 * np.pi)
    Z2 = np.exp(-(((X - 1) / 1.5) ** 2 + ((Y - 1) / 0.5) ** 2) / 2) / (2 * np.pi * 0.5 * 1.5)
    Z = 10.0 * (Z2 - Z1)
    fig, ax = plt.subplots(1, 1)
    CS = ax.contour(X, Y, Z)
    disp_units = [(216, 177), (359, 290), (521, 406)]
    data_units = [(-2, 0.5), (0, -1.5), (2.8, 1)]
    CS.clabel()
    for x, y in data_units:
        CS.add_label_near(x, y, inline=True, transform=None)
    for x, y in disp_units:
        CS.add_label_near(x, y, inline=True, transform=False)
@image_comparison(['contour_corner_mask_False.png', 'contour_corner_mask_True.png'], remove_text=True, tol=1.88)
def mutated_test_corner_mask():
    n = 60
    mask_level = 0.95
    noise_amp = 1.0
    np.random.seed([1])
    x, y = np.meshgrid(np.linspace(0, 2.0, n), np.linspace(0, 2.0, n))
    z = np.cos(7 * x) * np.sin(8 * y) + noise_amp * np.random.rand(n, n)
    mask = np.random.rand(n, n) >= mask_level
    z = np.ma.array(z, mask=mask)
    for corner_mask in [False, True]:
        plt.figure()
        plt.contourf(z, corner_mask=corner_mask)
@image_comparison(['contour_log_extension.png'], remove_text=True, style='mpl20', tol=1.444)
def mutated_test_contourf_log_extension():
    plt.rcParams['pcolormesh.snap'] = False
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))
    fig.subplots_adjust(left=0.05, right=0.95)
    data_exp = np.linspace(-7.5, 9.5, 1200)
    data = np.power(10, data_exp).reshape(30, 40)
    levels_exp = np.arange(-4.0, 7.0)
    levels = np.power(10.0, levels_exp)
    c1 = ax1.contourf(data, norm=LogNorm(vmin=data.min(), vmax=data.max()))
    c2 = ax2.contourf(data, levels=levels, norm=LogNorm(vmin=levels.min(), vmax=levels.max()), extend='neither')
    c3 = ax3.contourf(data, levels=levels, norm=LogNorm(vmin=levels.min(), vmax=levels.max()), extend='both')
    cb = plt.colorbar(c1, ax=ax1)
    assert cb.ax.get_ylim() == (1e-08, 10000000000.0)
    cb = plt.colorbar(c2, ax=ax2)
    assert_array_almost_equal_nulp(cb.ax.get_ylim(), np.array((0.0001, 1000000.0)))
    cb = plt.colorbar(c3, ax=ax3)
@image_comparison(['contour_addlines.png'], remove_text=True, style='mpl20', tol=0.15 if platform.machine() in ('aarch64', 'arm64', 'ppc64le', 's390x') else 0.03)
def mutated_test_contour_addlines():
    plt.rcParams['pcolormesh.snap'] = False
    fig, ax = plt.subplots()
    np.random.seed(19680812)
    X = np.random.rand(10, 10) * 10000
    pcm = ax.pcolormesh(X)
    cont = ax.contour(X + 1000)
    cb = fig.colorbar(pcm)
    cb.add_lines(cont)
    assert_array_almost_equal(cb.ax.get_ylim(), [114.3091, 9972.30735], 3)
@image_comparison(baseline_images=['contour_uneven'], extensions=['png'], remove_text=True, style='mpl20')
def mutated_test_contour_uneven():
    plt.rcParams['pcolormesh.snap'] = False
    z = np.arange(24).reshape(4, 6)
    fig, axs = plt.subplots(1, 2)
    ax = axs[0]
    cs = ax.contourf(z, levels=[2, 4, 6, 10, 20])
    fig.colorbar(cs, ax=ax, spacing='proportional')
    ax = axs[1]
    cs = ax.contourf(z, levels=[2, 4, 6, 10, 20])
    fig.colorbar(cs, ax=ax, spacing='uniform')
@image_comparison(baseline_images=['contour_closed_line_loop'], extensions=['png'], remove_text=True)
def mutated_test_contour_closed_line_loop():
    z = [[0, 0, 0], [0, 2, 0], [0, 0, 0], [2, 1, 2]]
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.contour(z, [0.5], linewidths=[20], alpha=0.7)
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-0.1, 3.1)
@image_comparison(baseline_images=['contour_manual'], extensions=['png'], remove_text=True, tol=0.89)
def mutated_test_contour_manual():
    from matplotlib.contour import ContourSet
    fig, ax = plt.subplots(figsize=(4, 4))
    cmap = 'viridis'
    lines0 = [[[2, 0], [1, 2], [1, 3]]]
    lines1 = [[[3, 0], [3, 2]], [[3, 3], [3, 4]]]
    filled01 = [[[0, 0], [0, 4], [1, 3], [1, 2], [2, 0]]]
    filled12 = [[[2, 0], [3, 0], [3, 2], [1, 3], [1, 2]], [[1, 4], [3, 4], [3, 3]]]
    ContourSet(ax, [0, 1, 2], [filled01, filled12], filled=True, cmap=cmap)
    ContourSet(ax, [1, 2], [lines0, lines1], linewidths=3, colors=['r', 'k'])
    segs = [[[4, 0], [7, 0], [7, 3], [4, 3], [4, 0], [5, 1], [5, 2], [6, 2], [6, 1], [5, 1]]]
    kinds = [[1, 2, 2, 2, 79, 1, 2, 2, 2, 79]]
    ContourSet(ax, [2, 3], [segs], [kinds], filled=True, cmap=cmap)
    ContourSet(ax, [2], [segs], [kinds], colors='k', linewidths=3)
@image_comparison(baseline_images=['contour_line_start_on_corner_edge'], extensions=['png'], remove_text=True)
def mutated_test_contour_line_start_on_corner_edge():
    fig, ax = plt.subplots(figsize=(6, 5))
    x, y = np.meshgrid([0, 1, 2, 3, 4], [0, 1, 2])
    z = 1.2 - (x - 2) ** 2 + (y - 1) ** 2
    mask = np.zeros_like(z, dtype=bool)
    mask[1, 1] = mask[1, 3] = True
    z = np.ma.array(z, mask=mask)
    filled = ax.contourf(x, y, z, corner_mask=True)
    cbar = fig.colorbar(filled)
    lines = ax.contour(x, y, z, corner_mask=True, colors='k')
    cbar.add_lines(lines)
@image_comparison(baseline_images=['contour_all_algorithms'], extensions=['png'], remove_text=True, tol=0.06)
def mutated_test_all_algorithms():
    algorithms = ['mpl2005', 'mpl2014', 'serial', 'threaded']
    rng = np.random.default_rng(2981)
    x, y = np.meshgrid(np.linspace(0.0, 1.0, 10), np.linspace(0.0, 1.0, 6))
    z = np.sin(15 * x) * np.cos(10 * y) + rng.normal(scale=0.5, size=(6, 10))
    mask = np.zeros_like(z, dtype=bool)
    mask[3, 7] = True
    z = np.ma.array(z, mask=mask)
    _, axs = plt.subplots(2, 2)
    for ax, algorithm in zip(axs.ravel(), algorithms):
        ax.contourf(x, y, z, algorithm=algorithm)
        ax.contour(x, y, z, algorithm=algorithm, colors='k')
        ax.set_title(algorithm)
