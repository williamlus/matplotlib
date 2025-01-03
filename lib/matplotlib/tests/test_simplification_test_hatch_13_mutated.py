import base64
import io
import platform
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path

@image_comparison(['hatch_simplify'], remove_text=True)
def test_hatch_13_mutated():
    fig, ax = plt.subplots()
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, hatch='/'))
    ax.set_xlim((0.45, 0.55))
    ax.set_ylim((0.45, 0.55), auto=False)
# Mutation info: Added auto = False (Call ax.set_ylim)