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

def test_subfigure_20_mutated():
    np.random.seed(19680801)
    fig = plt.figure(layout=None)
    sub = fig.subfigures(1, 2)
    axs = sub[0].subplots(2, 2)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[0].colorbar(pc, ax=axs)
    sub[0].suptitle('Left Side')
    sub[0].set_facecolor('white')
    axs = sub[1].subplots(1, 3)
    for ax in axs.flat:
        pc = ax.pcolormesh(np.random.randn(30, 30), vmin=-2, vmax=2)
    sub[1].colorbar(pc, ax=axs, location='bottom')
    sub[1].suptitle('Right Side')
    sub[1].set_facecolor('white')
    fig.suptitle('Figure suptitle', fontsize='xx-large')
    leg = fig.legend(handles=[plt.Line2D([0], [0], label='Line{}'.format(i)) for i in range(5)], loc='center')
    sub[0].set_zorder(leg.get_zorder() - 1)
    sub[1].set_zorder(leg.get_zorder() + 1)
# Mutation info: layout = <ast.Constant object at 0x7fc056f77e90> -> layout = None (Call plt.figure)