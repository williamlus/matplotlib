from itertools import product
import io
import platform
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import cbook
from matplotlib.backend_bases import MouseEvent
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle, Ellipse
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
from mpl_toolkits.axes_grid1 import axes_size as Size, host_subplot, make_axes_locatable, Grid, AxesGrid, ImageGrid
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredAuxTransformBox, AnchoredDrawingArea, AnchoredEllipse, AnchoredDirectionArrows, AnchoredSizeBar
from mpl_toolkits.axes_grid1.axes_divider import Divider, HBoxDivider, make_axes_area_auto_adjustable, SubplotDivider, VBoxDivider
from mpl_toolkits.axes_grid1.axes_rgb import RGBAxes
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset, inset_axes, BboxConnectorPatch, InsetPosition
import mpl_toolkits.axes_grid1.mpl_axes
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
@image_comparison(['twin_axes_empty_and_removed'], extensions=['png'], tol=1, style=('classic', '_classic_test_patch'))
def mutated_test_twin_axes_empty_and_removed():
    mpl.rcParams.update({'font.size': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8})
    generators = ['twinx', 'twiny', 'twin']
    modifiers = ['', 'host invisible', 'twin removed', 'twin invisible', 'twin removed\nhost invisible']
    h = host_subplot(len(modifiers) + 1, len(generators), 2)
    h.text(0.5, 0.5, 'host_subplot', horizontalalignment='center', verticalalignment='center')
    for i, (mod, gen) in enumerate(product(modifiers, generators), len(generators) + 1):
        h = host_subplot(len(modifiers) + 1, len(generators), i)
        t = getattr(h, gen)()
        if 'twin invisible' in mod:
            t.axis[:].set_visible(False)
        if 'twin removed' in mod:
            t.remove()
        if 'host invisible' in mod:
            h.axis[:].set_visible(False)
        h.text(0.5, 0.5, gen + ('\n' + mod if mod else ''), horizontalalignment='center', verticalalignment='center')
    plt.subplots_adjust(wspace=0.5, hspace=1)
@image_comparison(['inset_locator.png'], style='default', remove_text=True)
def mutated_test_inset_locator():
    fig, ax = plt.subplots(figsize=[5, 4])
    Z = cbook.get_sample_data('axes_grid/bivariate_normal.npy')
    extent = (-3, 4, -4, 3)
    Z2 = np.zeros((150, 150))
    ny, nx = Z.shape
    Z2[30:30 + ny, 30:30 + nx] = Z
    ax.imshow(Z2, extent=extent, interpolation='nearest', origin='lower')
    axins = zoomed_inset_axes(ax, zoom=6, loc='upper right')
    axins.imshow(Z2, extent=extent, interpolation='nearest', origin='lower')
    axins.yaxis.get_major_locator().set_params(nbins=7)
    axins.xaxis.get_major_locator().set_params(nbins=7)
    x1, x2, y1, y2 = (-1.5, -0.9, -2.5, -1.9)
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    mark_inset(ax, axins, loc1=2, loc2=4, fc='none', ec='0.5')
    asb = AnchoredSizeBar(ax.transData, 0.5, '0.5', loc='lower center', pad=0.1, borderpad=0.5, sep=5, frameon=False)
    ax.add_artist(asb)
@image_comparison(['inset_axes.png'], style='default', remove_text=True)
def mutated_test_inset_axes():
    fig, ax = plt.subplots(figsize=[5, 4])
    Z = cbook.get_sample_data('axes_grid/bivariate_normal.npy')
    extent = (-3, 4, -4, 3)
    Z2 = np.zeros((150, 150))
    ny, nx = Z.shape
    Z2[30:30 + ny, 30:30 + nx] = Z
    ax.imshow(Z2, extent=extent, interpolation='nearest', origin='lower')
    axins = inset_axes(ax, width=1.0, height=1.0, bbox_to_anchor=(1, 1), bbox_transform=ax.transAxes)
    axins.imshow(Z2, extent=extent, interpolation='nearest', origin='lower')
    axins.yaxis.get_major_locator().set_params(nbins=7)
    axins.xaxis.get_major_locator().set_params(nbins=7)
    x1, x2, y1, y2 = (-1.5, -0.9, -2.5, -1.9)
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    mark_inset(ax, axins, loc1=2, loc2=4, fc='none', ec='0.5')
    asb = AnchoredSizeBar(ax.transData, 0.5, '0.5', loc='lower center', pad=0.1, borderpad=0.5, sep=5, frameon=False)
    ax.add_artist(asb)
