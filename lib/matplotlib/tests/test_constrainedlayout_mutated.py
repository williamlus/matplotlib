import gc
import platform
import numpy as np
import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib import gridspec, ticker
@image_comparison(['constrained_layout1.png'])
def mutated_test_constrained_layout1():
    """Test constrained_layout for a single subplot"""
    fig = plt.figure(layout='constrained')
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)
@image_comparison(['constrained_layout2.png'])
def mutated_test_constrained_layout2():
    """Test constrained_layout for 2x2 subplots"""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        example_plot(ax, fontsize=24)
@image_comparison(['constrained_layout3.png'])
def mutated_test_constrained_layout3():
    """Test constrained_layout for colorbars with subplots"""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for nn, ax in enumerate(axs.flat):
        pcm = example_pcolor(ax, fontsize=24)
        if nn == 3:
            pad = 0.08
        else:
            pad = 0.02
        fig.colorbar(pcm, ax=ax, pad=pad)
@image_comparison(['constrained_layout4.png'])
def mutated_test_constrained_layout4():
    """Test constrained_layout for a single colorbar with subplots"""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)
@image_comparison(['constrained_layout5.png'], tol=0.002)
def mutated_test_constrained_layout5():
    """
    Test constrained_layout for a single colorbar with subplots,
    colorbar bottom
    """
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
    fig.colorbar(pcm, ax=axs, use_gridspec=False, pad=0.01, shrink=0.6, location='bottom')
@image_comparison(['constrained_layout6.png'], tol=0.002)
def mutated_test_constrained_layout6():
    """Test constrained_layout for nested gridspecs"""
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure(layout='constrained')
    gs = fig.add_gridspec(1, 2, figure=fig)
    gsl = gs[0].subgridspec(2, 2)
    gsr = gs[1].subgridspec(1, 2)
    axsl = []
    for gs in gsl:
        ax = fig.add_subplot(gs)
        axsl += [ax]
        example_plot(ax, fontsize=12)
    ax.set_xlabel('x-label\nMultiLine')
    axsr = []
    for gs in gsr:
        ax = fig.add_subplot(gs)
        axsr += [ax]
        pcm = example_pcolor(ax, fontsize=12)
    fig.colorbar(pcm, ax=axsr, pad=0.01, shrink=0.99, location='bottom', ticks=ticker.MaxNLocator(nbins=5))
@image_comparison(['constrained_layout8.png'])
def mutated_test_constrained_layout8():
    """Test for gridspecs that are not completely full"""
    fig = plt.figure(figsize=(10, 5), layout='constrained')
    gs = gridspec.GridSpec(3, 5, figure=fig)
    axs = []
    for j in [0, 1]:
        if j == 0:
            ilist = [1]
        else:
            ilist = [0, 4]
        for i in ilist:
            ax = fig.add_subplot(gs[j, i])
            axs += [ax]
            example_pcolor(ax, fontsize=9)
            if i > 0:
                ax.set_ylabel('')
            if j < 1:
                ax.set_xlabel('')
            ax.set_title('')
    ax = fig.add_subplot(gs[2, :])
    axs += [ax]
    pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)
@image_comparison(['constrained_layout9.png'])
def mutated_test_constrained_layout9():
    """Test for handling suptitle and for sharex and sharey"""
    fig, axs = plt.subplots(2, 2, layout='constrained', sharex=False, sharey=False)
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=24)
        ax.set_xlabel('')
        ax.set_ylabel('')
    ax.set_aspect(2.0)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)
    fig.suptitle('Test Suptitle', fontsize=28)
@image_comparison(['constrained_layout10.png'], tol=0.032 if platform.machine() == 'arm64' else 0)
def mutated_test_constrained_layout10():
    """Test for handling legend outside axis"""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        ax.plot(np.arange(12), label='This is a label')
    ax.legend(loc='center left', bbox_to_anchor=(0.8, 0.5))
@image_comparison(['constrained_layout11.png'])
def mutated_test_constrained_layout11():
    """Test for multiple nested gridspecs"""
    fig = plt.figure(layout='constrained', figsize=(13, 3))
    gs0 = gridspec.GridSpec(1, 2, figure=fig)
    gsl = gridspec.GridSpecFromSubplotSpec(1, 2, gs0[0])
    gsl0 = gridspec.GridSpecFromSubplotSpec(2, 2, gsl[1])
    ax = fig.add_subplot(gs0[1])
    example_plot(ax, fontsize=9)
    axs = []
    for gs in gsl0:
        ax = fig.add_subplot(gs)
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, shrink=0.6, aspect=70.0)
    ax = fig.add_subplot(gsl[0])
    example_plot(ax, fontsize=9)
@image_comparison(['constrained_layout11rat.png'])
def mutated_test_constrained_layout11rat():
    """Test for multiple nested gridspecs with width_ratios"""
    fig = plt.figure(layout='constrained', figsize=(10, 3))
    gs0 = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[6, 1])
    gsl = gridspec.GridSpecFromSubplotSpec(1, 2, gs0[0])
    gsl0 = gridspec.GridSpecFromSubplotSpec(2, 2, gsl[1], height_ratios=[2, 1])
    ax = fig.add_subplot(gs0[1])
    example_plot(ax, fontsize=9)
    axs = []
    for gs in gsl0:
        ax = fig.add_subplot(gs)
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, shrink=0.6, aspect=70.0)
    ax = fig.add_subplot(gsl[0])
    example_plot(ax, fontsize=9)
