from contextlib import ExitStack
from copy import copy
import functools
import io
import os
from pathlib import Path
import platform
import sys
import urllib.request
import numpy as np
from numpy.testing import assert_array_equal
from PIL import Image
import matplotlib as mpl
from matplotlib import colors, image as mimage, patches, pyplot as plt, style, rcParams
from matplotlib.image import AxesImage, BboxImage, FigureImage, NonUniformImage, PcolorImage
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.transforms import Bbox, Affine2D, TransformedBbox
import matplotlib.ticker as mticker
import pytest
@image_comparison(['interp_alpha.png'], remove_text=True)
def mutated_test_alpha_interp():
    """Test the interpolation of the alpha channel on RGBA images"""
    fig, (axl, axr) = plt.subplots(1, 2)
    img = np.zeros((5, 5, 4))
    img[..., 1] = np.ones((5, 5))
    img[..., 3] = np.tril(np.ones((5, 5), dtype=np.uint8))
    axl.imshow(img, interpolation='none')
    axr.imshow(img, interpolation='bilinear')
@image_comparison(['interp_nearest_vs_none'], extensions=['pdf', 'svg'], remove_text=True)
def mutated_test_interp_nearest_vs_none():
    """Test the effect of "nearest" and "none" interpolation"""
    rcParams['savefig.dpi'] = 3
    X = np.array([[[218, 165, 32], [122, 103, 238]], [[127, 255, 0], [255, 99, 71]]], dtype=np.uint8)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(X, interpolation='none')
    ax1.set_title('interpolation none')
    ax2.imshow(X, interpolation='nearest')
    ax2.set_title('interpolation nearest')
@image_comparison(['image_alpha'], remove_text=True)
def mutated_test_image_alpha():
    np.random.seed(0)
    Z = np.random.rand(6, 6)
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.imshow(Z, alpha=1.0, interpolation='none')
    ax2.imshow(Z, alpha=0.5, interpolation='none')
    ax3.imshow(Z, alpha=0.5, interpolation='nearest')
@image_comparison(['image_clip'], style='mpl20')
def mutated_test_image_clip():
    d = [[1, 2], [3, 4]]
    fig, ax = plt.subplots()
    im = ax.imshow(d)
    patch = patches.Circle((0, 0), radius=1, transform=ax.transData)
    im.set_clip_path(patch)
@image_comparison(['image_cliprect'], style='mpl20')
def mutated_test_image_cliprect():
    fig, ax = plt.subplots()
    d = [[1, 2], [3, 4]]
    im = ax.imshow(d, extent=(0, 5, 0, 5))
    rect = patches.Rectangle(xy=(1, 1), width=2, height=2, transform=im.axes.transData)
    im.set_clip_path(rect)
@image_comparison(['no_interpolation_origin'], remove_text=True)
def mutated_test_no_interpolation_origin():
    fig, axs = plt.subplots(2)
    axs[0].imshow(np.arange(100).reshape((2, 50)), origin='lower', interpolation='none')
    axs[1].imshow(np.arange(100).reshape((2, 50)), interpolation='none')
@image_comparison(['image_shift'], remove_text=True, extensions=['pdf', 'svg'])
def mutated_test_image_shift():
    imgData = [[1 / x + 1 / y for x in range(1, 100)] for y in range(1, 100)]
    tMin = 734717.945208
    tMax = 734717.946366
    fig, ax = plt.subplots()
    ax.imshow(imgData, norm=colors.LogNorm(), interpolation='none', extent=(tMin, tMax, 1, 100))
    ax.set_aspect('auto')
@image_comparison(['image_composite_background'], remove_text=True, style='mpl20')
def mutated_test_image_composite_background():
    fig, ax = plt.subplots()
    arr = np.arange(12).reshape(4, 3)
    ax.imshow(arr, extent=[0, 2, 15, 0])
    ax.imshow(arr, extent=[4, 6, 15, 0])
    ax.set_facecolor((1, 0, 0, 0.5))
    ax.set_xlim([0, 12])
