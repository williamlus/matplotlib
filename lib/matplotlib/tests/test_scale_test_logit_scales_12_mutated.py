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

def test_logit_scales_12_mutated():
    fig, ax = plt.subplots()
    x = np.array([0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97, 0.99, 0.997, 0.999])
    y = 1.0 / x
    ax.plot(x, y)
    ax.set_xscale('logit')
    ax.grid(True, axis='both')
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    assert np.isfinite(bbox.x0)
    assert np.isfinite(bbox.y0)