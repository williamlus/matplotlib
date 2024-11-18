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

@image_comparison(baseline_images=['fonttext_wrap'], extensions=['png'])
def test_font_wrap_11_mutated():
    fig = plt.figure()
    plt.axis([0, 10, 0, 10], emit=True)
    t = "This is a really long string that I'd rather have wrapped so that it doesn't go outside of the figure, but if it's long enough it will go off the top or bottom!"
    plt.text(4, -1, t, fontsize=18, family='serif', ha='left', rotation=15, wrap=True)
    plt.text(6, 5, t, family='sans serif', ha='left', rotation=15, wrap=True)
    plt.text(5, 10, t, weight='heavy', ha='center', va='top', wrap=True)
    plt.text(3, 4, t, family='monospace', ha='right', wrap=True)
    plt.text(-1, 0, t, fontsize=14, style='italic', ha='left', rotation=-15, wrap=True)
# Mutation info: Added emit = True (Call plt.axis)