@image_comparison(['constrained_layout12.png'])
def mutated_test_constrained_layout12():
    """Test that very unbalanced labeling still works."""
    fig = plt.figure(layout='constrained', figsize=(6, 8))
    gs0 = gridspec.GridSpec(6, 2, figure=fig)
    ax1 = fig.add_subplot(gs0[:3, 1])
    ax2 = fig.add_subplot(gs0[3:, 1])
    example_plot(ax1, fontsize=18)
    example_plot(ax2, fontsize=18)
    ax = fig.add_subplot(gs0[0:2, 0])
    example_plot(ax, nodec=True)
    ax = fig.add_subplot(gs0[2:4, 0])
    example_plot(ax, nodec=True)
    ax = fig.add_subplot(gs0[4:, 0])
    example_plot(ax, nodec=True)
    ax.set_xlabel('x-label')
@image_comparison(['constrained_layout13.png'], tol=0.02)
def mutated_test_constrained_layout13():
    """Test that padding works."""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=12)
        fig.colorbar(pcm, ax=ax, shrink=0.6, aspect=20.0, pad=0.02)
    with pytest.raises(TypeError):
        fig.get_layout_engine().set(wpad=1, hpad=2)
    fig.get_layout_engine().set(w_pad=24.0 / 72.0, h_pad=24.0 / 72.0)
@image_comparison(['constrained_layout14.png'])
def mutated_test_constrained_layout14():
    """Test that padding works."""
    fig, axs = plt.subplots(2, 2, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax, fontsize=12)
        fig.colorbar(pcm, ax=ax, shrink=0.6, aspect=20.0, pad=0.02)
    fig.get_layout_engine().set(w_pad=3.0 / 72.0, h_pad=3.0 / 72.0, hspace=0.2, wspace=0.2)
@image_comparison(['constrained_layout15.png'])
def mutated_test_constrained_layout15():
    """Test that rcparams work."""
    mpl.rcParams['figure.constrained_layout.use'] = True
    fig, axs = plt.subplots(2, 2)
    for ax in axs.flat:
        example_plot(ax, fontsize=12)
@image_comparison(['constrained_layout16.png'])
def mutated_test_constrained_layout16():
    """Test ax.set_position."""
    fig, ax = plt.subplots(layout='constrained')
    example_plot(ax, fontsize=12)
    ax2 = fig.add_axes([0.2, 0.2, 0.4, 0.4])
@image_comparison(['constrained_layout17.png'])
def mutated_test_constrained_layout17():
    """Test uneven gridspecs"""
    fig = plt.figure(layout='constrained')
    gs = gridspec.GridSpec(3, 3, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1:])
    ax3 = fig.add_subplot(gs[1:, 0:2])
    ax4 = fig.add_subplot(gs[1:, -1])
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    example_plot(ax4)
@image_comparison(['test_colorbar_location.png'], remove_text=True, style='mpl20')
def mutated_test_colorbar_location():
    """
    Test that colorbar handling is as expected for various complicated
    cases...
    """
    plt.rcParams['pcolormesh.snap'] = False
    fig, axs = plt.subplots(4, 5, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax)
        ax.set_xlabel('')
        ax.set_ylabel('')
    fig.colorbar(pcm, ax=axs[:, 1], shrink=0.4)
    fig.colorbar(pcm, ax=axs[-1, :2], shrink=0.5, location='bottom')
    fig.colorbar(pcm, ax=axs[0, 2:], shrink=0.5, location='bottom', pad=0.05)
    fig.colorbar(pcm, ax=axs[-2, 3:], shrink=0.5, location='top')
    fig.colorbar(pcm, ax=axs[0, 0], shrink=0.5, location='left')
    fig.colorbar(pcm, ax=axs[1:3, 2], shrink=0.5, location='right')
@image_comparison(['test_colorbars_no_overlapV.png'], style='mpl20')
def mutated_test_colorbars_no_overlapV():
    fig = plt.figure(figsize=(2, 4), layout='constrained')
    axs = fig.subplots(2, 1, sharex=True, sharey=True)
    for ax in axs:
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        ax.tick_params(axis='both', direction='in')
        im = ax.imshow([[1, 2], [3, 4]])
        fig.colorbar(im, ax=ax, orientation='vertical')
    fig.suptitle('foo')
@image_comparison(['test_colorbars_no_overlapH.png'], style='mpl20')
def mutated_test_colorbars_no_overlapH():
    fig = plt.figure(figsize=(4, 2), layout='constrained')
    fig.suptitle('foo')
    axs = fig.subplots(1, 2, sharex=True, sharey=True)
    for ax in axs:
        ax.yaxis.set_major_formatter(ticker.NullFormatter())
        ax.tick_params(axis='both', direction='in')
        im = ax.imshow([[1, 2], [3, 4]])
        fig.colorbar(im, ax=ax, orientation='horizontal')
@image_comparison(['test_bboxtight.png'], remove_text=True, style='mpl20', savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_bboxtight():
    fig, ax = plt.subplots(layout='constrained')
    ax.set_aspect(1.0)
@image_comparison(['test_bbox.png'], remove_text=True, style='mpl20', savefig_kwarg={'bbox_inches': mtransforms.Bbox([[0.5, 0], [2.5, 2]])})
def mutated_test_bbox():
    fig, ax = plt.subplots(layout='constrained')
    ax.set_aspect(1.0)
