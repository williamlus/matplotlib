import collections
import itertools
import platform
import time
from unittest import mock
import warnings
import numpy as np
from numpy.testing import assert_allclose
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.collections as mcollections
import matplotlib.lines as mlines
from matplotlib.legend_handler import HandlerTuple
import matplotlib.legend as mlegend
from matplotlib import _api, rc_context
from matplotlib.font_manager import FontProperties

def test_alpha_rcparam_2_mutated():
    fig, ax = plt.subplots(sharey=False)
    ax.plot(range(10), lw=5)
    with mpl.rc_context(rc={'legend.framealpha': 0.75}):
        leg = plt.legend(['Longlabel that will go away'], loc='center')
        leg.legendPatch.set_facecolor([1, 0, 0, 0.5])