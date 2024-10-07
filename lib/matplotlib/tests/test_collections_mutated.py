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
@image_comparison(['EventCollection_plot__default'])
def mutated_test__EventCollection__get_props():
    _, coll, props = generate_EventCollection_plot()
    check_segments(coll, props['positions'], props['linelength'], props['lineoffset'], props['orientation'])
    np.testing.assert_array_equal(props['positions'], coll.get_positions())
    assert props['orientation'] == coll.get_orientation()
    assert coll.is_horizontal()
    assert props['linelength'] == coll.get_linelength()
    assert props['lineoffset'] == coll.get_lineoffset()
    assert coll.get_linestyle() == [(0, None)]
    for color in [coll.get_color(), *coll.get_colors()]:
        np.testing.assert_array_equal(color, props['color'])
@image_comparison(['EventCollection_plot__set_positions'])
def mutated_test__EventCollection__set_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'], props['extra_positions']])
    coll.set_positions(new_positions)
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: set_positions')
    splt.set_xlim(-1, 90)
@image_comparison(['EventCollection_plot__add_positions'])
def mutated_test__EventCollection__add_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'], props['extra_positions'][0]])
    coll.switch_orientation()
    coll.add_positions(props['extra_positions'][0])
    coll.switch_orientation()
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: add_positions')
    splt.set_xlim(-1, 35)
@image_comparison(['EventCollection_plot__append_positions'])
def mutated_test__EventCollection__append_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'], props['extra_positions'][2]])
    coll.append_positions(props['extra_positions'][2])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: append_positions')
    splt.set_xlim(-1, 90)
@image_comparison(['EventCollection_plot__extend_positions'])
def mutated_test__EventCollection__extend_positions():
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'], props['extra_positions'][1:]])
    coll.extend_positions(props['extra_positions'][1:])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: extend_positions')
    splt.set_xlim(-1, 90)