@image_comparison(['image_composite_alpha'], remove_text=True)
def mutated_test_image_composite_alpha():
    """
    Tests that the alpha value is recognized and correctly applied in the
    process of compositing images together.
    """
    fig, ax = plt.subplots()
    arr = np.zeros((11, 21, 4))
    arr[:, :, 0] = 1
    arr[:, :, 3] = np.concatenate((np.arange(0, 1.1, 0.1), np.arange(0, 1, 0.1)[::-1]))
    arr2 = np.zeros((21, 11, 4))
    arr2[:, :, 0] = 1
    arr2[:, :, 1] = 1
    arr2[:, :, 3] = np.concatenate((np.arange(0, 1.1, 0.1), np.arange(0, 1, 0.1)[::-1]))[:, np.newaxis]
    ax.imshow(arr, extent=[1, 2, 5, 0], alpha=0.3)
    ax.imshow(arr, extent=[2, 3, 5, 0], alpha=0.6)
    ax.imshow(arr, extent=[3, 4, 5, 0])
    ax.imshow(arr2, extent=[0, 5, 1, 2])
    ax.imshow(arr2, extent=[0, 5, 2, 3], alpha=0.6)
    ax.imshow(arr2, extent=[0, 5, 3, 4], alpha=0.3)
    ax.set_facecolor((0, 0.5, 0, 1))
    ax.set_xlim([0, 5])
    ax.set_ylim([5, 0])
@image_comparison(['rasterize_10dpi'], extensions=['pdf', 'svg'], remove_text=True, style='mpl20')
def mutated_test_rasterize_dpi():
    img = np.asarray([[1, 2], [3, 4]])
    fig, axs = plt.subplots(1, 3, figsize=(3, 1))
    axs[0].imshow(img)
    axs[1].plot([0, 1], [0, 1], linewidth=20.0, rasterized=True)
    axs[1].set(xlim=(0, 1), ylim=(-1, 2))
    axs[2].plot([0, 1], [0, 1], linewidth=20.0)
    axs[2].set(xlim=(0, 1), ylim=(-1, 2))
    for ax in axs:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines[:].set_visible(False)
    rcParams['savefig.dpi'] = 10
@image_comparison(['bbox_image_inverted'], remove_text=True, style='mpl20')
def mutated_test_bbox_image_inverted():
    image = np.arange(100).reshape((10, 10))
    fig, ax = plt.subplots()
    bbox_im = BboxImage(TransformedBbox(Bbox([[100, 100], [0, 0]]), ax.transData), interpolation='nearest')
    bbox_im.set_data(image)
    bbox_im.set_clip_on(False)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.add_artist(bbox_im)
    image = np.identity(10)
    bbox_im = BboxImage(TransformedBbox(Bbox([[0.1, 0.2], [0.3, 0.25]]), ax.get_figure().transFigure), interpolation='nearest')
    bbox_im.set_data(image)
    bbox_im.set_clip_on(False)
    ax.add_artist(bbox_im)
@image_comparison(['zoom_and_clip_upper_origin.png'], remove_text=True, style='mpl20')
def mutated_test_zoom_and_clip_upper_origin():
    image = np.arange(100)
    image = image.reshape((10, 10))
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_ylim(2.0, -0.5)
    ax.set_xlim(-0.5, 2.0)
@image_comparison(['log_scale_image'], remove_text=True)
def mutated_test_log_scale_image():
    Z = np.zeros((10, 10))
    Z[::2] = 1
    fig, ax = plt.subplots()
    ax.imshow(Z, extent=[1, 100, 1, 100], cmap='viridis', vmax=1, vmin=-1, aspect='auto')
    ax.set(yscale='log')
