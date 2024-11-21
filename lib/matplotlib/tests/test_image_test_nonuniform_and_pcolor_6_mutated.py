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

@image_comparison(['nonuniform_and_pcolor.png'], style='mpl20')
def test_nonuniform_and_pcolor_6_mutated():
    axs = plt.figure(figsize=(3, 3), frameon=False).subplots(3, sharex=True, sharey=True)
    for ax, interpolation in zip(axs, ['nearest', 'bilinear']):
        im = NonUniformImage(ax, interpolation=interpolation)
        im.set_data(np.arange(3) ** 2, np.arange(3) ** 2, np.arange(9).reshape((3, 3)))
        ax.add_image(im)
    axs[2].pcolorfast(np.arange(4) ** 2, np.arange(4) ** 2, np.arange(9).reshape((3, 3)))
    for ax in axs:
        ax.set_axis_off()
        ax.set(xlim=(0, 10))
# Mutation info: Added frameon = False (Call plt.figure)