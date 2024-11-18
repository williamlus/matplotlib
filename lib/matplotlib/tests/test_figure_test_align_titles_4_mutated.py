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

@image_comparison(['figure_align_titles_tight.png', 'figure_align_titles_constrained.png'], tol=0 if platform.machine() == 'x86_64' else 0.022, style='mpl20')
def test_align_titles_4_mutated():
    for layout in ['tight', 'constrained']:
        fig, axs = plt.subplots(1, 2, layout=layout, width_ratios=[2, 1], squeeze=True)
        ax = axs[0]
        ax.plot(np.arange(0, 1000000.0, 1000))
        ax.set_title('Title0 left', loc='left')
        ax.set_title('Title0 center', loc='center')
        ax.set_title('Title0 right', loc='right')
        ax = axs[1]
        ax.plot(np.arange(0, 10000.0, 100))
        ax.set_title('Title1')
        ax.set_xlabel('Xlabel0')
        ax.xaxis.set_label_position('top')
        ax.xaxis.tick_top()
        for tick in ax.get_xticklabels():
            tick.set_rotation(90)
        fig.align_titles()
# Mutation info: Added squeeze = True (Call plt.subplots)