@image_comparison(['rotate_image'], remove_text=True)
def mutated_test_rotate_image():
    delta = 0.25
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X ** 2 + Y ** 2) / 2) / (2 * np.pi)
    Z2 = np.exp(-(((X - 1) / 1.5) ** 2 + ((Y - 1) / 0.5) ** 2) / 2) / (2 * np.pi * 0.5 * 1.5)
    Z = Z2 - Z1
    fig, ax1 = plt.subplots(1, 1)
    im1 = ax1.imshow(Z, interpolation='none', cmap='viridis', origin='lower', extent=[-2, 4, -3, 2], clip_on=True)
    trans_data2 = Affine2D().rotate_deg(30) + ax1.transData
    im1.set_transform(trans_data2)
    x1, x2, y1, y2 = im1.get_extent()
    ax1.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], 'r--', lw=3, transform=trans_data2)
    ax1.set_xlim(2, 5)
    ax1.set_ylim(0, 4)
@image_comparison(['mask_image_over_under.png'], remove_text=True, tol=1.0)
def mutated_test_mask_image_over_under():
    delta = 0.025
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X ** 2 + Y ** 2) / 2) / (2 * np.pi)
    Z2 = np.exp(-(((X - 1) / 1.5) ** 2 + ((Y - 1) / 0.5) ** 2) / 2) / (2 * np.pi * 0.5 * 1.5)
    Z = 10 * (Z2 - Z1)
    palette = plt.cm.gray.with_extremes(over='r', under='g', bad='b')
    Zm = np.ma.masked_where(Z > 1.2, Z)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    im = ax1.imshow(Zm, interpolation='bilinear', cmap=palette, norm=colors.Normalize(vmin=-1.0, vmax=1.0, clip=False), origin='lower', extent=[-3, 3, -3, 3])
    ax1.set_title('Green=low, Red=high, Blue=bad')
    fig.colorbar(im, extend='both', orientation='horizontal', ax=ax1, aspect=10)
    im = ax2.imshow(Zm, interpolation='nearest', cmap=palette, norm=colors.BoundaryNorm([-1, -0.5, -0.2, 0, 0.2, 0.5, 1], ncolors=256, clip=False), origin='lower', extent=[-3, 3, -3, 3])
    ax2.set_title('With BoundaryNorm')
    fig.colorbar(im, extend='both', spacing='proportional', orientation='horizontal', ax=ax2, aspect=10)
@image_comparison(['mask_image'], remove_text=True)
def mutated_test_mask_image():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    A = np.ones((5, 5))
    A[1:2, 1:2] = np.nan
    ax1.imshow(A, interpolation='nearest')
    A = np.zeros((5, 5), dtype=bool)
    A[1:2, 1:2] = True
    A = np.ma.masked_array(np.ones((5, 5), dtype=np.uint16), A)
    ax2.imshow(A, interpolation='nearest')
@image_comparison(['imshow_endianess.png'], remove_text=True)
def mutated_test_imshow_endianess():
    x = np.arange(10)
    X, Y = np.meshgrid(x, x)
    Z = np.hypot(X - 5, Y - 5)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    kwargs = dict(origin='lower', interpolation='nearest', cmap='viridis')
    ax1.imshow(Z.astype('<f8'), **kwargs)
    ax2.imshow(Z.astype('>f8'), **kwargs)
@image_comparison(['imshow_masked_interpolation'], tol=0 if platform.machine() == 'x86_64' else 0.01, remove_text=True, style='mpl20')
def mutated_test_imshow_masked_interpolation():
    cmap = mpl.colormaps['viridis'].with_extremes(over='r', under='b', bad='k')
    N = 20
    n = colors.Normalize(vmin=0, vmax=N * N - 1)
    data = np.arange(N * N, dtype=float).reshape(N, N)
    data[5, 5] = -1
    data[15, 5] = 100000.0
    data[15, 15] = np.inf
    mask = np.zeros_like(data).astype('bool')
    mask[5, 15] = True
    data = np.ma.masked_array(data, mask)
    fig, ax_grid = plt.subplots(3, 6)
    interps = sorted(mimage._interpd_)
    interps.remove('auto')
    interps.remove('antialiased')
    for interp, ax in zip(interps, ax_grid.ravel()):
        ax.set_title(interp)
        ax.imshow(data, norm=n, cmap=cmap, interpolation=interp)
        ax.axis('off')
@image_comparison(['imshow_flatfield.png'], remove_text=True, style='mpl20')
def mutated_test_imshow_flatfield():
    fig, ax = plt.subplots()
    im = ax.imshow(np.ones((5, 5)), interpolation='nearest')
    im.set_clim(0.5, 1.5)
