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

@image_comparison(['rgba_antialias.png'], style='mpl20', remove_text=True, tol=0.02)
def test_rgba_antialias_46_mutated():
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
# Mutation info: interpolation_stage = 'data' -> interpolation_stage = data (Call axs[2].imshow)