@image_comparison(['EventCollection_plot__switch_orientation'])
def mutated_test__EventCollection__switch_orientation():
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.switch_orientation()
    assert new_orientation == coll.get_orientation()
    assert not coll.is_horizontal()
    new_positions = coll.get_positions()
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], new_orientation)
    splt.set_title('EventCollection: switch_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)
@image_comparison(['EventCollection_plot__switch_orientation__2x'])
def mutated_test__EventCollection__switch_orientation_2x():
    """
    Check that calling switch_orientation twice sets the orientation back to
    the default.
    """
    splt, coll, props = generate_EventCollection_plot()
    coll.switch_orientation()
    coll.switch_orientation()
    new_positions = coll.get_positions()
    assert props['orientation'] == coll.get_orientation()
    assert coll.is_horizontal()
    np.testing.assert_array_equal(props['positions'], new_positions)
    check_segments(coll, new_positions, props['linelength'], props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: switch_orientation 2x')
@image_comparison(['EventCollection_plot__set_orientation'])
def mutated_test__EventCollection__set_orientation():
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.set_orientation(new_orientation)
    assert new_orientation == coll.get_orientation()
    assert not coll.is_horizontal()
    check_segments(coll, props['positions'], props['linelength'], props['lineoffset'], new_orientation)
    splt.set_title('EventCollection: set_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)
@image_comparison(['EventCollection_plot__set_linelength'])
def mutated_test__EventCollection__set_linelength():
    splt, coll, props = generate_EventCollection_plot()
    new_linelength = 15
    coll.set_linelength(new_linelength)
    assert new_linelength == coll.get_linelength()
    check_segments(coll, props['positions'], new_linelength, props['lineoffset'], props['orientation'])
    splt.set_title('EventCollection: set_linelength')
    splt.set_ylim(-20, 20)
@image_comparison(['EventCollection_plot__set_lineoffset'])
def mutated_test__EventCollection__set_lineoffset():
    splt, coll, props = generate_EventCollection_plot()
    new_lineoffset = -5.0
    coll.set_lineoffset(new_lineoffset)
    assert new_lineoffset == coll.get_lineoffset()
    check_segments(coll, props['positions'], props['linelength'], new_lineoffset, props['orientation'])
    splt.set_title('EventCollection: set_lineoffset')
    splt.set_ylim(-6, -4)
@image_comparison(['EventCollection_plot__set_linestyle', 'EventCollection_plot__set_linestyle', 'EventCollection_plot__set_linewidth'])
def mutated_test__EventCollection__set_prop():
    for prop, value, expected in [('linestyle', 'dashed', [(0, (6.0, 6.0))]), ('linestyle', (0, (6.0, 6.0)), [(0, (6.0, 6.0))]), ('linewidth', 5, 5)]:
        splt, coll, _ = generate_EventCollection_plot()
        coll.set(**{prop: value})
        assert plt.getp(coll, prop) == expected
        splt.set_title(f'EventCollection: set_{prop}')
@image_comparison(['EventCollection_plot__set_color'])
def mutated_test__EventCollection__set_color():
    splt, coll, _ = generate_EventCollection_plot()
    new_color = np.array([0, 1, 1, 1])
    coll.set_color(new_color)
    for color in [coll.get_color(), *coll.get_colors()]:
        np.testing.assert_array_equal(color, new_color)
    splt.set_title('EventCollection: set_color')
@image_comparison(['EllipseCollection_test_image.png'], remove_text=True, tol=0.021 if platform.machine() == 'arm64' else 0)
def mutated_test_EllipseCollection():
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
    ax.autoscale_view()
@image_comparison(['polycollection_close.png'], remove_text=True, style='mpl20')
def mutated_test_polycollection_close():
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
    ax.set_zlim3d(0, 3)
    ax.set_ylim3d(0, 4)
@image_comparison(['regularpolycollection_rotate.png'], remove_text=True)
def mutated_test_regularpolycollection_rotate():
    xx, yy = np.mgrid[:10, :10]
    xy_points = np.transpose([xx.flatten(), yy.flatten()])
    rotations = np.linspace(0, 2 * np.pi, len(xy_points))
    fig, ax = plt.subplots()
    for xy, alpha in zip(xy_points, rotations):
        col = mcollections.RegularPolyCollection(4, sizes=(100,), rotation=alpha, offsets=[xy], offset_transform=ax.transData)
        ax.add_collection(col, autolim=True)
    ax.autoscale_view()
@image_comparison(['regularpolycollection_scale.png'], remove_text=True)
def mutated_test_regularpolycollection_scale():

    class SquareCollection(mcollections.RegularPolyCollection):

        def __init__(self, **kwargs):
            super().__init__(4, rotation=np.pi / 4.0, **kwargs)

        def get_transform(self):
            """Return transform scaling circle areas to data space."""
            ax = self.axes
            pts2pixels = 72.0 / ax.get_figure(root=True).dpi
            scale_x = pts2pixels * ax.bbox.width / ax.viewLim.width
            scale_y = pts2pixels * ax.bbox.height / ax.viewLim.height
            return mtransforms.Affine2D().scale(scale_x, scale_y)
    fig, ax = plt.subplots()
    xy = [(0, 0)]
    circle_areas = [np.pi / 2]
    squares = SquareCollection(sizes=circle_areas, offsets=xy, offset_transform=ax.transData)
    ax.add_collection(squares, autolim=True)
    ax.axis([-1, 1, -1, 1])
@image_comparison(['size_in_xy.png'], remove_text=True)
def mutated_test_size_in_xy():
    fig, ax = plt.subplots()
    widths, heights, angles = ((10, 10), 10, 0)
    widths = (10, 10)
    coords = [(10, 10), (15, 15)]
    e = mcollections.EllipseCollection(widths, heights, angles, units='xy', offsets=coords, offset_transform=ax.transData)
    ax.add_collection(e)
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 30)
@image_comparison(['cap_and_joinstyle.png'])
def mutated_test_cap_and_joinstyle_image():
    fig, ax = plt.subplots()
    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([-0.5, 2.5])
    x = np.array([0.0, 1.0, 0.5])
    ys = np.array([[0.0], [0.5], [1.0]]) + np.array([[0.0, 0.0, 1.0]])
    segs = np.zeros((3, 3, 2))
    segs[:, :, 0] = x
    segs[:, :, 1] = ys
    line_segments = LineCollection(segs, linewidth=[10, 15, 20])
    line_segments.set_capstyle('round')
    line_segments.set_joinstyle('miter')
    ax.add_collection(line_segments)
    ax.set_title('Line collection with customized caps and joinstyle')
@image_comparison(['scatter_post_alpha.png'], remove_text=True, style='default')
def mutated_test_scatter_post_alpha():
    fig, ax = plt.subplots()
    sc = ax.scatter(range(5), range(5), c=range(5))
    sc.set_alpha(0.1)
@image_comparison(baseline_images=['test_check_masked_offsets'], extensions=['png'], remove_text=True, style='mpl20')
def mutated_test_check_masked_offsets():
    unmasked_x = [datetime(2022, 12, 15, 4, 49, 52), datetime(2022, 12, 15, 4, 49, 53), datetime(2022, 12, 15, 4, 49, 54), datetime(2022, 12, 15, 4, 49, 55), datetime(2022, 12, 15, 4, 49, 56)]
    masked_y = np.ma.array([1, 2, 3, 4, 5], mask=[0, 1, 1, 0, 0])
    fig, ax = plt.subplots()
    ax.scatter(unmasked_x, masked_y)
