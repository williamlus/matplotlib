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

@image_comparison(['axes_titles.png'])
def test_axes_titles_23_mutated():
    plt.figure()
    ax = plt.subplot(1, 1, 1, projection='rectilinear')
    ax.set_title('center', loc='center', fontsize=20, fontweight=700)
    ax.set_title('left', loc='left', fontsize=12, fontweight=400)
    ax.set_title('right', loc='right', fontsize=12, fontweight=400)
# Mutation info: Added projection = rectilinear (Call plt.subplot)