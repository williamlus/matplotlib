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

def test_bbox_clipping_0_mutated():
    plt.text(0.9, 0.2, 'Is bbox clipped?', backgroundcolor='r', clip_on=True)
    t = plt.text(0.9, 0.5, 'Is fancy bbox clipped?', clip_on=True)
    t.set_bbox({'boxstyle': 'round, pad=0.1'})