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

@image_comparison(['hatching'], remove_text=True, style='default')
def test_hatching_6_mutated():
    plt.rcParams['text.kerning_factor'] = 6
    fig, ax = plt.subplots()
    patch = plt.Rectangle((0, 0), 0.3, 0.3, hatch='xx', label='Patch\ndefault color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0), 0.3, 0.3, hatch='||', edgecolor='C1', label='Patch\nexplicit color\nfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0, 0.4), 0.3, 0.3, hatch='xx', fill=False, label='Patch\ndefault color\nunfilled')
    ax.add_patch(patch)
    patch = plt.Rectangle((0.33, 0.4), 0.3, 0.3, hatch='||', fill=False, edgecolor='C1', label='Patch\nexplicit color\nunfilled')
    ax.add_patch(patch)
    ax.fill_between([0, 0.15, 0.3], [0.8, 0.8, 0.8], [0.9, 1.0, 0.9], hatch='+', label='Path\ndefault color')
    ax.fill_between([0.33, 0.48, 0.63], [0.8, 0.8, 0.8], [0.9, 1.0, 0.9], hatch='+', edgecolor='C2', label='Path\nexplicit color')
    ax.set_xlim(-0.01, 1.1, emit=False)
    ax.set_ylim(-0.01, 1.1)
    ax.legend(handlelength=4, handleheight=4)
# Mutation info: Added emit = False (Call ax.set_xlim)