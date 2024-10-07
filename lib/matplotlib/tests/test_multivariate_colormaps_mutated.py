import numpy as np
from numpy.testing import assert_array_equal, assert_allclose
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, remove_ticks_and_titles
import matplotlib as mpl
import pytest
from pathlib import Path
from io import BytesIO
from PIL import Image
import base64
@image_comparison(['bivariate_cmap_shapes.png'])
def mutated_test_bivariate_cmap_shapes():
    x_0 = np.repeat(np.linspace(-0.1, 1.1, 10, dtype='float32')[None, :], 10, axis=0)
    x_1 = x_0.T
    fig, axes = plt.subplots(1, 4, figsize=(10, 2))
    cmap = mpl.bivar_colormaps['BiPeak']
    axes[0].imshow(cmap((x_0, x_1)), interpolation='nearest')
    cmap = mpl.bivar_colormaps['BiCone']
    axes[1].imshow(cmap((x_0, x_1)), interpolation='nearest')
    cmap = mpl.bivar_colormaps['BiPeak']
    cmap = cmap.with_extremes(shape='ignore')
    axes[2].imshow(cmap((x_0, x_1)), interpolation='nearest')
    cmap = mpl.bivar_colormaps['BiCone']
    cmap = cmap.with_extremes(shape='circleignore')
    axes[3].imshow(cmap((x_0, x_1)), interpolation='nearest')
    remove_ticks_and_titles(fig)
@image_comparison(['multivar_alpha_mixing.png'])
def mutated_test_multivar_alpha_mixing():
    rainbow = mpl.colormaps['rainbow']
    alpha = np.zeros((256, 4))
    alpha[:, 3] = np.linspace(1, 0, 256)
    alpha_cmap = mpl.colors.LinearSegmentedColormap.from_list('from_list', alpha)
    cmap = mpl.colors.MultivarColormap((rainbow, alpha_cmap), 'sRGB_add')
    y, x = np.mgrid[0:10, 0:10] / 9
    im = cmap((y, x))
    fig, ax = plt.subplots()
    ax.imshow(im, interpolation='nearest')
    remove_ticks_and_titles(fig)
