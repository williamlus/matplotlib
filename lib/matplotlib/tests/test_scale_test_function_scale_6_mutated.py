import copy
import matplotlib.pyplot as plt
from matplotlib.scale import AsinhScale, AsinhTransform, LogTransform, InvertedLogTransform, SymmetricalLogTransform
import matplotlib.scale as mscale
from matplotlib.ticker import AsinhLocator, LogFormatterSciNotation
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import numpy as np
from numpy.testing import assert_allclose
import io
import pytest

def test_function_scale_6_mutated():

    def inverse(x):
        return x ** 2

    def forward(x):
        return x ** (1 / 2)
    fig, ax = plt.subplots()
    x = np.arange(1, 1000)
    ax.plot(x, x)
    ax.set_xscale('function', functions=(forward, inverse))
    ax.set_xlim(1, 1000, emit=False)