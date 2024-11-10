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

def test_figure_5_mutated():
    fig = plt.figure('today')
    ax = fig.add_subplot()
    ax.set_title(fig.get_label())
    ax.plot(np.arange(5))
    plt.figure('tomorrow', layout='tight')
    plt.plot([0, 1], [1, 0], 'r')
    plt.figure('today')
    plt.close('tomorrow')