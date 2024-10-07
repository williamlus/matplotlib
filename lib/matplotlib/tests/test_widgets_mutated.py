import functools
import io
import operator
from unittest import mock
import matplotlib as mpl
from matplotlib.backend_bases import MouseEvent
import matplotlib.colors as mcolors
import matplotlib.widgets as widgets
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing.widgets import click_and_drag, do_event, get_ax, mock_event, noop
import numpy as np
from numpy.testing import assert_allclose
import pytest
@image_comparison(['check_radio_buttons.png'], style='mpl20', remove_text=True)
def mutated_test_check_radio_buttons_image():
    ax = get_ax()
    fig = ax.get_figure(root=False)
    fig.subplots_adjust(left=0.3)
    rax1 = fig.add_axes((0.05, 0.7, 0.2, 0.15))
    rb1 = widgets.RadioButtons(rax1, ('Radio 1', 'Radio 2', 'Radio 3'))
    rax2 = fig.add_axes((0.05, 0.5, 0.2, 0.15))
    cb1 = widgets.CheckButtons(rax2, ('Check 1', 'Check 2', 'Check 3'), (False, True, True))
    rax3 = fig.add_axes((0.05, 0.3, 0.2, 0.15))
    rb3 = widgets.RadioButtons(rax3, ('Radio 1', 'Radio 2', 'Radio 3'), label_props={'fontsize': [8, 12, 16], 'color': ['red', 'green', 'blue']}, radio_props={'edgecolor': ['red', 'green', 'blue'], 'facecolor': ['mistyrose', 'palegreen', 'lightblue']})
    rax4 = fig.add_axes((0.05, 0.1, 0.2, 0.15))
    cb4 = widgets.CheckButtons(rax4, ('Check 1', 'Check 2', 'Check 3'), (False, True, True), label_props={'fontsize': [8, 12, 16], 'color': ['red', 'green', 'blue']}, frame_props={'edgecolor': ['red', 'green', 'blue'], 'facecolor': ['mistyrose', 'palegreen', 'lightblue']}, check_props={'color': ['red', 'green', 'blue']})
