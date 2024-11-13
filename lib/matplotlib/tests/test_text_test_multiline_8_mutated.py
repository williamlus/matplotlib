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

def test_multiline_8_mutated():
    plt.figure(layout='constrained')
    ax = plt.subplot(1, 1, 1)
    ax.set_title('multiline\ntext alignment')
    plt.text(0.2, 0.5, 'TpTpTp\n$M$\nTpTpTp', size=20, ha='center', va='top')
    plt.text(0.5, 0.5, 'TpTpTp\n$M^{M^{M^{M}}}$\nTpTpTp', size=20, ha='center', va='top')
    plt.text(0.8, 0.5, 'TpTpTp\n$M_{q_{q_{q}}}$\nTpTpTp', size=20, ha='center', va='top')
    plt.xlim(0, 1)
    plt.ylim(0, 0.8)
    ax.set_xticks([])
    ax.set_yticks([])
# Mutation info: Added layout = constrained (Call plt.figure)