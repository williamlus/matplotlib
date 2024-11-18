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

@image_comparison(['text_alignment'], style='mpl20')
def test_alignment_20_mutated():
    plt.figure()
    ax = plt.subplot(1, 1, 1, projection='hammer')
    x = 0.1
    for rotation in (0, 30):
        for alignment in ('top', 'bottom', 'baseline', 'center'):
            ax.text(x, 0.5, alignment + ' Tj', va=alignment, rotation=rotation, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.text(x, 1.0, '$\\sum_{i=0}^{j}$', va=alignment, rotation=rotation)
            x += 0.1
    ax.plot([0, 1], [0.5, 0.5])
    ax.plot([0, 1], [1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
# Mutation info: Added projection = hammer (Call plt.subplot)