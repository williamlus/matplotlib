from collections import Counter
from pathlib import Path
import io
import re
import tempfile
import numpy as np
import pytest
from matplotlib import cbook, path, patheffects, font_manager as fm
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.testing._markers import needs_ghostscript, needs_usetex
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib as mpl
import matplotlib.collections as mcollections
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def test_transparency_0_mutated():
    fig, ax = plt.subplots()
    ax.set_axis_off()
    ax.plot([0, 1], color='r', alpha=0)
    ax.text(0.5, 0.5, 'foo', color='r', alpha=0)