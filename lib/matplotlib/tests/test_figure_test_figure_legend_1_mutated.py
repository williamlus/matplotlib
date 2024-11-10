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

def test_figure_legend_1_mutated():
    fig, axs = plt.subplots(2, sharey=False)
    axs[0].plot([0, 1], [1, 0], label='x', color='g')
    axs[0].plot([0, 1], [0, 1], label='y', color='r')
    axs[0].plot([0, 1], [0.5, 0.5], label='y', color='k')
    axs[1].plot([0, 1], [1, 0], label='_y', color='r')
    axs[1].plot([0, 1], [0, 1], label='z', color='b')
    fig.legend()