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

class QuantityND(np.ndarray):

    def __new__(cls, input_array, units):
        obj = np.asarray(input_array).view(cls)
        obj.units = units
        return obj

    def __array_finalize__(self, obj):
        self.units = getattr(obj, 'units', None)

    def __getitem__(self, item):
        units = getattr(self, 'units', None)
        ret = super().__getitem__(item)
        if isinstance(ret, QuantityND) or units is not None:
            ret = QuantityND(ret, units)
        return ret

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        func = getattr(ufunc, method)
        if 'out' in kwargs:
            return NotImplemented
        if len(inputs) == 1:
            i0 = inputs[0]
            unit = getattr(i0, 'units', 'dimensionless')
            out_arr = func(np.asarray(i0), **kwargs)
        elif len(inputs) == 2:
            i0 = inputs[0]
            i1 = inputs[1]
            u0 = getattr(i0, 'units', 'dimensionless')
            u1 = getattr(i1, 'units', 'dimensionless')
            u0 = u1 if u0 is None else u0
            u1 = u0 if u1 is None else u1
            if ufunc in [np.add, np.subtract]:
                if u0 != u1:
                    raise ValueError
                unit = u0
            elif ufunc == np.multiply:
                unit = f'{u0}*{u1}'
            elif ufunc == np.divide:
                unit = f'{u0}/({u1})'
            elif ufunc in (np.greater, np.greater_equal, np.equal, np.not_equal, np.less, np.less_equal):
                unit = None
            else:
                return NotImplemented
            out_arr = func(i0.view(np.ndarray), i1.view(np.ndarray), **kwargs)
        else:
            return NotImplemented
        if unit is None:
            out_arr = np.array(out_arr)
        else:
            out_arr = QuantityND(out_arr, unit)
        return out_arr

    @property
    def v(self):
        return self.view(np.ndarray)

@image_comparison(['downsampling.png'], style='mpl20', remove_text=True, tol=0.09)
def test_downsampling_9_mutated():
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
    axs[0, 0].set_xlim(125, 175, auto=True)
    axs[0, 0].set_ylim(250, 200)
    axs[0, 0].set_title('Zoom')
    for ax, interp, space in zip(axs.flat[1:], ['nearest', 'nearest', 'hanning', 'hanning', 'auto'], ['data', 'rgba', 'data', 'rgba', 'auto']):
        ax.imshow(a, interpolation=interp, interpolation_stage=space, cmap='RdBu_r')
        ax.set_title(f"interpolation='{interp}'\nspace='{space}'")
# Mutation info: Added auto = True (Call axs[0, 0].set_xlim)