@image_comparison(['imshow_bignumbers.png'], remove_text=True, style='mpl20')
def mutated_test_imshow_bignumbers():
    rcParams['image.interpolation'] = 'nearest'
    fig, ax = plt.subplots()
    img = np.array([[1, 2, 1000000000000.0], [3, 1, 4]], dtype=np.uint64)
    pc = ax.imshow(img)
    pc.set_clim(0, 5)
@image_comparison(['imshow_bignumbers_real.png'], remove_text=True, style='mpl20')
def mutated_test_imshow_bignumbers_real():
    rcParams['image.interpolation'] = 'nearest'
    fig, ax = plt.subplots()
    img = np.array([[2.0, 1.0, 1e+22], [4.0, 1.0, 3.0]])
    pc = ax.imshow(img)
    pc.set_clim(0, 5)
@image_comparison(['image_placement'], extensions=['svg', 'pdf'], remove_text=True, style='mpl20')
def mutated_test_image_placement():
    """
    The red box should line up exactly with the outside of the image.
    """
    fig, ax = plt.subplots()
    ax.plot([0, 0, 1, 1, 0], [0, 1, 1, 0, 0], color='r', lw=0.1)
    np.random.seed(19680801)
    ax.imshow(np.random.randn(16, 16), cmap='Blues', extent=(0, 1, 0, 1), interpolation='none', vmin=-1, vmax=1)
    ax.set_xlim(-0.1, 1 + 0.1)
    ax.set_ylim(-0.1, 1 + 0.1)
@image_comparison(['nonuniform_and_pcolor.png'], style='mpl20')
def mutated_test_nonuniform_and_pcolor():
    axs = plt.figure(figsize=(3, 3)).subplots(3, sharex=True, sharey=True)
    for ax, interpolation in zip(axs, ['nearest', 'bilinear']):
        im = NonUniformImage(ax, interpolation=interpolation)
        im.set_data(np.arange(3) ** 2, np.arange(3) ** 2, np.arange(9).reshape((3, 3)))
        ax.add_image(im)
    axs[2].pcolorfast(np.arange(4) ** 2, np.arange(4) ** 2, np.arange(9).reshape((3, 3)))
    for ax in axs:
        ax.set_axis_off()
        ax.set(xlim=(0, 10))
@image_comparison(['nonuniform_logscale.png'], style='mpl20')
def mutated_test_nonuniform_logscale():
    _, axs = plt.subplots(ncols=3, nrows=1)
    for i in range(3):
        ax = axs[i]
        im = NonUniformImage(ax)
        im.set_data(np.arange(1, 4) ** 2, np.arange(1, 4) ** 2, np.arange(9).reshape((3, 3)))
        ax.set_xlim(1, 16)
        ax.set_ylim(1, 16)
        ax.set_box_aspect(1)
        if i == 1:
            ax.set_xscale('log', base=2)
            ax.set_yscale('log', base=2)
        if i == 2:
            ax.set_xscale('log', base=4)
            ax.set_yscale('log', base=4)
        ax.add_image(im)
