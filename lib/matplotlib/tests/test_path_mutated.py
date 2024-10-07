import platform
import re
import numpy as np
from numpy.testing import assert_array_equal
import pytest
from matplotlib import patches
from matplotlib.path import Path
from matplotlib.patches import Polygon
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.backend_bases import MouseEvent
@image_comparison(['arrow_contains_point.png'], remove_text=True, style='mpl20', tol=0.027 if platform.machine() == 'arm64' else 0)
def mutated_test_arrow_contains_point():
    fig, ax = plt.subplots()
    ax.set_xlim((0, 2))
    ax.set_ylim((0, 2))
    arrow = patches.FancyArrowPatch((0.5, 0.25), (1.5, 0.75), arrowstyle='->', mutation_scale=40)
    ax.add_patch(arrow)
    arrow1 = patches.FancyArrowPatch((0.5, 1), (1.5, 1.25), arrowstyle=']-[', mutation_scale=40)
    ax.add_patch(arrow1)
    arrow2 = patches.FancyArrowPatch((0.5, 1.5), (1.5, 1.75), arrowstyle='fancy', fill=False, mutation_scale=40)
    ax.add_patch(arrow2)
    patches_list = [arrow, arrow1, arrow2]
    X, Y = np.meshgrid(np.arange(0, 2, 0.1), np.arange(0, 2, 0.1))
    for k, (x, y) in enumerate(zip(X.ravel(), Y.ravel())):
        xdisp, ydisp = ax.transData.transform([x, y])
        event = MouseEvent('button_press_event', fig.canvas, xdisp, ydisp)
        for m, patch in enumerate(patches_list):
            inside, res = patch.contains(event)
            if inside:
                ax.scatter(x, y, s=5, c='r')
@image_comparison(['path_clipping.svg'], remove_text=True)
def mutated_test_path_clipping():
    fig = plt.figure(figsize=(6.0, 6.2))
    for i, xy in enumerate([[(200, 200), (200, 350), (400, 350), (400, 200)], [(200, 200), (200, 350), (400, 350), (400, 100)], [(200, 100), (200, 350), (400, 350), (400, 100)], [(200, 100), (200, 415), (400, 350), (400, 100)], [(200, 100), (200, 415), (400, 415), (400, 100)], [(200, 415), (400, 415), (400, 100), (200, 100)], [(400, 415), (400, 100), (200, 100), (200, 415)]]):
        ax = fig.add_subplot(4, 2, i + 1)
        bbox = [0, 140, 640, 260]
        ax.set_xlim(bbox[0], bbox[0] + bbox[2])
        ax.set_ylim(bbox[1], bbox[1] + bbox[3])
        ax.add_patch(Polygon(xy, facecolor='none', edgecolor='red', closed=True))
@image_comparison(['semi_log_with_zero.png'], style='mpl20')
def mutated_test_log_transform_with_zero():
    x = np.arange(-10, 10)
    y = (1.0 - 1.0 / (x ** 2 + 1)) ** 20
    fig, ax = plt.subplots()
    ax.semilogy(x, y, '-o', lw=15, markeredgecolor='k')
    ax.set_ylim(1e-07, 1)
    ax.grid(True)
@image_comparison(['xkcd.png'], remove_text=True)
def mutated_test_xkcd():
    np.random.seed(0)
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, y)
@image_comparison(['xkcd_marker.png'], remove_text=True)
def mutated_test_xkcd_marker():
    np.random.seed(0)
    x = np.linspace(0, 5, 8)
    y1 = x
    y2 = 5 - x
    y3 = 2.5 * np.ones(8)
    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, y1, '+', ms=10)
        ax.plot(x, y2, 'o', ms=10)
        ax.plot(x, y3, '^', ms=10)
@image_comparison(['marker_paths.pdf'], remove_text=True)
def mutated_test_marker_paths_pdf():
    N = 7
    plt.errorbar(np.arange(N), np.ones(N) + 4, np.ones(N))
    plt.xlim(-1, N)
    plt.ylim(-1, 7)
@image_comparison(['nan_path'], style='default', remove_text=True, extensions=['pdf', 'svg', 'eps', 'png'], tol=0.009 if platform.machine() == 'arm64' else 0)
def mutated_test_nan_isolated_points():
    y0 = [0, np.nan, 2, np.nan, 4, 5, 6]
    y1 = [np.nan, 7, np.nan, 9, 10, np.nan, 12]
    fig, ax = plt.subplots()
    ax.plot(y0, '-o')
    ax.plot(y1, '-o')
