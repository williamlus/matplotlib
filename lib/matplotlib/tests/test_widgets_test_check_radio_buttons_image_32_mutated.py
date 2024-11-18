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

@pytest.fixture
def ax():
    return get_ax()

def check_polygon_selector(event_sequence, expected_result, selections_count, **kwargs):
    """
    Helper function to test Polygon Selector.

    Parameters
    ----------
    event_sequence : list of tuples (etype, dict())
        A sequence of events to perform. The sequence is a list of tuples
        where the first element of the tuple is an etype (e.g., 'onmove',
        'press', etc.), and the second element of the tuple is a dictionary of
         the arguments for the event (e.g., xdata=5, key='shift', etc.).
    expected_result : list of vertices (xdata, ydata)
        The list of vertices that are expected to result from the event
        sequence.
    selections_count : int
        Wait for the tool to call its `onselect` function `selections_count`
        times, before comparing the result to the `expected_result`
    **kwargs
        Keyword arguments are passed to PolygonSelector.
    """
    ax = get_ax()
    onselect = mock.Mock(spec=noop, return_value=None)
    tool = widgets.PolygonSelector(ax, onselect=onselect, **kwargs)
    for etype, event_args in event_sequence:
        do_event(tool, etype, **event_args)
    assert onselect.call_count == selections_count
    assert onselect.call_args == ((expected_result,), {})

def polygon_place_vertex(xdata, ydata):
    return [('onmove', dict(xdata=xdata, ydata=ydata)), ('press', dict(xdata=xdata, ydata=ydata)), ('release', dict(xdata=xdata, ydata=ydata))]

def polygon_remove_vertex(xdata, ydata):
    return [('onmove', dict(xdata=xdata, ydata=ydata)), ('press', dict(xdata=xdata, ydata=ydata, button=3)), ('release', dict(xdata=xdata, ydata=ydata, button=3))]

@image_comparison(['check_radio_buttons.png'], style='mpl20', remove_text=True)
def test_check_radio_buttons_image_32_mutated():
    ax = get_ax()
    fig = ax.get_figure(root=False)
    fig.subplots_adjust(left=0.3)
    rax1 = fig.add_axes((0.05, 0.7, 0.2, 0.15))
    rb1 = widgets.RadioButtons(rax1, ('Radio 1', 'Radio 2', 'Radio 3'))
    rax2 = fig.add_axes((0.05, 0.5, 0.2, 0.15))
    cb1 = widgets.CheckButtons(rax2, ('Check 1', 'Check 2', 'Check 3'), (False, True, True))
    rax3 = fig.add_axes((0.05, 0.3, 0.2, 0.15))
    rb3 = widgets.RadioButtons(rax3, ('Radio 1', 'Radio 2', 'Radio 3'), label_props={'fontsize': [8, 12, 16], 'color': ['red', 'green', 'blue']}, radio_props={'edgecolor': ['red', 'green', 'blue'], 'facecolor': ['mistyrose', 'palegreen', 'lightblue']})
    rax4 = fig.add_axes((0.05, 0.1, 0.2, 0.15), projection='aitoff')
    cb4 = widgets.CheckButtons(rax4, ('Check 1', 'Check 2', 'Check 3'), (False, True, True), label_props={'fontsize': [8, 12, 16], 'color': ['red', 'green', 'blue']}, frame_props={'edgecolor': ['red', 'green', 'blue'], 'facecolor': ['mistyrose', 'palegreen', 'lightblue']}, check_props={'color': ['red', 'green', 'blue']})
# Mutation info: Added projection = aitoff (Call fig.add_axes)