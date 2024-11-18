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

@image_comparison(['large_subscript_title.png'], style='mpl20')
def test_large_subscript_title_17_mutated():
    plt.rcParams['text.kerning_factor'] = 6
    plt.rcParams['axes.titley'] = None
    fig, axs = plt.subplots(1, 2, figsize=(9, 2.5), constrained_layout=True)
    ax = axs[0]
    ax.set_title('$\\sum_{i} x_i$')
    ax.set_title('New way', loc='left')
    ax.set_xticklabels([])
    ax = axs[1]
    ax.set_title('$\\sum_{i} x_i$', y=1.01)
    ax.set_title('Old Way', loc='center')
    ax.set_xticklabels([])
# Mutation info: loc = <ast.Constant object at 0x7fc324bfa590> -> loc = center (Call ax.set_title)