@image_comparison(['rgba_antialias.png'], style='mpl20', remove_text=True, tol=0.02)
def mutated_test_rgba_antialias():
    fig, axs = plt.subplots(2, 2, figsize=(3.5, 3.5), sharex=False, sharey=False, constrained_layout=True)
    N = 250
    aa = np.ones((N, N))
    aa[::2, :] = -1
    x = np.arange(N) / N - 0.5
    y = np.arange(N) / N - 0.5
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X ** 2 + Y ** 2)
    f0 = 10
    k = 75
    a = np.sin(np.pi * 2 * (f0 * R + k * R ** 2 / 2))
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.4] = -1
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.3] = 1
    aa[:, int(N / 2):] = a[:, int(N / 2):]
    aa[20:50, 20:50] = np.nan
    aa[70:90, 70:90] = 1000000.0
    aa[70:90, 20:30] = -1000000.0
    aa[70:90, 195:215] = 1000000.0
    aa[20:30, 195:215] = -1000000.0
    cmap = copy(plt.cm.RdBu_r)
    cmap.set_over('yellow')
    cmap.set_under('cyan')
    axs = axs.flatten()
    axs[0].imshow(aa, interpolation='nearest', cmap=cmap, vmin=-1.2, vmax=1.2)
    axs[0].set_xlim([N / 2 - 25, N / 2 + 25])
    axs[0].set_ylim([N / 2 + 50, N / 2 - 10])
    axs[1].imshow(aa, interpolation='nearest', cmap=cmap, vmin=-1.2, vmax=1.2)
    axs[2].imshow(aa, interpolation='auto', interpolation_stage='data', cmap=cmap, vmin=-1.2, vmax=1.2)
    axs[3].imshow(aa, interpolation='auto', interpolation_stage='rgba', cmap=cmap, vmin=-1.2, vmax=1.2)
@image_comparison(['downsampling.png'], style='mpl20', remove_text=True, tol=0.09)
def mutated_test_downsampling():
    N = 450
    x = np.arange(N) / N - 0.5
    y = np.arange(N) / N - 0.5
    aa = np.ones((N, N))
    aa[::2, :] = -1
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X ** 2 + Y ** 2)
    f0 = 5
    k = 100
    a = np.sin(np.pi * 2 * (f0 * R + k * R ** 2 / 2))
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.4] = -1
    a[:int(N / 2), :][R[:int(N / 2), :] < 0.3] = 1
    aa[:, int(N / 3):] = a[:, int(N / 3):]
    a = aa
    fig, axs = plt.subplots(2, 3, figsize=(7, 6), layout='compressed')
    axs[0, 0].imshow(a, interpolation='nearest', interpolation_stage='rgba', cmap='RdBu_r')
    axs[0, 0].set_xlim(125, 175)
    axs[0, 0].set_ylim(250, 200)
    axs[0, 0].set_title('Zoom')
    for ax, interp, space in zip(axs.flat[1:], ['nearest', 'nearest', 'hanning', 'hanning', 'auto'], ['data', 'rgba', 'data', 'rgba', 'auto']):
        ax.imshow(a, interpolation=interp, interpolation_stage=space, cmap='RdBu_r')
        ax.set_title(f"interpolation='{interp}'\nspace='{space}'")
@image_comparison(['downsampling_speckle.png'], style='mpl20', remove_text=True, tol=0.09)
def mutated_test_downsampling_speckle():
    fig, axs = plt.subplots(1, 2, figsize=(5, 2.7), sharex=True, sharey=True, layout='compressed')
    axs = axs.flatten()
    img = (np.arange(1024).reshape(-1, 1) * np.ones(720) // 50).T
    cm = plt.get_cmap('viridis')
    cm.set_over('m')
    norm = colors.LogNorm(vmin=3, vmax=11)
    axs[0].set_title("interpolation='auto', stage='rgba'")
    axs[0].imshow(np.triu(img), cmap=cm, norm=norm, interpolation_stage='rgba')
    axs[1].set_title("interpolation='auto', stage='auto'")
    axs[1].imshow(np.triu(img), cmap=cm, norm=norm)
@image_comparison(['upsampling.png'], style='mpl20', remove_text=True)
def mutated_test_upsampling():
    np.random.seed(19680801 + 9)
    a = np.random.rand(4, 4)
    fig, axs = plt.subplots(1, 3, figsize=(6.5, 3), layout='compressed')
    im = axs[0].imshow(a, cmap='viridis')
    axs[0].set_title("interpolation='auto'\nstage='antialaised'\n(default for upsampling)")
    axs[1].imshow(a, cmap='viridis', interpolation='sinc')
    axs[1].set_title("interpolation='sinc'\nstage='auto'\n(default for upsampling)")
    axs[2].imshow(a, cmap='viridis', interpolation='sinc', interpolation_stage='rgba')
    axs[2].set_title("interpolation='sinc'\nstage='rgba'")
    fig.colorbar(im, ax=axs, shrink=0.7, extend='both')
