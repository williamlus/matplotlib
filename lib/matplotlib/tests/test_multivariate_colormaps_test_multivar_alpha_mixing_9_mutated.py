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

@image_comparison(['multivar_alpha_mixing.png'])
def test_multivar_alpha_mixing_9_mutated():
    rainbow = mpl.colormaps['rainbow']
    alpha = np.zeros((256, 4))
    alpha[:, 3] = np.linspace(1, 0, 256)
    alpha_cmap = mpl.colors.LinearSegmentedColormap.from_list('from_list', alpha)
    cmap = mpl.colors.MultivarColormap((rainbow, alpha_cmap), 'sRGB_add')
    y, x = np.mgrid[0:10, 0:10] / 9
    im = cmap((y, x))
    fig, ax = plt.subplots()
    ax.imshow(im, interpolation='nearest', filternorm=False)
    remove_ticks_and_titles(fig)
# Mutation info: Added filternorm = False (Call ax.imshow)