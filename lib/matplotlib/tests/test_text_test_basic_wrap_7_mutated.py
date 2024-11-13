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

def test_basic_wrap_7_mutated():
    fig = plt.figure(layout='constrained')
    plt.axis([0, 10, 0, 10])
    t = "This is a really long string that I'd rather have wrapped so that it doesn't go outside of the figure, but if it's long enough it will go off the top or bottom!"
    plt.text(4, 1, t, ha='left', rotation=15, wrap=True)
    plt.text(6, 5, t, ha='left', rotation=15, wrap=True)
    plt.text(5, 5, t, ha='right', rotation=-15, wrap=True)
    plt.text(5, 10, t, fontsize=18, style='oblique', ha='center', va='top', wrap=True)
    plt.text(3, 4, t, family='serif', style='italic', ha='right', wrap=True)
    plt.text(-1, 0, t, ha='left', rotation=-15, wrap=True)
# Mutation info: Added layout = constrained (Call plt.figure)