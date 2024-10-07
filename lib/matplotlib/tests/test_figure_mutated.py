import copy
from datetime import datetime
import io
import pickle
import platform
from threading import Timer
from types import SimpleNamespace
import warnings
import numpy as np
import pytest
from PIL import Image
import matplotlib as mpl
from matplotlib import gridspec
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.axes import Axes
from matplotlib.backend_bases import KeyEvent, MouseEvent
from matplotlib.figure import Figure, FigureBase
from matplotlib.layout_engine import ConstrainedLayoutEngine, TightLayoutEngine, PlaceHolderLayoutEngine
from matplotlib.ticker import AutoMinorLocator, FixedFormatter, ScalarFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
@image_comparison(['figure_align_labels'], extensions=['png', 'svg'], tol=0 if platform.machine() == 'x86_64' else 0.01)
def mutated_test_align_labels():
    fig = plt.figure(layout='tight')
    gs = gridspec.GridSpec(3, 3)
    ax = fig.add_subplot(gs[0, :2])
    ax.plot(np.arange(0, 1000000.0, 1000))
    ax.set_ylabel('Ylabel0 0')
    ax = fig.add_subplot(gs[0, -1])
    ax.plot(np.arange(0, 10000.0, 100))
    for i in range(3):
        ax = fig.add_subplot(gs[1, i])
        ax.set_ylabel('YLabel1 %d' % i)
        ax.set_xlabel('XLabel1 %d' % i)
        if i in [0, 2]:
            ax.xaxis.set_label_position('top')
            ax.xaxis.tick_top()
        if i == 0:
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
        if i == 2:
            ax.yaxis.set_label_position('right')
            ax.yaxis.tick_right()
    for i in range(3):
        ax = fig.add_subplot(gs[2, i])
        ax.set_xlabel(f'XLabel2 {i}')
        ax.set_ylabel(f'YLabel2 {i}')
        if i == 2:
            ax.plot(np.arange(0, 10000.0, 10))
            ax.yaxis.set_label_position('right')
            ax.yaxis.tick_right()
            for tick in ax.get_xticklabels():
                tick.set_rotation(90)
    fig.align_labels()
@image_comparison(['figure_align_titles_tight.png', 'figure_align_titles_constrained.png'], tol=0 if platform.machine() == 'x86_64' else 0.022, style='mpl20')
def mutated_test_align_titles():
    for layout in ['tight', 'constrained']:
        fig, axs = plt.subplots(1, 2, layout=layout, width_ratios=[2, 1])
        ax = axs[0]
        ax.plot(np.arange(0, 1000000.0, 1000))
        ax.set_title('Title0 left', loc='left')
        ax.set_title('Title0 center', loc='center')
        ax.set_title('Title0 right', loc='right')
        ax = axs[1]
        ax.plot(np.arange(0, 10000.0, 100))
        ax.set_title('Title1')
        ax.set_xlabel('Xlabel0')
        ax.xaxis.set_label_position('top')
        ax.xaxis.tick_top()
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        fig.align_titles()
@image_comparison(['figure_today'], tol=0.015 if platform.machine() == 'arm64' else 0)
def mutated_test_figure():
    fig = plt.figure('today')
    ax = fig.add_subplot()
    ax.set_title(fig.get_label())
    ax.plot(np.arange(5))
    plt.figure('tomorrow')
    plt.plot([0, 1], [1, 0], 'r')
    plt.figure('today')
    plt.close('tomorrow')
@image_comparison(['figure_legend'])
def mutated_test_figure_legend():
    fig, axs = plt.subplots(2)
    axs[0].plot([0, 1], [1, 0], label='x', color='g')
    axs[0].plot([0, 1], [0, 1], label='y', color='r')
    axs[0].plot([0, 1], [0.5, 0.5], label='y', color='k')
    axs[1].plot([0, 1], [1, 0], label='_y', color='r')
    axs[1].plot([0, 1], [0, 1], label='z', color='b')
    fig.legend()
@image_comparison(['figure_suptitle'])
def mutated_test_suptitle():
    fig, _ = plt.subplots()
    fig.suptitle('hello', color='r')
    fig.suptitle('title', color='g', rotation=30)
@image_comparison(['alpha_background'], extensions=['png', 'svg'], savefig_kwarg={'facecolor': (0, 1, 0.4), 'edgecolor': 'none'})
def mutated_test_alpha():
    fig = plt.figure(figsize=[2, 1])
    fig.set_facecolor((0, 1, 0.4))
    fig.patch.set_alpha(0.4)
    fig.patches.append(mpl.patches.CirclePolygon([20, 20], radius=15, alpha=0.6, facecolor='red'))
