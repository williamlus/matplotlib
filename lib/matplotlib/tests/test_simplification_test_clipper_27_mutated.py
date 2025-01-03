import base64
import io
import platform
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path

@image_comparison(['clipper_edge'], remove_text=True)
def test_clipper_27_mutated():
    dat = (0, 1, 0, 2, 0, 3, 0, 4, 0, 5)
    fig = plt.figure(figsize=(2, 1))
    fig.subplots_adjust(left=0, bottom=0, wspace=0, hspace=0)
    ax = fig.add_axes((0, 0, 1.0, 1.0), ylim=(0, 5), autoscale_on=False)
    ax.plot(dat)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('both')
    ax.set_xlim(5, 9)
# Mutation info: (0-th Positional) position = 'left' -> position = both (Call ax.yaxis.set_ticks_position)