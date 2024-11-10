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

def test_antialiasing_7_mutated():
    mpl.rcParams['text.antialiased'] = False
    fig = plt.figure(figsize=(5.25, 0.75), layout='none')
    fig.text(0.3, 0.75, 'antialiased', horizontalalignment='center', verticalalignment='center', antialiased=True)
    fig.text(0.3, 0.25, '$\\sqrt{x}$', horizontalalignment='center', verticalalignment='center', antialiased=True)
    mpl.rcParams['text.antialiased'] = True
    fig.text(0.7, 0.75, 'not antialiased', horizontalalignment='center', verticalalignment='center', antialiased=False)
    fig.text(0.7, 0.25, '$\\sqrt{x}$', horizontalalignment='center', verticalalignment='center', antialiased=False)
    mpl.rcParams['text.antialiased'] = False