@image_comparison(['fill_facecolor.png'], remove_text=True, style='mpl20')
def mutated_test_fill_facecolor():
    fig, ax = plt.subplots(1, 5)
    fig.set_size_inches(5, 5)
    for i in range(1, 4):
        ax[i].yaxis.set_visible(False)
    ax[4].yaxis.tick_right()
    bbox = Bbox.from_extents(0, 0.4, 1, 0.6)
    bbox1 = TransformedBbox(bbox, ax[0].transData)
    bbox2 = TransformedBbox(bbox, ax[1].transData)
    p = BboxConnectorPatch(bbox1, bbox2, loc1a=1, loc2a=2, loc1b=4, loc2b=3, ec='r', fc='b')
    p.set_clip_on(False)
    ax[0].add_patch(p)
    axins = zoomed_inset_axes(ax[0], 1, loc='upper right')
    axins.set_xlim(0, 0.2)
    axins.set_ylim(0, 0.2)
    plt.gca().axes.xaxis.set_ticks([])
    plt.gca().axes.yaxis.set_ticks([])
    mark_inset(ax[0], axins, loc1=2, loc2=4, fc='b', ec='0.5')
    bbox3 = TransformedBbox(bbox, ax[1].transData)
    bbox4 = TransformedBbox(bbox, ax[2].transData)
    p = BboxConnectorPatch(bbox3, bbox4, loc1a=1, loc2a=2, loc1b=4, loc2b=3, ec='r', facecolor='y')
    p.set_clip_on(False)
    ax[1].add_patch(p)
    axins = zoomed_inset_axes(ax[1], 1, loc='upper right')
    axins.set_xlim(0, 0.2)
    axins.set_ylim(0, 0.2)
    plt.gca().axes.xaxis.set_ticks([])
    plt.gca().axes.yaxis.set_ticks([])
    mark_inset(ax[1], axins, loc1=2, loc2=4, facecolor='y', ec='0.5')
    bbox5 = TransformedBbox(bbox, ax[2].transData)
    bbox6 = TransformedBbox(bbox, ax[3].transData)
    p = BboxConnectorPatch(bbox5, bbox6, loc1a=1, loc2a=2, loc1b=4, loc2b=3, ec='r', color='g')
    p.set_clip_on(False)
    ax[2].add_patch(p)
    axins = zoomed_inset_axes(ax[2], 1, loc='upper right')
    axins.set_xlim(0, 0.2)
    axins.set_ylim(0, 0.2)
    plt.gca().axes.xaxis.set_ticks([])
    plt.gca().axes.yaxis.set_ticks([])
    mark_inset(ax[2], axins, loc1=2, loc2=4, color='g', ec='0.5')
    bbox7 = TransformedBbox(bbox, ax[3].transData)
    bbox8 = TransformedBbox(bbox, ax[4].transData)
    p = BboxConnectorPatch(bbox7, bbox8, loc1a=1, loc2a=2, loc1b=4, loc2b=3, ec='r', fc='g', fill=False)
    p.set_clip_on(False)
    ax[3].add_patch(p)
    axins = zoomed_inset_axes(ax[3], 1, loc='upper right')
    axins.set_xlim(0, 0.2)
    axins.set_ylim(0, 0.2)
    axins.xaxis.set_ticks([])
    axins.yaxis.set_ticks([])
    mark_inset(ax[3], axins, loc1=2, loc2=4, fc='g', ec='0.5', fill=False)