@image_comparison(['tightbbox_box_aspect.svg'], style='mpl20', savefig_kwarg={'bbox_inches': 'tight', 'facecolor': 'teal'}, remove_text=True)
def mutated_test_tightbbox_box_aspect():
    fig = plt.figure()
    gs = fig.add_gridspec(1, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    ax1.set_box_aspect(0.5)
    ax2.set_box_aspect((2, 1, 1))
@image_comparison(['test_subfigure.png'], style='mpl20', savefig_kwarg={'facecolor': 'teal'})
def mutated_test_subfigure():
    np.random.seed(19680801)
    fig = plt.figure(layout='constrained')
    sub = fig.subfigures(1, 2)
    axs = sub[0].subplots(2, 2)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[0].colorbar(pc, ax=axs)
    sub[0].suptitle('Left Side')
    sub[0].set_facecolor('white')
    axs = sub[1].subplots(1, 3)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[1].colorbar(pc, ax=axs, location='bottom')
    sub[1].suptitle('Right Side')
    sub[1].set_facecolor('white')
    fig.suptitle('Figure suptitle', fontsize='xx-large')
    leg = fig.legend(handles=[plt.Line2D([0], [0], label='Line{}'.format(i)) for i in range(5)], loc='center')
    sub[0].set_zorder(leg.get_zorder() - 1)
    sub[1].set_zorder(leg.get_zorder() + 1)
@image_comparison(['test_subfigure_ss.png'], style='mpl20', savefig_kwarg={'facecolor': 'teal'}, tol=0.02)
def mutated_test_subfigure_ss():
    np.random.seed(19680801)
    fig = plt.figure(layout='constrained')
    gs = fig.add_gridspec(1, 2)
    sub = fig.add_subfigure(gs[0], facecolor='pink')
    axs = sub.subplots(2, 2)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub.colorbar(pc, ax=axs)
    sub.suptitle('Left Side')
    ax = fig.add_subplot(gs[1])
    ax.plot(np.arange(20))
    ax.set_title('Axes')
    fig.suptitle('Figure suptitle', fontsize='xx-large')
@image_comparison(['test_subfigure_double.png'], style='mpl20', savefig_kwarg={'facecolor': 'teal'})
def mutated_test_subfigure_double():
    np.random.seed(19680801)
    fig = plt.figure(layout='constrained', figsize=(10, 8))
    fig.suptitle('fig')
    subfigs = fig.subfigures(1, 2, wspace=0.07)
    subfigs[0].set_facecolor('coral')
    subfigs[0].suptitle('subfigs[0]')
    subfigs[1].set_facecolor('coral')
    subfigs[1].suptitle('subfigs[1]')
    subfigsnest = subfigs[0].subfigures(2, 1, height_ratios=[1, 1.4])
    subfigsnest[0].suptitle('subfigsnest[0]')
    subfigsnest[0].set_facecolor('r')
    axsnest0 = subfigsnest[0].subplots(1, 2, sharey=True)
    for ax in axsnest0:
        fontsize = 12
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2.5, vmax=2.5)
        ax.set_xlabel('x-label', fontsize=fontsize)
        ax.set_ylabel('y-label', fontsize=fontsize)
        ax.set_title('Title', fontsize=fontsize)
    subfigsnest[0].colorbar(pc, ax=axsnest0)
    subfigsnest[1].suptitle('subfigsnest[1]')
    subfigsnest[1].set_facecolor('g')
    axsnest1 = subfigsnest[1].subplots(3, 1, sharex=True)
    for nn, ax in enumerate(axsnest1):
        ax.set_ylabel(f'ylabel{nn}')
    subfigsnest[1].supxlabel('supxlabel')
    subfigsnest[1].supylabel('supylabel')
    axsRight = subfigs[1].subplots(2, 2)
@image_comparison(['test_subfigure_scatter_size.png'], style='mpl20', remove_text=True)
def mutated_test_subfigure_scatter_size():
    fig = plt.figure()
    gs = fig.add_gridspec(1, 2)
    ax0 = fig.add_subplot(gs[1])
    ax0.scatter([1, 2, 3], [1, 2, 3], s=30, marker='s')
    ax0.scatter([3, 4, 5], [1, 2, 3], s=[20, 30, 40], marker='s')
    sfig = fig.add_subfigure(gs[0])
    axs = sfig.subplots(1, 2)
    for ax in [ax0, axs[0]]:
        ax.scatter([1, 2, 3], [1, 2, 3], s=30, marker='s', color='r')
        ax.scatter([3, 4, 5], [1, 2, 3], s=[20, 30, 40], marker='s', color='g')
