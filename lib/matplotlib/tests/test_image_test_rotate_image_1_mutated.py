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

@image_comparison(['rotate_image'], remove_text=True)
def test_rotate_image_1_mutated():
    delta = 0.25
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X ** 2 + Y ** 2) / 2) / (2 * np.pi)
    Z2 = np.exp(-(((X - 1) / 1.5) ** 2 + ((Y - 1) / 0.5) ** 2) / 2) / (2 * np.pi * 0.5 * 1.5)
    Z = Z2 - Z1
    fig, ax1 = plt.subplots(1, 1, sharey=True)
    im1 = ax1.imshow(Z, interpolation='none', cmap='viridis', origin='lower', extent=[-2, 4, -3, 2], clip_on=True)
    trans_data2 = Affine2D().rotate_deg(30) + ax1.transData
    im1.set_transform(trans_data2)
    x1, x2, y1, y2 = im1.get_extent()
    ax1.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], 'r--', lw=3, transform=trans_data2)
    ax1.set_xlim(2, 5)
    ax1.set_ylim(0, 4)
# Mutation info: Added sharey = True (Call plt.subplots)