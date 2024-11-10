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

def test_multi_font_type42_0_mutated():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('ps', fonttype=42)
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')