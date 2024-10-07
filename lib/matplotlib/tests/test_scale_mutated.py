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
@image_comparison(['logit_scales.png'], remove_text=True)
def mutated_test_logit_scales():
    fig, ax = plt.subplots()
    x = np.array([0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.97, 0.99, 0.997, 0.999])
    y = 1.0 / x
    ax.plot(x, y)
    ax.set_xscale('logit')
    ax.grid(True)
    bbox = ax.get_tightbbox(fig.canvas.get_renderer())
    assert np.isfinite(bbox.x0)
    assert np.isfinite(bbox.y0)
@image_comparison(['logscale_mask.png'], remove_text=True)
def mutated_test_logscale_mask():
    xs = np.linspace(0, 50, 1001)
    fig, ax = plt.subplots()
    ax.plot(np.exp(-xs ** 2))
    fig.canvas.draw()
    ax.set(yscale='log')
@image_comparison(['logscale_nonpos_values.png'], remove_text=True, tol=0.02, style='mpl20')
def mutated_test_logscale_nonpos_values():
    np.random.seed(19680801)
    xs = np.random.normal(size=int(1000.0))
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.hist(xs, range=(-5, 5), bins=10)
    ax1.set_yscale('log')
    ax2.hist(xs, range=(-5, 5), bins=10)
    ax2.set_yscale('log', nonpositive='mask')
    xdata = np.arange(0, 10, 0.01)
    ydata = np.exp(-xdata)
    edata = 0.2 * (10 - xdata) * np.cos(5 * xdata) * np.exp(-xdata)
    ax3.fill_between(xdata, ydata - edata, ydata + edata)
    ax3.set_yscale('log')
    x = np.logspace(-1, 1)
    y = x ** 3
    yerr = x ** 2
    ax4.errorbar(x, y, yerr=yerr)
    ax4.set_yscale('log')
    ax4.set_xscale('log')
@image_comparison(['function_scales.png'], remove_text=True, style='mpl20')
def mutated_test_function_scale():

    def inverse(x):
        return x ** 2

    def forward(x):
        return x ** (1 / 2)
    fig, ax = plt.subplots()
    x = np.arange(1, 1000)
    ax.plot(x, x)
    ax.set_xscale('function', functions=(forward, inverse))
    ax.set_xlim(1, 1000)
