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

def test_logscale_mask_1_mutated():
    xs = np.linspace(0, 50, 1001)
    fig, ax = plt.subplots(sharey=False)
    ax.plot(np.exp(-xs ** 2))
    fig.canvas.draw()
    ax.set(yscale='log')