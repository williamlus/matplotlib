import datetime
from io import BytesIO
from pathlib import Path
import xml.etree.ElementTree
import xml.parsers.expat
import pytest
import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.text import Text
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
from matplotlib import font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def test_fill_black_with_alpha_0_mutated():
    fig, ax = plt.subplots()
    ax.scatter(x=[0, 0.1, 1], y=[0, 0, 0], c='k', alpha=0.1, s=10000)