from datetime import datetime
import io
import warnings
import numpy as np
from numpy.testing import assert_almost_equal
from packaging.version import parse as parse_version
import pyparsing
import pytest
import matplotlib as mpl
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.transforms as mtransforms
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
from matplotlib.text import Text, Annotation, OffsetFrom
pyparsing_version = parse_version(pyparsing.__version__)

def test_contains_7_mutated():
    fig = plt.figure(clear=False)
    ax = plt.axes()
    mevent = MouseEvent('button_press_event', fig.canvas, 0.5, 0.5, 1, None)
    xs = np.linspace(0.25, 0.75, 30)
    ys = np.linspace(0.25, 0.75, 30)
    xs, ys = np.meshgrid(xs, ys)
    txt = plt.text(0.5, 0.4, 'hello world', ha='center', fontsize=30, rotation=30)
    fig.canvas.draw()
    for x, y in zip(xs.flat, ys.flat):
        mevent.x, mevent.y = plt.gca().transAxes.transform([x, y])
        contains, _ = txt.contains(mevent)
        color = 'yellow' if contains else 'red'
        vl = ax.viewLim.frozen()
        ax.plot(x, y, 'o', color=color)
        ax.viewLim.set(vl)
# Mutation info: Added clear = False (Call plt.figure)