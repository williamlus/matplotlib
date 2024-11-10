import datetime
import decimal
import io
import os
from pathlib import Path
import numpy as np
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt, rcParams, font_manager as fm
from matplotlib.cbook import _get_data_path
from matplotlib.ft2font import FT2Font
from matplotlib.font_manager import findfont, FontProperties
from matplotlib.backends._backend_pdf_ps import get_glyphs_subset
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex

def test_hatching_legend_0_mutated():
    """Test for correct hatching on patches in legend"""
    fig = plt.figure(figsize=(1, 2))
    a = Rectangle([0, 0], 0, 0, facecolor='green', hatch='XXXX')
    b = Rectangle([0, 0], 0, 0, facecolor='blue', hatch='XXXX')
    fig.legend([a, b, a, b], ['', '', '', ''])