@image_comparison(['zoomed_axes.png', 'inverted_zoomed_axes.png'], style=('classic', '_classic_test_patch'), tol=0.02 if platform.machine() == 'arm64' else 0)
def mutated_test_zooming_with_inverted_axes():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.axis([1, 3, 1, 3])
    inset_ax = zoomed_inset_axes(ax, zoom=2.5, loc='lower right')
    inset_ax.axis([1.1, 1.4, 1.1, 1.4])
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 2, 3])
    ax.axis([3, 1, 3, 1])
    inset_ax = zoomed_inset_axes(ax, zoom=2.5, loc='lower right')
    inset_ax.axis([1.4, 1.1, 1.4, 1.1])
@image_comparison(['anchored_direction_arrows.png'], tol=0 if platform.machine() == 'x86_64' else 0.01, style=('classic', '_classic_test_patch'))
def mutated_test_anchored_direction_arrows():
    fig, ax = plt.subplots()
    ax.imshow(np.zeros((10, 10)), interpolation='nearest')
    simple_arrow = AnchoredDirectionArrows(ax.transAxes, 'X', 'Y')
    ax.add_artist(simple_arrow)
@image_comparison(['anchored_direction_arrows_many_args.png'], style=('classic', '_classic_test_patch'))
def mutated_test_anchored_direction_arrows_many_args():
    fig, ax = plt.subplots()
    ax.imshow(np.ones((10, 10)))
    direction_arrows = AnchoredDirectionArrows(ax.transAxes, 'A', 'B', loc='upper right', color='red', aspect_ratio=-0.5, pad=0.6, borderpad=2, frameon=True, alpha=0.7, sep_x=-0.06, sep_y=-0.08, back_length=0.1, head_width=9, head_length=10, tail_width=5)
    ax.add_artist(direction_arrows)
