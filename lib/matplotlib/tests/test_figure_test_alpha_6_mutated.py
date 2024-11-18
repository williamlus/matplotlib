import copy
from datetime import datetime
import io
import pickle
import platform
from threading import Timer
from types import SimpleNamespace
import warnings
import numpy as np
import pytest
from PIL import Image
import matplotlib as mpl
from matplotlib import gridspec
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.axes import Axes
from matplotlib.backend_bases import KeyEvent, MouseEvent
from matplotlib.figure import Figure, FigureBase
from matplotlib.layout_engine import ConstrainedLayoutEngine, TightLayoutEngine, PlaceHolderLayoutEngine
from matplotlib.ticker import AutoMinorLocator, FixedFormatter, ScalarFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

@image_comparison(['alpha_background'], extensions=['png', 'svg'], savefig_kwarg={'facecolor': (0, 1, 0.4), 'edgecolor': 'none'})
def test_alpha_6_mutated():
    fig = plt.figure(figsize=[2, 1], layout='compressed')
    fig.set_facecolor((0, 1, 0.4))
    fig.patch.set_alpha(0.4)
    fig.patches.append(mpl.patches.CirclePolygon([20, 20], radius=15, alpha=0.6, facecolor='red'))
# Mutation info: Added layout = compressed (Call plt.figure)