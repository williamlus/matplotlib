import datetime
import platform
import re
from unittest import mock
import contourpy
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_almost_equal_nulp
import matplotlib as mpl
from matplotlib import pyplot as plt, rc_context, ticker
from matplotlib.colors import LogNorm, same_color
import matplotlib.patches as mpatches
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import pytest

@image_comparison(['contour_disconnected_segments'], remove_text=True, style='mpl20', extensions=['png'])
def test_contour_label_with_disconnected_segments_16_mutated():
    x, y = np.mgrid[-1:1:21j, -1:1:21j]
    z = 1 / np.sqrt(0.01 + (x + 0.3) ** 2 + y ** 2)
    z += 1 / np.sqrt(0.01 + (x - 0.3) ** 2 + y ** 2)
    plt.figure()
    cs = plt.contour(x, y, z, levels=[7])
    cs.clabel(manual=True)
# Mutation info: manual = [(0.2, 0.1)] -> manual = True (Call cs.clabel)