@image_comparison(['image_grid_each_left_label_mode_all.png'], style='mpl20', savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_image_grid_each_left_label_mode_all():
    imdata = np.arange(100).reshape((10, 10))
    fig = plt.figure(1, (3, 3))
    grid = ImageGrid(fig, (1, 1, 1), nrows_ncols=(3, 2), axes_pad=(0.5, 0.3), cbar_mode='each', cbar_location='left', cbar_size='15%', label_mode='all')
    assert isinstance(grid.get_divider(), SubplotDivider)
    assert grid.get_axes_pad() == (0.5, 0.3)
    assert grid.get_aspect()
    for ax, cax in zip(grid, grid.cbar_axes):
        im = ax.imshow(imdata, interpolation='none')
        cax.colorbar(im)
@image_comparison(['image_grid_single_bottom_label_mode_1.png'], style='mpl20', savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_image_grid_single_bottom():
    imdata = np.arange(100).reshape((10, 10))
    fig = plt.figure(1, (2.5, 1.5))
    grid = ImageGrid(fig, (0, 0, 1, 1), nrows_ncols=(1, 3), axes_pad=(0.2, 0.15), cbar_mode='single', cbar_pad=0.3, cbar_location='bottom', cbar_size='10%', label_mode='1')
    assert type(grid.get_divider()) is Divider
    for i in range(3):
        im = grid[i].imshow(imdata, interpolation='none')
    grid.cbar_axes[0].colorbar(im)
@image_comparison(['image_grid.png'], remove_text=True, style='mpl20', savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_image_grid():
    im = np.arange(100).reshape((10, 10))
    fig = plt.figure(1, (4, 4))
    grid = ImageGrid(fig, 111, nrows_ncols=(2, 2), axes_pad=0.1)
    assert grid.get_axes_pad() == (0.1, 0.1)
    for i in range(4):
        grid[i].imshow(im, interpolation='nearest')
@image_comparison(['anchored_artists.png'], remove_text=True, style='mpl20')
def mutated_test_anchored_artists():
    fig, ax = plt.subplots(figsize=(3, 3))
    ada = AnchoredDrawingArea(40, 20, 0, 0, loc='upper right', pad=0.0, frameon=False)
    p1 = Circle((10, 10), 10)
    ada.drawing_area.add_artist(p1)
    p2 = Circle((30, 10), 5, fc='r')
    ada.drawing_area.add_artist(p2)
    ax.add_artist(ada)
    box = AnchoredAuxTransformBox(ax.transData, loc='upper left')
    el = Ellipse((0, 0), width=0.1, height=0.4, angle=30, color='cyan')
    box.drawing_area.add_artist(el)
    ax.add_artist(box)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        ae = AnchoredEllipse(ax.transData, width=0.1, height=0.25, angle=-60, loc='lower left', pad=0.5, borderpad=0.4, frameon=True)
    ax.add_artist(ae)
    asb = AnchoredSizeBar(ax.transData, 0.2, '0.2 units', loc='lower right', pad=0.3, borderpad=0.4, sep=4, fill_bar=True, frameon=False, label_top=True, prop={'size': 20}, size_vertical=0.05, color='green')
    ax.add_artist(asb)
@image_comparison(['rgb_axes.png'], remove_text=True, style=('classic', '_classic_test_patch'))
def mutated_test_rgb_axes():
    fig = plt.figure()
    ax = RGBAxes(fig, (0.1, 0.1, 0.8, 0.8), pad=0.1)
    rng = np.random.default_rng(19680801)
    r = rng.random((5, 5))
    g = rng.random((5, 5))
    b = rng.random((5, 5))
    ax.imshow_rgb(r, g, b, interpolation='none')
@image_comparison(['insetposition.png'], remove_text=True, style=('classic', '_classic_test_patch'))
def mutated_test_insetposition():
    fig, ax = plt.subplots(figsize=(2, 2))
    ax_ins = plt.axes([0, 0, 1, 1])
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        ip = InsetPosition(ax, [0.2, 0.25, 0.5, 0.4])
    ax_ins.set_axes_locator(ip)
@image_comparison(['imagegrid_cbar_mode.png'], remove_text=True, style='mpl20', tol=0.3)
def mutated_test_imagegrid_cbar_mode_edge():
    arr = np.arange(16).reshape((4, 4))
    fig = plt.figure(figsize=(18, 9))
    positions = (241, 242, 243, 244, 245, 246, 247, 248)
    directions = ['row'] * 4 + ['column'] * 4
    cbar_locations = ['left', 'right', 'top', 'bottom'] * 2
    for position, direction, location in zip(positions, directions, cbar_locations):
        grid = ImageGrid(fig, position, nrows_ncols=(2, 2), direction=direction, cbar_location=location, cbar_size='20%', cbar_mode='edge')
        ax1, ax2, ax3, ax4 = grid
        ax1.imshow(arr, cmap='nipy_spectral')
        ax2.imshow(arr.T, cmap='hot')
        ax3.imshow(np.hypot(arr, arr.T), cmap='jet')
        ax4.imshow(np.arctan2(arr, arr.T), cmap='hsv')
        for ax in grid:
            ax.cax.cla()
            cb = ax.cax.colorbar(ax.images[0])
@image_comparison(['anchored_locator_base_call.png'], style='mpl20')
def mutated_test_anchored_locator_base_call():
    fig = plt.figure(figsize=(3, 3))
    fig1, fig2 = fig.subfigures(nrows=2, ncols=1)
    ax = fig1.subplots()
    ax.set(aspect=1, xlim=(-15, 15), ylim=(-20, 5))
    ax.set(xticks=[], yticks=[])
    Z = cbook.get_sample_data('axes_grid/bivariate_normal.npy')
    extent = (-3, 4, -4, 3)
    axins = zoomed_inset_axes(ax, zoom=2, loc='upper left')
    axins.set(xticks=[], yticks=[])
    axins.imshow(Z, extent=extent, origin='lower')
