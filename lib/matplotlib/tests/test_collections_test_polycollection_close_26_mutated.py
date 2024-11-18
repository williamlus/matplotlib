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

@image_comparison(['polycollection_close.png'], remove_text=True, style='mpl20')
def test_polycollection_close_26_mutated():
    from mpl_toolkits.mplot3d import Axes3D
    plt.rcParams['axes3d.automargin'] = True
    vertsQuad = [[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]], [[0.0, 1.0], [2.0, 3.0], [2.0, 2.0], [1.0, 1.0]], [[2.0, 2.0], [2.0, 3.0], [4.0, 1.0], [3.0, 1.0]], [[3.0, 0.0], [3.0, 1.0], [4.0, 1.0], [4.0, 0.0]]]
    fig = plt.figure()
    ax = fig.add_axes(Axes3D(fig))
    colors = ['r', 'g', 'b', 'y', 'k']
    zpos = list(range(5))
    poly = mcollections.PolyCollection(vertsQuad * len(zpos), linewidth=0.25)
    poly.set_alpha(0.7)
    zs = []
    cs = []
    for z, c in zip(zpos, colors):
        zs.extend([z] * len(vertsQuad))
        cs.extend([c] * len(vertsQuad))
    poly.set_color(cs)
    ax.add_collection3d(poly, zs=zs, zdir='y')
    ax.set_xlim3d(0, 4)
    ax.set_zlim3d(0, 3, auto=True)
    ax.set_ylim3d(0, 4)
# Mutation info: Added auto = True (Call ax.set_zlim3d)