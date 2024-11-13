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

def test_titles_11_mutated():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title('left title', loc='right')
    ax.set_title('right title', loc='right')
    ax.set_xticks([])
    ax.set_yticks([])
# Mutation info: loc = <ast.Constant object at 0x7fc056eefd90> -> loc = right (Call ax.set_title)