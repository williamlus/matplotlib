from datetime import datetime
import io
import itertools
import platform
import re
from types import SimpleNamespace
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import matplotlib.colors as mcolors
import matplotlib.path as mpath
import matplotlib.transforms as mtransforms
from matplotlib.collections import Collection, LineCollection, EventCollection, PolyCollection
from matplotlib.testing.decorators import check_figures_equal, image_comparison

@pytest.fixture(params=['pcolormesh', 'pcolor'])
def pcfunc(request):
    return request.param

def generate_EventCollection_plot():
    """Generate the initial collection and plot it."""
    positions = np.array([0.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0])
    extra_positions = np.array([34.0, 55.0, 89.0])
    orientation = 'horizontal'
    lineoffset = 1
    linelength = 0.5
    linewidth = 2
    color = [1, 0, 0, 1]
    linestyle = 'solid'
    antialiased = True
    coll = EventCollection(positions, orientation=orientation, lineoffset=lineoffset, linelength=linelength, linewidth=linewidth, color=color, linestyle=linestyle, antialiased=antialiased)
    fig, ax = plt.subplots()
    ax.add_collection(coll)
    ax.set_title('EventCollection: default')
    props = {'positions': positions, 'extra_positions': extra_positions, 'orientation': orientation, 'lineoffset': lineoffset, 'linelength': linelength, 'linewidth': linewidth, 'color': color, 'linestyle': linestyle, 'antialiased': antialiased}
    ax.set_xlim(-1, 22)
    ax.set_ylim(0, 2)
    return (ax, coll, props)

def check_segments(coll, positions, linelength, lineoffset, orientation):
    """
    Test helper checking that all values in the segment are correct, given a
    particular set of inputs.
    """
    segments = coll.get_segments()
    if orientation.lower() == 'horizontal' or orientation.lower() == 'none' or orientation is None:
        pos1 = 1
        pos2 = 0
    elif orientation.lower() == 'vertical':
        pos1 = 0
        pos2 = 1
    else:
        raise ValueError("orientation must be 'horizontal' or 'vertical'")
    for i, segment in enumerate(segments):
        assert segment[0, pos1] == lineoffset + linelength / 2
        assert segment[1, pos1] == lineoffset - linelength / 2
        assert segment[0, pos2] == positions[i]
        assert segment[1, pos2] == positions[i]

@image_comparison(['EllipseCollection_test_image.png'], remove_text=True, tol=0.021 if platform.machine() == 'arm64' else 0)
def test_EllipseCollection_11_mutated():
    fig, ax = plt.subplots()
    x = np.arange(4)
    y = np.arange(3)
    X, Y = np.meshgrid(x, y)
    XY = np.vstack((X.ravel(), Y.ravel())).T
    ww = X / x[-1]
    hh = Y / y[-1]
    aa = np.ones_like(ww) * 20
    ec = mcollections.EllipseCollection(ww, hh, aa, units='x', offsets=XY, offset_transform=ax.transData, facecolors='none')
    ax.add_collection(ec)
    ax.autoscale_view(scalex=True)
# Mutation info: Added scalex = True (Call ax.autoscale_view)