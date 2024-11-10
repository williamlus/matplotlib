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

def test_noscale_15_mutated():
    X, Y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    Z = np.sin(Y ** 2)
    fig, ax = plt.subplots()
    ax.imshow(Z, cmap='gray', interpolation='none', aspect='equal')