import contextlib
from collections import namedtuple
import datetime
from decimal import Decimal
from functools import partial
import inspect
import io
from itertools import product
import platform
from types import SimpleNamespace
import dateutil.tz
import numpy as np
from numpy import ma
from cycler import cycler
import pytest
import matplotlib
import matplotlib as mpl
from matplotlib import rc_context, patheffects
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import matplotlib.font_manager as mfont_manager
import matplotlib.markers as mmarkers
import matplotlib.patches as mpatches
import matplotlib.path as mpath
from matplotlib.projections.geo import HammerAxes
from matplotlib.projections.polar import PolarAxes
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.ticker as mticker
import matplotlib.transforms as mtransforms
import mpl_toolkits.axisartist as AA
from numpy.testing import assert_allclose, assert_array_equal, assert_array_almost_equal
from matplotlib.testing.decorators import image_comparison, check_figures_equal, remove_ticks_and_titles
from matplotlib.testing._markers import needs_usetex
@image_comparison(['formatter_ticker_001', 'formatter_ticker_002', 'formatter_ticker_003', 'formatter_ticker_004', 'formatter_ticker_005'], tol=0.031 if platform.machine() == 'arm64' else 0)
def mutated_test_formatter_ticker():
    import matplotlib.testing.jpl_units as units
    units.register()
    matplotlib.rcParams['lines.markeredgewidth'] = 30
    xdata = [x * units.sec for x in range(10)]
    ydata1 = [(1.5 * y - 0.5) * units.km for y in range(10)]
    ydata2 = [(1.75 * y - 1.0) * units.km for y in range(10)]
    ax = plt.figure().subplots()
    ax.set_xlabel('x-label 001')
    ax = plt.figure().subplots()
    ax.set_xlabel('x-label 001')
    ax.plot(xdata, ydata1, color='blue', xunits='sec')
    ax = plt.figure().subplots()
    ax.set_xlabel('x-label 001')
    ax.plot(xdata, ydata1, color='blue', xunits='sec')
    ax.set_xlabel('x-label 003')
    ax = plt.figure().subplots()
    ax.plot(xdata, ydata1, color='blue', xunits='sec')
    ax.plot(xdata, ydata2, color='green', xunits='hour')
    ax.set_xlabel('x-label 004')
    ax = plt.figure().subplots()
    ax.plot(xdata, ydata1, color='blue', xunits='sec')
    ax.plot(xdata, ydata2, color='green', xunits='hour')
    ax.set_xlabel('x-label 005')
    ax.autoscale_view()
@image_comparison(['twin_axis_locators_formatters'])
def mutated_test_twin_axis_locators_formatters():
    vals = np.linspace(0, 1, num=5, endpoint=True)
    locs = np.sin(np.pi * vals / 2.0)
    majl = plt.FixedLocator(locs)
    minl = plt.FixedLocator([0.1, 0.2, 0.3])
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot([0.1, 100], [0, 1])
    ax1.yaxis.set_major_locator(majl)
    ax1.yaxis.set_minor_locator(minl)
    ax1.yaxis.set_major_formatter(plt.FormatStrFormatter('%08.2lf'))
    ax1.yaxis.set_minor_formatter(plt.FixedFormatter(['tricks', 'mind', 'jedi']))
    ax1.xaxis.set_major_locator(plt.LinearLocator())
    ax1.xaxis.set_minor_locator(plt.FixedLocator([15, 35, 55, 75]))
    ax1.xaxis.set_major_formatter(plt.FormatStrFormatter('%05.2lf'))
    ax1.xaxis.set_minor_formatter(plt.FixedFormatter(['c', '3', 'p', 'o']))
    ax1.twiny()
    ax1.twinx()
@image_comparison(['twin_autoscale.png'], tol=0.009 if platform.machine() == 'arm64' else 0)
def mutated_test_twinx_axis_scales():
    x = np.array([0, 0.5, 1])
    y = 0.5 * x
    x2 = np.array([0, 1, 2])
    y2 = 2 * x2
    fig = plt.figure()
    ax = fig.add_axes((0, 0, 1, 1), autoscalex_on=False, autoscaley_on=False)
    ax.plot(x, y, color='blue', lw=10)
    ax2 = plt.twinx(ax)
    ax2.plot(x2, y2, 'r--', lw=5)
    ax.margins(0, 0)
    ax2.margins(0, 0)
@image_comparison(['autoscale_tiny_range'], remove_text=True)
def mutated_test_autoscale_tiny_range():
    fig, axs = plt.subplots(2, 2)
    for i, ax in enumerate(axs.flat):
        y1 = 10 ** (-11 - i)
        ax.plot([0, 1], [1, 1 + y1])
@image_comparison(['sticky_tolerance.png'], remove_text=True, style='mpl20')
def mutated_test_sticky_tolerance():
    fig, axs = plt.subplots(2, 2)
    width = 0.1
    axs.flat[0].bar(x=0, height=width, bottom=20000.6)
    axs.flat[0].bar(x=1, height=width, bottom=20000.1)
    axs.flat[1].bar(x=0, height=-width, bottom=20000.6)
    axs.flat[1].bar(x=1, height=-width, bottom=20000.1)
    axs.flat[2].barh(y=0, width=-width, left=-20000.6)
    axs.flat[2].barh(y=1, width=-width, left=-20000.1)
    axs.flat[3].barh(y=0, width=width, left=-20000.6)
    axs.flat[3].barh(y=1, width=width, left=-20000.1)
@image_comparison(['sticky_tolerance_cf.png'], remove_text=True, style='mpl20')
def mutated_test_sticky_tolerance_contourf():
    fig, ax = plt.subplots()
    x = y = [14496.71, 14496.75]
    data = [[0, 1], [2, 3]]
    ax.contourf(x, y, data)
@image_comparison(['offset_points'], remove_text=True)
def mutated_test_basic_annotate():
    t = np.arange(0.0, 5.0, 0.01)
    s = np.cos(2.0 * np.pi * t)
    fig = plt.figure()
    ax = fig.add_subplot(autoscale_on=False, xlim=(-1, 5), ylim=(-3, 5))
    line, = ax.plot(t, s, lw=3, color='purple')
    ax.annotate('local max', xy=(3, 1), xycoords='data', xytext=(3, 3), textcoords='offset points')
@image_comparison(['arrow_simple.png'], remove_text=True)
def mutated_test_arrow_simple():
    length_includes_head = (True, False)
    shape = ('full', 'left', 'right')
    head_starts_at_zero = (True, False)
    kwargs = product(length_includes_head, shape, head_starts_at_zero)
    fig, axs = plt.subplots(3, 4)
    for i, (ax, kwarg) in enumerate(zip(axs.flat, kwargs)):
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        length_includes_head, shape, head_starts_at_zero = kwarg
        theta = 2 * np.pi * i / 12
        ax.arrow(0, 0, np.sin(theta), np.cos(theta), width=theta / 100, length_includes_head=length_includes_head, shape=shape, head_starts_at_zero=head_starts_at_zero, head_width=theta / 10, head_length=theta / 10)
@image_comparison(['fill_units.png'], savefig_kwarg={'dpi': 60})
def mutated_test_fill_units():
    import matplotlib.testing.jpl_units as units
    units.register()
    t = units.Epoch('ET', dt=datetime.datetime(2009, 4, 27))
    value = 10.0 * units.deg
    day = units.Duration('ET', 24.0 * 60.0 * 60.0)
    dt = np.arange('2009-04-27', '2009-04-29', dtype='datetime64[D]')
    dtn = mdates.date2num(dt)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.plot([t], [value], yunits='deg', color='red')
    ind = [0, 0, 1, 1]
    ax1.fill(dtn[ind], [0.0, 0.0, 90.0, 0.0], 'b')
    ax2.plot([t], [value], yunits='deg', color='red')
    ax2.fill([t, t, t + day, t + day], [0.0, 0.0, 90.0, 0.0], 'b')
    ax3.plot([t], [value], yunits='deg', color='red')
    ax3.fill(dtn[ind], [0 * units.deg, 0 * units.deg, 90 * units.deg, 0 * units.deg], 'b')
    ax4.plot([t], [value], yunits='deg', color='red')
    ax4.fill([t, t, t + day, t + day], [0 * units.deg, 0 * units.deg, 90 * units.deg, 0 * units.deg], facecolor='blue')
    fig.autofmt_xdate()
@image_comparison(['single_point', 'single_point'])
def mutated_test_single_point():
    matplotlib.rcParams['lines.marker'] = 'o'
    matplotlib.rcParams['axes.grid'] = True
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot([0], [0], 'o')
    ax2.plot([1], [1], 'o')
    data = {'a': [0], 'b': [1]}
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot('a', 'a', 'o', data=data)
    ax2.plot('b', 'b', 'o', data=data)
@image_comparison(['single_date.png'], style='mpl20')
def mutated_test_single_date():
    plt.rcParams['axes.formatter.limits'] = (-7, 7)
    dt = mdates.date2num(np.datetime64('0000-12-31'))
    time1 = [721964.0]
    data1 = [-65.54]
    fig, ax = plt.subplots(2, 1)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        ax[0].plot_date(time1 + dt, data1, 'o', color='r')
    ax[1].plot(time1, data1, 'o', color='r')
@image_comparison(['aitoff_proj'], extensions=['png'], remove_text=True, style='mpl20')
def mutated_test_aitoff_proj():
    """
    Test aitoff projection ref.:
    https://github.com/matplotlib/matplotlib/pull/14451
    """
    x = np.linspace(-np.pi, np.pi, 20)
    y = np.linspace(-np.pi / 2, np.pi / 2, 20)
    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots(figsize=(8, 4.2), subplot_kw=dict(projection='aitoff'))
    ax.grid()
    ax.plot(X.flat, Y.flat, 'o', markersize=4)
@image_comparison(['axvspan_epoch'])
def mutated_test_axvspan_epoch():
    import matplotlib.testing.jpl_units as units
    units.register()
    t0 = units.Epoch('ET', dt=datetime.datetime(2009, 1, 21))
    tf = units.Epoch('ET', dt=datetime.datetime(2009, 1, 22))
    dt = units.Duration('ET', units.day.convert('sec'))
    ax = plt.gca()
    ax.axvspan(t0, tf, facecolor='blue', alpha=0.25)
    ax.set_xlim(t0 - 5.0 * dt, tf + 5.0 * dt)
@image_comparison(['axhspan_epoch'], tol=0.02)
def mutated_test_axhspan_epoch():
    import matplotlib.testing.jpl_units as units
    units.register()
    t0 = units.Epoch('ET', dt=datetime.datetime(2009, 1, 21))
    tf = units.Epoch('ET', dt=datetime.datetime(2009, 1, 22))
    dt = units.Duration('ET', units.day.convert('sec'))
    ax = plt.gca()
    ax.axhspan(t0, tf, facecolor='blue', alpha=0.25)
    ax.set_ylim(t0 - 5.0 * dt, tf + 5.0 * dt)
@image_comparison(['hexbin_extent.png', 'hexbin_extent.png'], remove_text=True)
def mutated_test_hexbin_extent():
    fig, ax = plt.subplots()
    data = (np.arange(2000) / 2000).reshape((2, 1000))
    x, y = data
    ax.hexbin(x, y, extent=[0.1, 0.3, 0.6, 0.7])
    data = {'x': x, 'y': y}
    fig, ax = plt.subplots()
    ax.hexbin('x', 'y', extent=[0.1, 0.3, 0.6, 0.7], data=data)
@image_comparison(['hexbin_empty.png'], remove_text=True)
def mutated_test_hexbin_empty():
    fig, ax = plt.subplots()
    ax.hexbin([], [])
    ax.hexbin([], [], bins='log')
    ax.hexbin([], [], C=[], reduce_C_function=np.max)
    ax.hexbin([], [], bins=np.arange(10))
@image_comparison(['hexbin_log.png'], style='mpl20')
def mutated_test_hexbin_log():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(19680801)
    n = 100000
    x = np.random.standard_normal(n)
    y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
    y = np.power(2, y * 0.5)
    fig, ax = plt.subplots()
    h = ax.hexbin(x, y, yscale='log', bins='log', marginals=True, reduce_C_function=np.sum)
    plt.colorbar(h)
    assert h.get_offsets().shape == (11558, 2)
@image_comparison(['hexbin_linear.png'], style='mpl20', remove_text=True)
def mutated_test_hexbin_linear():
    np.random.seed(19680801)
    n = 100000
    x = np.random.standard_normal(n)
    y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
    fig, ax = plt.subplots()
    ax.hexbin(x, y, gridsize=(10, 5), marginals=True, reduce_C_function=np.sum)
@image_comparison(['nonfinite_limits'])
def mutated_test_nonfinite_limits():
    x = np.arange(0.0, np.e, 0.01)
    with np.errstate(divide='ignore'):
        y = np.log(x)
    x[len(x) // 2] = np.nan
    fig, ax = plt.subplots()
    ax.plot(x, y)
@image_comparison(['imshow', 'imshow'], remove_text=True, style='mpl20')
def mutated_test_imshow():
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    N = 100
    x, y = np.indices((N, N))
    x -= N // 2
    y -= N // 2
    r = np.sqrt(x ** 2 + y ** 2 - x * y)
    fig, ax = plt.subplots()
    ax.imshow(r)
    data = {'r': r}
    fig, ax = plt.subplots()
    ax.imshow('r', data=data)
@image_comparison(['imshow_clip'], style='mpl20', tol=1.24 if platform.machine() in ('aarch64', 'arm64', 'ppc64le', 's390x') else 0)
def mutated_test_imshow_clip():
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    N = 100
    x, y = np.indices((N, N))
    x -= N // 2
    y -= N // 2
    r = np.sqrt(x ** 2 + y ** 2 - x * y)
    fig, ax = plt.subplots()
    c = ax.contour(r, [N / 4])
    clip_path = mtransforms.TransformedPath(c.get_paths()[0], c.get_transform())
    ax.imshow(r, clip_path=clip_path)
@image_comparison(['polycollection_joinstyle'], remove_text=True)
def mutated_test_polycollection_joinstyle():
    fig, ax = plt.subplots()
    verts = np.array([[1, 1], [1, 2], [2, 2], [2, 1]])
    c = mpl.collections.PolyCollection([verts], linewidths=40)
    ax.add_collection(c)
    ax.set_xbound(0, 3)
    ax.set_ybound(0, 3)
@image_comparison(['fill_between_interpolate'], remove_text=True, tol=0.012 if platform.machine() == 'arm64' else 0)
def mutated_test_fill_between_interpolate():
    x = np.arange(0.0, 2, 0.02)
    y1 = np.sin(2 * np.pi * x)
    y2 = 1.2 * np.sin(4 * np.pi * x)
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(x, y1, x, y2, color='black')
    ax1.fill_between(x, y1, y2, where=y2 >= y1, facecolor='white', hatch='/', interpolate=True)
    ax1.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)
    y2 = np.ma.masked_greater(y2, 1.0)
    y2[0] = np.ma.masked
    ax2.plot(x, y1, x, y2, color='black')
    ax2.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
    ax2.fill_between(x, y1, y2, where=y2 <= y1, facecolor='red', interpolate=True)
@image_comparison(['fill_between_interpolate_decreasing'], style='mpl20', remove_text=True)
def mutated_test_fill_between_interpolate_decreasing():
    p = np.array([724.3, 700, 655])
    t = np.array([9.4, 7, 2.2])
    prof = np.array([7.9, 6.6, 3.8])
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.plot(t, p, 'tab:red')
    ax.plot(prof, p, 'k')
    ax.fill_betweenx(p, t, prof, where=prof < t, facecolor='blue', interpolate=True, alpha=0.4)
    ax.fill_betweenx(p, t, prof, where=prof > t, facecolor='red', interpolate=True, alpha=0.4)
    ax.set_xlim(0, 30)
    ax.set_ylim(800, 600)
@image_comparison(['fill_between_interpolate_nan'], remove_text=True)
def mutated_test_fill_between_interpolate_nan():
    x = np.arange(10)
    y1 = np.asarray([8, 18, np.nan, 18, 8, 18, 24, 18, 8, 18])
    y2 = np.asarray([18, 11, 8, 11, 18, 26, 32, 30, np.nan, np.nan])
    fig, ax = plt.subplots()
    ax.plot(x, y1, c='k')
    ax.plot(x, y2, c='b')
    ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True, alpha=0.5)
    ax.fill_between(x, y1, y2, where=y1 >= y2, facecolor='red', interpolate=True, alpha=0.5)
@image_comparison(['symlog.pdf'])
def mutated_test_symlog():
    x = np.array([0, 1, 2, 4, 6, 9, 12, 24])
    y = np.array([1000000, 500000, 100000, 100, 5, 0, 0, 0])
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_yscale('symlog')
    ax.set_xscale('linear')
    ax.set_ylim(-1, 10000000)
@image_comparison(['symlog2.pdf'], remove_text=True)
def mutated_test_symlog2():
    x = np.arange(-50, 50, 0.001)
    fig, axs = plt.subplots(5, 1)
    for ax, linthresh in zip(axs, [20.0, 2.0, 1.0, 0.1, 0.01]):
        ax.plot(x, x)
        ax.set_xscale('symlog', linthresh=linthresh)
        ax.grid(True)
    axs[-1].set_ylim(-0.1, 0.1)
@image_comparison(['pcolormesh'], remove_text=True)
def mutated_test_pcolormesh():
    plt.rcParams['pcolormesh.snap'] = False
    n = 12
    x = np.linspace(-1.5, 1.5, n)
    y = np.linspace(-1.5, 1.5, n * 2)
    X, Y = np.meshgrid(x, y)
    Qx = np.cos(Y) - np.cos(X)
    Qz = np.sin(Y) + np.sin(X)
    Qx = Qx + 1.1
    Z = np.hypot(X, Y) / 5
    Z = (Z - Z.min()) / np.ptp(Z)
    Zm = ma.masked_where(np.abs(Qz) < 0.5 * np.max(Qz), Z)
    _, (ax1, ax2, ax3) = plt.subplots(1, 3)
    ax1.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=0.5, edgecolors='k')
    ax2.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=2, edgecolors=['b', 'w'])
    ax3.pcolormesh(Qx, Qz, Zm, shading='gouraud')
@image_comparison(['pcolormesh_small'], extensions=['eps'])
def mutated_test_pcolormesh_small():
    n = 3
    x = np.linspace(-1.5, 1.5, n)
    y = np.linspace(-1.5, 1.5, n * 2)
    X, Y = np.meshgrid(x, y)
    Qx = np.cos(Y) - np.cos(X)
    Qz = np.sin(Y) + np.sin(X)
    Qx = Qx + 1.1
    Z = np.hypot(X, Y) / 5
    Z = (Z - Z.min()) / np.ptp(Z)
    Zm = ma.masked_where(np.abs(Qz) < 0.5 * np.max(Qz), Z)
    Zm2 = ma.masked_where(Qz < -0.5 * np.max(Qz), Z)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=0.5, edgecolors='k')
    ax2.pcolormesh(Qx, Qz, Zm[:-1, :-1], lw=2, edgecolors=['b', 'w'])
    ax3.pcolormesh(Qx, Qz, Zm, shading='gouraud')
    ax4.pcolormesh(Qx, Qz, Zm2, shading='gouraud')
    for ax in fig.axes:
        ax.set_axis_off()
@image_comparison(['pcolormesh_alpha'], extensions=['png', 'pdf'], remove_text=True)
def mutated_test_pcolormesh_alpha():
    plt.rcParams['pcolormesh.snap'] = False
    n = 12
    X, Y = np.meshgrid(np.linspace(-1.5, 1.5, n), np.linspace(-1.5, 1.5, n * 2))
    Qx = X
    Qy = Y + np.sin(X)
    Z = np.hypot(X, Y) / 5
    Z = (Z - Z.min()) / np.ptp(Z)
    vir = mpl.colormaps['viridis'].resampled(16)
    colors = vir(np.arange(16))
    colors[:, 3] = 0.5 + 0.5 * np.sin(np.arange(16))
    cmap = mcolors.ListedColormap(colors)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    for ax in (ax1, ax2, ax3, ax4):
        ax.add_patch(mpatches.Rectangle((0, -1.5), 1.5, 3, facecolor=[0.7, 0.1, 0.1, 0.5], zorder=0))
    ax1.pcolormesh(Qx, Qy, Z[:-1, :-1], cmap=vir, alpha=0.4, shading='flat', zorder=1)
    ax2.pcolormesh(Qx, Qy, Z, cmap=vir, alpha=0.4, shading='gouraud', zorder=1)
    ax3.pcolormesh(Qx, Qy, Z[:-1, :-1], cmap=cmap, shading='flat', zorder=1)
    ax4.pcolormesh(Qx, Qy, Z, cmap=cmap, shading='gouraud', zorder=1)
@image_comparison(['pcolormesh_datetime_axis.png'], style='mpl20')
def mutated_test_pcolormesh_datetime_axis():
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, top=0.98, bottom=0.15)
    base = datetime.datetime(2013, 1, 1)
    x = np.array([base + datetime.timedelta(days=d) for d in range(21)])
    y = np.arange(21)
    z1, z2 = np.meshgrid(np.arange(20), np.arange(20))
    z = z1 * z2
    plt.subplot(221)
    plt.pcolormesh(x[:-1], y[:-1], z[:-1, :-1])
    plt.subplot(222)
    plt.pcolormesh(x, y, z)
    x = np.repeat(x[np.newaxis], 21, axis=0)
    y = np.repeat(y[:, np.newaxis], 21, axis=1)
    plt.subplot(223)
    plt.pcolormesh(x[:-1, :-1], y[:-1, :-1], z[:-1, :-1])
    plt.subplot(224)
    plt.pcolormesh(x, y, z)
    for ax in fig.get_axes():
        for label in ax.get_xticklabels():
            label.set_ha('right')
            label.set_rotation(30)
@image_comparison(['pcolor_datetime_axis.png'], style='mpl20')
def mutated_test_pcolor_datetime_axis():
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4, top=0.98, bottom=0.15)
    base = datetime.datetime(2013, 1, 1)
    x = np.array([base + datetime.timedelta(days=d) for d in range(21)])
    y = np.arange(21)
    z1, z2 = np.meshgrid(np.arange(20), np.arange(20))
    z = z1 * z2
    plt.subplot(221)
    plt.pcolor(x[:-1], y[:-1], z[:-1, :-1])
    plt.subplot(222)
    plt.pcolor(x, y, z)
    x = np.repeat(x[np.newaxis], 21, axis=0)
    y = np.repeat(y[:, np.newaxis], 21, axis=1)
    plt.subplot(223)
    plt.pcolor(x[:-1, :-1], y[:-1, :-1], z[:-1, :-1])
    plt.subplot(224)
    plt.pcolor(x, y, z)
    for ax in fig.get_axes():
        for label in ax.get_xticklabels():
            label.set_ha('right')
            label.set_rotation(30)
@image_comparison(['canonical'], tol=0.02 if platform.machine() == 'arm64' else 0)
def mutated_test_canonical():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
@image_comparison(['arc_angles.png'], remove_text=True, style='default')
def mutated_test_arc_angles():
    w = 2
    h = 1
    centre = (0.2, 0.5)
    scale = 2
    fig, axs = plt.subplots(3, 3)
    for i, ax in enumerate(axs.flat):
        theta2 = i * 360 / 9
        theta1 = theta2 - 45
        ax.add_patch(mpatches.Ellipse(centre, w, h, alpha=0.3))
        ax.add_patch(mpatches.Arc(centre, w, h, theta1=theta1, theta2=theta2))
        ax.plot([scale * np.cos(np.deg2rad(theta1)) + centre[0], centre[0], scale * np.cos(np.deg2rad(theta2)) + centre[0]], [scale * np.sin(np.deg2rad(theta1)) + centre[1], centre[1], scale * np.sin(np.deg2rad(theta2)) + centre[1]])
        ax.set_xlim(-scale, scale)
        ax.set_ylim(-scale, scale)
        w *= 10
        h *= 10
        centre = (centre[0] * 10, centre[1] * 10)
        scale *= 10
@image_comparison(['arc_ellipse'], remove_text=True)
def mutated_test_arc_ellipse():
    xcenter, ycenter = (0.38, 0.52)
    width, height = (0.1, 0.3)
    angle = -30
    theta = np.deg2rad(np.arange(360))
    x = width / 2.0 * np.cos(theta)
    y = height / 2.0 * np.sin(theta)
    rtheta = np.deg2rad(angle)
    R = np.array([[np.cos(rtheta), -np.sin(rtheta)], [np.sin(rtheta), np.cos(rtheta)]])
    x, y = np.dot(R, [x, y])
    x += xcenter
    y += ycenter
    fig = plt.figure()
    ax = fig.add_subplot(211, aspect='auto')
    ax.fill(x, y, alpha=0.2, facecolor='yellow', edgecolor='yellow', linewidth=1, zorder=1)
    e1 = mpatches.Arc((xcenter, ycenter), width, height, angle=angle, linewidth=2, fill=False, zorder=2)
    ax.add_patch(e1)
    ax = fig.add_subplot(212, aspect='equal')
    ax.fill(x, y, alpha=0.2, facecolor='green', edgecolor='green', zorder=1)
    e2 = mpatches.Arc((xcenter, ycenter), width, height, angle=angle, linewidth=2, fill=False, zorder=2)
    ax.add_patch(e2)
@image_comparison(['markevery'], remove_text=True)
def mutated_test_markevery():
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.sqrt(x / 10 + 0.5)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label='default')
    ax.plot(x, y, 'd', markevery=None, label='mark all')
    ax.plot(x, y, 's', markevery=10, label='mark every 10')
    ax.plot(x, y, '+', markevery=(5, 20), label='mark every 5 starting at 10')
    ax.legend()
@image_comparison(['markevery_line'], remove_text=True, tol=0.005)
def mutated_test_markevery_line():
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.sqrt(x / 10 + 0.5)
    fig, ax = plt.subplots()
    ax.plot(x, y, '-o', label='default')
    ax.plot(x, y, '-d', markevery=None, label='mark all')
    ax.plot(x, y, '-s', markevery=10, label='mark every 10')
    ax.plot(x, y, '-+', markevery=(5, 20), label='mark every 5 starting at 10')
    ax.legend()
@image_comparison(['markevery_linear_scales'], remove_text=True, tol=0.001)
def mutated_test_markevery_linear_scales():
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]
    cols = 3
    gs = matplotlib.gridspec.GridSpec(len(cases) // cols + 1, cols)
    delta = 0.11
    x = np.linspace(0, 10 - 2 * delta, 200) + delta
    y = np.sin(x) + 1.0 + delta
    for i, case in enumerate(cases):
        row = i // cols
        col = i % cols
        plt.subplot(gs[row, col])
        plt.title('markevery=%s' % str(case))
        plt.plot(x, y, 'o', ls='-', ms=4, markevery=case)
@image_comparison(['markevery_linear_scales_zoomed'], remove_text=True)
def mutated_test_markevery_linear_scales_zoomed():
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]
    cols = 3
    gs = matplotlib.gridspec.GridSpec(len(cases) // cols + 1, cols)
    delta = 0.11
    x = np.linspace(0, 10 - 2 * delta, 200) + delta
    y = np.sin(x) + 1.0 + delta
    for i, case in enumerate(cases):
        row = i // cols
        col = i % cols
        plt.subplot(gs[row, col])
        plt.title('markevery=%s' % str(case))
        plt.plot(x, y, 'o', ls='-', ms=4, markevery=case)
        plt.xlim((6, 6.7))
        plt.ylim((1.1, 1.7))
@image_comparison(['markevery_log_scales'], remove_text=True)
def mutated_test_markevery_log_scales():
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]
    cols = 3
    gs = matplotlib.gridspec.GridSpec(len(cases) // cols + 1, cols)
    delta = 0.11
    x = np.linspace(0, 10 - 2 * delta, 200) + delta
    y = np.sin(x) + 1.0 + delta
    for i, case in enumerate(cases):
        row = i // cols
        col = i % cols
        plt.subplot(gs[row, col])
        plt.title('markevery=%s' % str(case))
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(x, y, 'o', ls='-', ms=4, markevery=case)
@image_comparison(['markevery_polar'], style='default', remove_text=True)
def mutated_test_markevery_polar():
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]
    cols = 3
    gs = matplotlib.gridspec.GridSpec(len(cases) // cols + 1, cols)
    r = np.linspace(0, 3.0, 200)
    theta = 2 * np.pi * r
    for i, case in enumerate(cases):
        row = i // cols
        col = i % cols
        plt.subplot(gs[row, col], polar=True)
        plt.title('markevery=%s' % str(case))
        plt.plot(theta, r, 'o', ls='-', ms=4, markevery=case)
@image_comparison(['markevery_linear_scales_nans'], remove_text=True)
def mutated_test_markevery_linear_scales_nans():
    cases = [None, 8, (30, 8), [16, 24, 30], [0, -1], slice(100, 200, 3), 0.1, 0.3, 1.5, (0.0, 0.1), (0.45, 0.1)]
    cols = 3
    gs = matplotlib.gridspec.GridSpec(len(cases) // cols + 1, cols)
    delta = 0.11
    x = np.linspace(0, 10 - 2 * delta, 200) + delta
    y = np.sin(x) + 1.0 + delta
    y[:10] = y[-20:] = y[50:70] = np.nan
    for i, case in enumerate(cases):
        row = i // cols
        col = i % cols
        plt.subplot(gs[row, col])
        plt.title('markevery=%s' % str(case))
        plt.plot(x, y, 'o', ls='-', ms=4, markevery=case)
@image_comparison(['marker_edges'], remove_text=True)
def mutated_test_marker_edges():
    x = np.linspace(0, 1, 10)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'y.', ms=30.0, mew=0, mec='r')
    ax.plot(x + 0.1, np.sin(x), 'y.', ms=30.0, mew=1, mec='r')
    ax.plot(x + 0.2, np.sin(x), 'y.', ms=30.0, mew=2, mec='b')
@image_comparison(['bar_tick_label_single.png', 'bar_tick_label_single.png'])
def mutated_test_bar_tick_label_single():
    ax = plt.gca()
    ax.bar(0, 1, align='edge', tick_label='0')
    data = {'a': 0, 'b': 1}
    fig, ax = plt.subplots()
    ax = plt.gca()
    ax.bar('a', 'b', align='edge', tick_label='0', data=data)
@image_comparison(['bar_tick_label_multiple.png'])
def mutated_test_bar_tick_label_multiple():
    ax = plt.gca()
    ax.bar([1, 2.5], [1, 2], width=[0.2, 0.5], tick_label=['a', 'b'], align='center')
@image_comparison(['bar_tick_label_multiple_old_label_alignment.png'])
def mutated_test_bar_tick_label_multiple_old_alignment():
    matplotlib.rcParams['ytick.alignment'] = 'center'
    ax = plt.gca()
    ax.bar([1, 2.5], [1, 2], width=[0.2, 0.5], tick_label=['a', 'b'], align='center')
@image_comparison(['barh_tick_label.png'])
def mutated_test_barh_tick_label():
    ax = plt.gca()
    ax.barh([1, 2.5], [1, 2], height=[0.2, 0.5], tick_label=['a', 'b'], align='center')
@image_comparison(['hist_log'], remove_text=True)
def mutated_test_hist_log():
    data0 = np.linspace(0, 1, 200) ** 3
    data = np.concatenate([1 - data0, 1 + data0])
    fig, ax = plt.subplots()
    ax.hist(data, fill=False, log=True)
@image_comparison(['hist_bar_empty.png'], remove_text=True)
def mutated_test_hist_bar_empty():
    ax = plt.gca()
    ax.hist([], histtype='bar')
@image_comparison(['hist_step_empty.png'], remove_text=True)
def mutated_test_hist_step_empty():
    ax = plt.gca()
    ax.hist([], histtype='step')
@image_comparison(['hist_step_filled.png'], remove_text=True)
def mutated_test_hist_step_filled():
    np.random.seed(0)
    x = np.random.randn(1000, 3)
    n_bins = 10
    kwargs = [{'fill': True}, {'fill': False}, {'fill': None}, {}] * 2
    types = ['step'] * 4 + ['stepfilled'] * 4
    fig, axs = plt.subplots(nrows=2, ncols=4)
    for kg, _type, ax in zip(kwargs, types, axs.flat):
        ax.hist(x, n_bins, histtype=_type, stacked=True, **kg)
        ax.set_title(f'{kg}/{_type}')
        ax.set_ylim(bottom=-50)
    patches = axs[0, 0].patches
    assert all((p.get_facecolor() == p.get_edgecolor() for p in patches))
@image_comparison(['hist_density.png'])
def mutated_test_hist_density():
    np.random.seed(19680801)
    data = np.random.standard_normal(2000)
    fig, ax = plt.subplots()
    ax.hist(data, density=True)
@image_comparison(['test_stairs_options.png'], remove_text=True)
def mutated_test_stairs_options():
    x, y = (np.array([1, 2, 3, 4, 5]), np.array([1, 2, 3, 4]).astype(float))
    yn = y.copy()
    yn[1] = np.nan
    fig, ax = plt.subplots()
    ax.stairs(y * 3, x, color='green', fill=True, label='A')
    ax.stairs(y, x * 3 - 3, color='red', fill=True, orientation='horizontal', label='B')
    ax.stairs(yn, x, color='orange', ls='--', lw=2, label='C')
    ax.stairs(yn / 3, x * 3 - 2, ls='--', lw=2, baseline=0.5, orientation='horizontal', label='D')
    ax.stairs(y[::-1] * 3 + 13, x - 1, color='red', ls='--', lw=2, baseline=None, label='E')
    ax.stairs(y[::-1] * 3 + 14, x, baseline=26, color='purple', ls='--', lw=2, label='F')
    ax.stairs(yn[::-1] * 3 + 15, x + 1, baseline=np.linspace(27, 25, len(y)), color='blue', ls='--', label='G', fill=True)
    ax.stairs(y[:-1][::-1] * 2 + 11, x[:-1] + 0.5, color='black', ls='--', lw=2, baseline=12, hatch='//', label='H')
    ax.legend(loc=0)
@image_comparison(['test_stairs_datetime.png'])
def mutated_test_stairs_datetime():
    f, ax = plt.subplots(constrained_layout=True)
    ax.stairs(np.arange(36), np.arange(np.datetime64('2001-12-27'), np.datetime64('2002-02-02')))
    plt.xticks(rotation=30)
@image_comparison(['contour_hatching'], remove_text=True, style='mpl20')
def mutated_test_contour_hatching():
    x, y, z = contour_dat()
    fig, ax = plt.subplots()
    ax.contourf(x, y, z, 7, hatches=['/', '\\', '//', '-'], cmap=mpl.colormaps['gray'], extend='both', alpha=0.5)
@image_comparison(['contour_colorbar'], style='mpl20', tol=0.54 if platform.machine() in ('aarch64', 'arm64', 'ppc64le', 's390x') else 0)
def mutated_test_contour_colorbar():
    x, y, z = contour_dat()
    fig, ax = plt.subplots()
    cs = ax.contourf(x, y, z, levels=np.arange(-1.8, 1.801, 0.2), cmap=mpl.colormaps['RdBu'], vmin=-0.6, vmax=0.6, extend='both')
    cs1 = ax.contour(x, y, z, levels=np.arange(-2.2, -0.599, 0.2), colors=['y'], linestyles='solid', linewidths=2)
    cs2 = ax.contour(x, y, z, levels=np.arange(0.6, 2.2, 0.2), colors=['c'], linewidths=2)
    cbar = fig.colorbar(cs, ax=ax)
    cbar.add_lines(cs1)
    cbar.add_lines(cs2, erase=False)
@image_comparison(['hist2d', 'hist2d'], remove_text=True, style='mpl20')
def mutated_test_hist2d():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(0)
    x = np.random.randn(100) * 2 + 5
    y = np.random.randn(100) - 2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)
    data = {'x': x, 'y': y}
    fig, ax = plt.subplots()
    ax.hist2d('x', 'y', bins=10, data=data, rasterized=True)
@image_comparison(['hist2d_transpose'], remove_text=True, style='mpl20')
def mutated_test_hist2d_transpose():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(0)
    x = np.array([5] * 100)
    y = np.random.randn(100) - 2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)
@image_comparison(['hist2d_transpose'], remove_text=True, style='mpl20')
def mutated_test_hist2d_transpose():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(0)
    x = np.array([5] * 100)
    y = np.random.randn(100) - 2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)

def test_hist2d_density():
    x, y = np.random.random((2, 100))
    ax = plt.figure().subplots()
    for obj in [ax, plt]:
        obj.hist2d(x, y, density=True)

class TestScatter:

    @image_comparison(['scatter'], style='mpl20', remove_text=True)
    def test_scatter_plot(self):
        data = {'x': np.array([3, 4, 2, 6]), 'y': np.array([2, 5, 2, 3]), 'c': ['r', 'y', 'b', 'lime'], 's': [24, 15, 19, 29], 'c2': ['0.5', '0.6', '0.7', '0.8']}
        fig, ax = plt.subplots()
        ax.scatter(data['x'] - 1.0, data['y'] - 1.0, c=data['c'], s=data['s'])
        ax.scatter(data['x'] + 1.0, data['y'] + 1.0, c=data['c2'], s=data['s'])
        ax.scatter('x', 'y', c='c', s='s', data=data)
@image_comparison(['hist2d_transpose'], remove_text=True, style='mpl20')
def mutated_test_hist2d_transpose():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(0)
    x = np.array([5] * 100)
    y = np.random.randn(100) - 2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)

def test_hist2d_density():
    x, y = np.random.random((2, 100))
    ax = plt.figure().subplots()
    for obj in [ax, plt]:
        obj.hist2d(x, y, density=True)

class TestScatter:

    @image_comparison(['scatter'], style='mpl20', remove_text=True)
    def test_scatter_plot(self):
        data = {'x': np.array([3, 4, 2, 6]), 'y': np.array([2, 5, 2, 3]), 'c': ['r', 'y', 'b', 'lime'], 's': [24, 15, 19, 29], 'c2': ['0.5', '0.6', '0.7', '0.8']}
        fig, ax = plt.subplots()
        ax.scatter(data['x'] - 1.0, data['y'] - 1.0, c=data['c'], s=data['s'])
        ax.scatter(data['x'] + 1.0, data['y'] + 1.0, c=data['c2'], s=data['s'])
        ax.scatter('x', 'y', c='c', s='s', data=data)

    @image_comparison(['scatter_marker.png'], remove_text=True)
    def test_scatter_marker(self):
        fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)
        ax0.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker='s')
        ax1.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker=mmarkers.MarkerStyle('o', fillstyle='top'))
        rx, ry = (3, 1)
        area = rx * ry * np.pi
        theta = np.linspace(0, 2 * np.pi, 21)
        verts = np.column_stack([np.cos(theta) * rx / area, np.sin(theta) * ry / area])
        ax2.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker=verts)
@image_comparison(['hist2d_transpose'], remove_text=True, style='mpl20')
def mutated_test_hist2d_transpose():
    plt.rcParams['pcolormesh.snap'] = False
    np.random.seed(0)
    x = np.array([5] * 100)
    y = np.random.randn(100) - 2
    fig, ax = plt.subplots()
    ax.hist2d(x, y, bins=10, rasterized=True)

def test_hist2d_density():
    x, y = np.random.random((2, 100))
    ax = plt.figure().subplots()
    for obj in [ax, plt]:
        obj.hist2d(x, y, density=True)

class TestScatter:

    @image_comparison(['scatter'], style='mpl20', remove_text=True)
    def test_scatter_plot(self):
        data = {'x': np.array([3, 4, 2, 6]), 'y': np.array([2, 5, 2, 3]), 'c': ['r', 'y', 'b', 'lime'], 's': [24, 15, 19, 29], 'c2': ['0.5', '0.6', '0.7', '0.8']}
        fig, ax = plt.subplots()
        ax.scatter(data['x'] - 1.0, data['y'] - 1.0, c=data['c'], s=data['s'])
        ax.scatter(data['x'] + 1.0, data['y'] + 1.0, c=data['c2'], s=data['s'])
        ax.scatter('x', 'y', c='c', s='s', data=data)

    @image_comparison(['scatter_marker.png'], remove_text=True)
    def test_scatter_marker(self):
        fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)
        ax0.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker='s')
        ax1.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker=mmarkers.MarkerStyle('o', fillstyle='top'))
        rx, ry = (3, 1)
        area = rx * ry * np.pi
        theta = np.linspace(0, 2 * np.pi, 21)
        verts = np.column_stack([np.cos(theta) * rx / area, np.sin(theta) * ry / area])
        ax2.scatter([3, 4, 2, 6], [2, 5, 2, 3], c=[(1, 0, 0), 'y', 'b', 'lime'], s=[60, 50, 40, 30], edgecolors=['k', 'r', 'g', 'b'], marker=verts)

    @image_comparison(['scatter_2D'], remove_text=True, extensions=['png'])
    def test_scatter_2D(self):
        x = np.arange(3)
        y = np.arange(2)
        x, y = np.meshgrid(x, y)
        z = x + y
        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=200, edgecolors='face')
@image_comparison(['stackplot_test_image', 'stackplot_test_image'], tol=0.031 if platform.machine() == 'arm64' else 0)
def mutated_test_stackplot():
    fig = plt.figure()
    x = np.linspace(0, 10, 10)
    y1 = 1.0 * x
    y2 = 2.0 * x + 1
    y3 = 3.0 * x + 2
    ax = fig.add_subplot(1, 1, 1)
    ax.stackplot(x, y1, y2, y3)
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 70))
    data = {'x': x, 'y1': y1, 'y2': y2, 'y3': y3}
    fig, ax = plt.subplots()
    ax.stackplot('x', 'y1', 'y2', 'y3', data=data, colors=['C0', 'C1', 'C2'])
    ax.set_xlim((0, 10))
    ax.set_ylim((0, 70))
@image_comparison(['stackplot_test_baseline'], remove_text=True)
def mutated_test_stackplot_baseline():
    np.random.seed(0)

    def layers(n, m):
        a = np.zeros((m, n))
        for i in range(n):
            for j in range(5):
                x = 1 / (0.1 + np.random.random())
                y = 2 * np.random.random() - 0.5
                z = 10 / (0.1 + np.random.random())
                a[:, i] += x * np.exp(-((np.arange(m) / m - y) * z) ** 2)
        return a
    d = layers(3, 100)
    d[50, :] = 0
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].stackplot(range(100), d.T, baseline='zero')
    axs[0, 1].stackplot(range(100), d.T, baseline='sym')
    axs[1, 0].stackplot(range(100), d.T, baseline='wiggle')
    axs[1, 1].stackplot(range(100), d.T, baseline='weighted_wiggle')
@image_comparison(['bxp_baseline.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_baseline():
    _bxp_test_helper()
@image_comparison(['bxp_rangewhis.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_rangewhis():
    _bxp_test_helper(stats_kwargs=dict(whis=[0, 100]))
@image_comparison(['bxp_percentilewhis.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_percentilewhis():
    _bxp_test_helper(stats_kwargs=dict(whis=[5, 95]))
@image_comparison(['bxp_with_xlabels.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_with_xlabels():

    def transform(stats):
        for s, label in zip(stats, list('ABCD')):
            s['label'] = label
        return stats
    _bxp_test_helper(transform_stats=transform)
@image_comparison(['bxp_horizontal.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default', tol=0.1)
def mutated_test_bxp_horizontal():
    _bxp_test_helper(bxp_kwargs=dict(orientation='horizontal'))
@image_comparison(['bxp_with_ylabels.png'], savefig_kwarg={'dpi': 40}, style='default', tol=0.1)
def mutated_test_bxp_with_ylabels():

    def transform(stats):
        for s, label in zip(stats, list('ABCD')):
            s['label'] = label
        return stats
    _bxp_test_helper(transform_stats=transform, bxp_kwargs=dict(orientation='horizontal'))
@image_comparison(['bxp_patchartist.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_patchartist():
    _bxp_test_helper(bxp_kwargs=dict(patch_artist=True))
@image_comparison(['bxp_custompatchartist.png'], remove_text=True, savefig_kwarg={'dpi': 100}, style='default')
def mutated_test_bxp_custompatchartist():
    _bxp_test_helper(bxp_kwargs=dict(patch_artist=True, boxprops=dict(facecolor='yellow', edgecolor='green', ls=':')))
@image_comparison(['bxp_customoutlier.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_customoutlier():
    _bxp_test_helper(bxp_kwargs=dict(flierprops=dict(linestyle='none', marker='d', mfc='g')))
@image_comparison(['bxp_withmean_custompoint.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_showcustommean():
    _bxp_test_helper(bxp_kwargs=dict(showmeans=True, meanprops=dict(linestyle='none', marker='d', mfc='green')))
@image_comparison(['bxp_custombox.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_custombox():
    _bxp_test_helper(bxp_kwargs=dict(boxprops=dict(linestyle='--', color='b', lw=3)))
@image_comparison(['bxp_custommedian.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_custommedian():
    _bxp_test_helper(bxp_kwargs=dict(medianprops=dict(linestyle='--', color='b', lw=3)))
@image_comparison(['bxp_customcap.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_customcap():
    _bxp_test_helper(bxp_kwargs=dict(capprops=dict(linestyle='--', color='g', lw=3)))
@image_comparison(['bxp_customwhisker.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_customwhisker():
    _bxp_test_helper(bxp_kwargs=dict(whiskerprops=dict(linestyle='-', color='m', lw=3)))
@image_comparison(['bxp_withnotch.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_shownotches():
    _bxp_test_helper(bxp_kwargs=dict(shownotches=True))
@image_comparison(['bxp_nocaps.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_nocaps():
    _bxp_test_helper(bxp_kwargs=dict(showcaps=False))
@image_comparison(['bxp_nobox.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_nobox():
    _bxp_test_helper(bxp_kwargs=dict(showbox=False))
@image_comparison(['bxp_no_flier_stats.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_no_flier_stats():

    def transform(stats):
        for s in stats:
            s.pop('fliers', None)
        return stats
    _bxp_test_helper(transform_stats=transform, bxp_kwargs=dict(showfliers=False))
@image_comparison(['bxp_withmean_point.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_showmean():
    _bxp_test_helper(bxp_kwargs=dict(showmeans=True, meanline=False))
@image_comparison(['bxp_withmean_line.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_showmeanasline():
    _bxp_test_helper(bxp_kwargs=dict(showmeans=True, meanline=True))
@image_comparison(['bxp_scalarwidth.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_scalarwidth():
    _bxp_test_helper(bxp_kwargs=dict(widths=0.25))
@image_comparison(['bxp_customwidths.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_customwidths():
    _bxp_test_helper(bxp_kwargs=dict(widths=[0.1, 0.25, 0.65, 0.85]))
@image_comparison(['bxp_custompositions.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_custompositions():
    _bxp_test_helper(bxp_kwargs=dict(positions=[1, 5, 6, 7]))
@image_comparison(['bxp_custom_capwidths.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_custom_capwidths():
    _bxp_test_helper(bxp_kwargs=dict(capwidths=[0.0, 0.1, 0.5, 1.0]))
@image_comparison(['bxp_custom_capwidth.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_bxp_custom_capwidth():
    _bxp_test_helper(bxp_kwargs=dict(capwidths=0.6))
@image_comparison(['boxplot', 'boxplot'], tol=1.28, style='default')
def mutated_test_boxplot():
    np.random.seed(937)
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    ax.boxplot([x, x], bootstrap=10000, notch=1)
    ax.set_ylim((-30, 30))
    data = {'x': [x, x]}
    fig, ax = plt.subplots()
    ax.boxplot('x', bootstrap=10000, notch=1, data=data)
    ax.set_ylim((-30, 30))
@image_comparison(['boxplot_custom_capwidths.png'], savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_boxplot_custom_capwidths():
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    ax.boxplot([x, x], notch=1, capwidths=[0.01, 0.2])
@image_comparison(['boxplot_sym2.png'], remove_text=True, style='default')
def mutated_test_boxplot_sym2():
    np.random.seed(937)
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, [ax1, ax2] = plt.subplots(1, 2)
    ax1.boxplot([x, x], bootstrap=10000, sym='^')
    ax1.set_ylim((-30, 30))
    ax2.boxplot([x, x], bootstrap=10000, sym='g')
    ax2.set_ylim((-30, 30))
@image_comparison(['boxplot_sym.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_boxplot_sym():
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    ax.boxplot([x, x], sym='gs')
    ax.set_ylim((-30, 30))
@image_comparison(['boxplot_autorange_false_whiskers.png', 'boxplot_autorange_true_whiskers.png'], style='default')
def mutated_test_boxplot_autorange_whiskers():
    np.random.seed(937)
    x = np.ones(140)
    x = np.hstack([0, x, 2])
    fig1, ax1 = plt.subplots()
    ax1.boxplot([x, x], bootstrap=10000, notch=1)
    ax1.set_ylim((-5, 5))
    fig2, ax2 = plt.subplots()
    ax2.boxplot([x, x], bootstrap=10000, notch=1, autorange=True)
    ax2.set_ylim((-5, 5))
@image_comparison(['boxplot_rc_parameters'], savefig_kwarg={'dpi': 100}, remove_text=True, tol=1, style='default')
def mutated_test_boxplot_rc_parameters():
    np.random.seed(937)
    fig, ax = plt.subplots(3)
    rc_axis0 = {'boxplot.notch': True, 'boxplot.whiskers': [5, 95], 'boxplot.bootstrap': 10000, 'boxplot.flierprops.color': 'b', 'boxplot.flierprops.marker': 'o', 'boxplot.flierprops.markerfacecolor': 'g', 'boxplot.flierprops.markeredgecolor': 'b', 'boxplot.flierprops.markersize': 5, 'boxplot.flierprops.linestyle': '--', 'boxplot.flierprops.linewidth': 2.0, 'boxplot.boxprops.color': 'r', 'boxplot.boxprops.linewidth': 2.0, 'boxplot.boxprops.linestyle': '--', 'boxplot.capprops.color': 'c', 'boxplot.capprops.linewidth': 2.0, 'boxplot.capprops.linestyle': '--', 'boxplot.medianprops.color': 'k', 'boxplot.medianprops.linewidth': 2.0, 'boxplot.medianprops.linestyle': '--'}
    rc_axis1 = {'boxplot.whiskers': [0, 100], 'boxplot.patchartist': True}
    rc_axis2 = {'boxplot.whiskers': 2.0, 'boxplot.showcaps': False, 'boxplot.showbox': False, 'boxplot.showfliers': False, 'boxplot.showmeans': True, 'boxplot.meanline': True, 'boxplot.meanprops.color': 'c', 'boxplot.meanprops.linewidth': 2.0, 'boxplot.meanprops.linestyle': '--', 'boxplot.whiskerprops.color': 'r', 'boxplot.whiskerprops.linewidth': 2.0, 'boxplot.whiskerprops.linestyle': '-.'}
    dict_list = [rc_axis0, rc_axis1, rc_axis2]
    for axis, rc_axis in zip(ax, dict_list):
        _rc_test_bxp_helper(axis, rc_axis)
    assert matplotlib.patches.PathPatch in [type(t) for t in ax[1].get_children()]
@image_comparison(['boxplot_with_CIarray.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_boxplot_with_CIarray():
    np.random.seed(937)
    x = np.linspace(-7, 7, 140)
    x = np.hstack([-25, x, 25])
    fig, ax = plt.subplots()
    CIs = np.array([[-1.5, 3.0], [-1.0, 3.5]])
    ax.boxplot([x, x], bootstrap=10000, usermedians=[None, 1.0], conf_intervals=CIs, notch=1)
    ax.set_ylim((-30, 30))
@image_comparison(['boxplot_no_inverted_whisker.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_boxplot_no_weird_whisker():
    x = np.array([3, 9000, 150, 88, 350, 200000, 1400, 960], dtype=np.float64)
    ax1 = plt.axes()
    ax1.boxplot(x)
    ax1.set_yscale('log')
    ax1.yaxis.grid(False, which='minor')
    ax1.xaxis.grid(False)
@image_comparison(['boxplot_mod_artists_after_plotting.png'], remove_text=True, savefig_kwarg={'dpi': 40}, style='default')
def mutated_test_boxplot_mod_artist_after_plotting():
    x = [0.15, 0.11, 0.06, 0.06, 0.12, 0.56, -0.56]
    fig, ax = plt.subplots()
    bp = ax.boxplot(x, sym='o')
    for key in bp:
        for obj in bp[key]:
            obj.set_color('green')
@image_comparison(['violinplot_vert_baseline.png', 'violinplot_vert_baseline.png'])
def mutated_test_vert_violinplot_baseline():
    np.random.seed(414213562)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax = plt.axes()
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False, showmedians=False)
    data = {'d': data}
    fig, ax = plt.subplots()
    ax.violinplot('d', positions=range(4), showmeans=False, showextrema=False, showmedians=False, data=data)
@image_comparison(['violinplot_vert_showmeans.png'])
def mutated_test_vert_violinplot_showmeans():
    ax = plt.axes()
    np.random.seed(732050807)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=True, showextrema=False, showmedians=False)
@image_comparison(['violinplot_vert_showextrema.png'])
def mutated_test_vert_violinplot_showextrema():
    ax = plt.axes()
    np.random.seed(236067977)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=True, showmedians=False)
@image_comparison(['violinplot_vert_showmedians.png'])
def mutated_test_vert_violinplot_showmedians():
    ax = plt.axes()
    np.random.seed(645751311)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False, showmedians=True)
@image_comparison(['violinplot_vert_showall.png'])
def mutated_test_vert_violinplot_showall():
    ax = plt.axes()
    np.random.seed(316624790)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=True, showextrema=True, showmedians=True, quantiles=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]])
@image_comparison(['violinplot_vert_custompoints_10.png'])
def mutated_test_vert_violinplot_custompoints_10():
    ax = plt.axes()
    np.random.seed(605551275)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False, showmedians=False, points=10)
@image_comparison(['violinplot_vert_custompoints_200.png'])
def mutated_test_vert_violinplot_custompoints_200():
    ax = plt.axes()
    np.random.seed(123105625)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), showmeans=False, showextrema=False, showmedians=False, points=200)
@image_comparison(['violinplot_horiz_baseline.png'])
def mutated_test_horiz_violinplot_baseline():
    ax = plt.axes()
    np.random.seed(358898943)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False, showextrema=False, showmedians=False)
@image_comparison(['violinplot_horiz_showmedians.png'])
def mutated_test_horiz_violinplot_showmedians():
    ax = plt.axes()
    np.random.seed(795831523)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False, showextrema=False, showmedians=True)
@image_comparison(['violinplot_horiz_showmeans.png'])
def mutated_test_horiz_violinplot_showmeans():
    ax = plt.axes()
    np.random.seed(385164807)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=True, showextrema=False, showmedians=False)
@image_comparison(['violinplot_horiz_showextrema.png'])
def mutated_test_horiz_violinplot_showextrema():
    ax = plt.axes()
    np.random.seed(567764362)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False, showextrema=True, showmedians=False)
@image_comparison(['violinplot_horiz_showall.png'])
def mutated_test_horiz_violinplot_showall():
    ax = plt.axes()
    np.random.seed(82762530)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=True, showextrema=True, showmedians=True, quantiles=[[0.1, 0.9], [0.2, 0.8], [0.3, 0.7], [0.4, 0.6]])
@image_comparison(['violinplot_horiz_custompoints_10.png'])
def mutated_test_horiz_violinplot_custompoints_10():
    ax = plt.axes()
    np.random.seed(403124237)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False, showextrema=False, showmedians=False, points=10)
@image_comparison(['violinplot_horiz_custompoints_200.png'])
def mutated_test_horiz_violinplot_custompoints_200():
    ax = plt.axes()
    np.random.seed(557438524)
    data = [np.random.normal(size=100) for _ in range(4)]
    ax.violinplot(data, positions=range(4), orientation='horizontal', showmeans=False, showextrema=False, showmedians=False, points=200)
@image_comparison(['violinplot_sides.png'], remove_text=True, style='mpl20')
def mutated_test_violinplot_sides():
    ax = plt.axes()
    np.random.seed(19680801)
    data = [np.random.normal(size=100)]
    for pos, side in zip([0, -0.5, 0.5], ['both', 'low', 'high']):
        ax.violinplot(data, positions=[pos], orientation='horizontal', showmeans=False, showextrema=True, showmedians=True, side=side)
    for pos, side in zip([4, 3.5, 4.5], ['both', 'low', 'high']):
        ax.violinplot(data, positions=[pos], orientation='vertical', showmeans=False, showextrema=True, showmedians=True, side=side)
@image_comparison(['errorbar_basic', 'errorbar_mixed', 'errorbar_basic'])
def mutated_test_errorbar():
    x = np.arange(0.1, 4, 0.5, dtype=np.longdouble)
    y = np.exp(-x)
    yerr = 0.1 + 0.2 * np.sqrt(x)
    xerr = 0.1 + yerr
    fig = plt.figure()
    ax = fig.gca()
    ax.errorbar(x, y, xerr=0.2, yerr=0.4)
    ax.set_title('Simplest errorbars, 0.2 in x, 0.4 in y')
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
    ax = axs[0, 0]
    ax.errorbar(x, y, yerr=yerr, fmt='o')
    ax.set_title('Vert. symmetric')
    ax.locator_params(nbins=4)
    ax = axs[0, 1]
    ax.errorbar(x, y, xerr=xerr, fmt='o', alpha=0.4)
    ax.set_title('Hor. symmetric w/ alpha')
    ax = axs[1, 0]
    ax.errorbar(x, y, yerr=[yerr, 2 * yerr], xerr=[xerr, 2 * xerr], fmt='--o')
    ax.set_title('H, V asymmetric')
    ax = axs[1, 1]
    ax.set_yscale('log')
    ylower = np.maximum(0.01, y - yerr)
    yerr_lower = y - ylower
    ax.errorbar(x, y, yerr=[yerr_lower, 2 * yerr], xerr=xerr, fmt='o', ecolor='g', capthick=2)
    ax.set_title('Mixed sym., log y')
    ax.set_ylim(0.01, 10.0)
    fig.suptitle('Variable errorbars')
    data = {'x': x, 'y': y}
    fig = plt.figure()
    ax = fig.gca()
    ax.errorbar('x', 'y', xerr=0.2, yerr=0.4, data=data)
    ax.set_title('Simplest errorbars, 0.2 in x, 0.4 in y')
@image_comparison(['mixed_errorbar_polar_caps'], extensions=['png'], remove_text=True)
def mutated_test_mixed_errorbar_polar_caps():
    """
    Mix several polar errorbar use cases in a single test figure.

    It is advisable to position individual points off the grid. If there are
    problems with reproducibility of this test, consider removing grid.
    """
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    th_sym = [1, 2, 3]
    r_sym = [0.9] * 3
    ax.errorbar(th_sym, r_sym, xerr=0.35, yerr=0.2, fmt='o')
    th_long = [np.pi / 2 + 0.1, np.pi + 0.1]
    r_long = [1.8, 2.2]
    ax.errorbar(th_long, r_long, xerr=0.8 * np.pi, yerr=0.15, fmt='o')
    th_asym = [4 * np.pi / 3 + 0.1, 5 * np.pi / 3 + 0.1, 2 * np.pi - 0.1]
    r_asym = [1.1] * 3
    xerr = [[0.3, 0.3, 0.2], [0.2, 0.3, 0.3]]
    yerr = [[0.35, 0.5, 0.5], [0.5, 0.35, 0.5]]
    ax.errorbar(th_asym, r_asym, xerr=xerr, yerr=yerr, fmt='o')
    th_over = [2.1]
    r_over = [3.1]
    ax.errorbar(th_over, r_over, xerr=10, yerr=0.2, fmt='o')
@image_comparison(['errorbar_limits'])
def mutated_test_errorbar_limits():
    x = np.arange(0.5, 5.5, 0.5)
    y = np.exp(-x)
    xerr = 0.1
    yerr = 0.2
    ls = 'dotted'
    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, ls=ls, color='blue')
    uplims = np.zeros_like(x)
    uplims[[1, 5, 9]] = True
    ax.errorbar(x, y + 0.5, xerr=xerr, yerr=yerr, uplims=uplims, ls=ls, color='green')
    lolims = np.zeros_like(x)
    lolims[[2, 4, 8]] = True
    ax.errorbar(x, y + 1.0, xerr=xerr, yerr=yerr, lolims=lolims, ls=ls, color='red')
    ax.errorbar(x, y + 1.5, marker='o', ms=8, xerr=xerr, yerr=yerr, lolims=lolims, uplims=uplims, ls=ls, color='magenta')
    xerr = 0.2
    yerr = np.full_like(x, 0.2)
    yerr[[3, 6]] = 0.3
    xlolims = lolims
    xuplims = uplims
    lolims = np.zeros_like(x)
    uplims = np.zeros_like(x)
    lolims[[6]] = True
    uplims[[3]] = True
    ax.errorbar(x, y + 2.1, marker='o', ms=8, xerr=xerr, yerr=yerr, xlolims=xlolims, xuplims=xuplims, uplims=uplims, lolims=lolims, ls='none', mec='blue', capsize=0, color='cyan')
    ax.set_xlim((0, 5.5))
    ax.set_title('Errorbar upper and lower limits')
@image_comparison(['hist_stacked_stepfilled', 'hist_stacked_stepfilled'])
def mutated_test_hist_stacked_stepfilled():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype='stepfilled', stacked=True)
    data = {'x': (d1, d2)}
    fig, ax = plt.subplots()
    ax.hist('x', histtype='stepfilled', stacked=True, data=data)
@image_comparison(['hist_offset'])
def mutated_test_hist_offset():
    d1 = np.linspace(0, 10, 50)
    d2 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist(d1, bottom=5)
    ax.hist(d2, bottom=15)
@image_comparison(['hist_step.png'], remove_text=True)
def mutated_test_hist_step():
    d1 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist(d1, histtype='step')
    ax.set_ylim(0, 10)
    ax.set_xlim(-1, 5)
@image_comparison(['hist_step_horiz.png'])
def mutated_test_hist_step_horiz():
    d1 = np.linspace(0, 10, 50)
    d2 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype='step', orientation='horizontal')
@image_comparison(['hist_stacked_weights'])
def mutated_test_hist_stacked_weighted():
    d1 = np.linspace(0, 10, 50)
    d2 = np.linspace(1, 3, 20)
    w1 = np.linspace(0.01, 3.5, 50)
    w2 = np.linspace(0.05, 2.0, 20)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), weights=(w1, w2), histtype='stepfilled', stacked=True)
@image_comparison(['stem.png'], style='mpl20', remove_text=True)
def mutated_test_stem():
    x = np.linspace(0.1, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.stem(x, np.cos(x), linefmt='C2-.', markerfmt='k+', basefmt='C1-.', label=' ')
    ax.legend()
@image_comparison(['stem_orientation.png'], style='mpl20', remove_text=True)
def mutated_test_stem_orientation():
    x = np.linspace(0.1, 2 * np.pi, 50)
    fig, ax = plt.subplots()
    ax.stem(x, np.cos(x), linefmt='C2-.', markerfmt='kx', basefmt='C1-.', orientation='horizontal')
@image_comparison(['hist_stacked_stepfilled_alpha'])
def mutated_test_hist_stacked_stepfilled_alpha():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype='stepfilled', stacked=True, alpha=0.5)
@image_comparison(['hist_stacked_step'])
def mutated_test_hist_stacked_step():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), histtype='step', stacked=True)
@image_comparison(['hist_stacked_normed'])
def mutated_test_hist_stacked_density():
    d1 = np.linspace(1, 3, 20)
    d2 = np.linspace(0, 10, 50)
    fig, ax = plt.subplots()
    ax.hist((d1, d2), stacked=True, density=True)
@image_comparison(['hist_step_bottom.png'], remove_text=True)
def mutated_test_hist_step_bottom():
    d1 = np.linspace(1, 3, 20)
    fig, ax = plt.subplots()
    ax.hist(d1, bottom=np.arange(10), histtype='stepfilled')
@image_comparison(['hist_stacked_bar'])
def mutated_test_hist_stacked_bar():
    d = [[100, 100, 100, 100, 200, 320, 450, 80, 20, 600, 310, 800], [20, 23, 50, 11, 100, 420], [120, 120, 120, 140, 140, 150, 180], [60, 60, 60, 60, 300, 300, 5, 5, 5, 5, 10, 300], [555, 555, 555, 30, 30, 30, 30, 30, 100, 100, 100, 100, 30, 30], [30, 30, 30, 30, 400, 400, 400, 400, 400, 400, 400, 400]]
    colors = [(0.5759849696758961, 1.0, 0.0), (0.0, 1.0, 0.350624650815206), (0.0, 1.0, 0.6549834156005998), (0.0, 0.6569064625276622, 1.0), (0.28302699607823545, 0.0, 1.0), (0.6849123462299822, 0.0, 1.0)]
    labels = ['green', 'orange', ' yellow', 'magenta', 'black']
    fig, ax = plt.subplots()
    ax.hist(d, bins=10, histtype='barstacked', align='mid', color=colors, label=labels)
    ax.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), ncols=1)
@image_comparison(['transparent_markers'], remove_text=True)
def mutated_test_transparent_markers():
    np.random.seed(0)
    data = np.random.random(50)
    fig, ax = plt.subplots()
    ax.plot(data, 'D', mfc='none', markersize=100)
@image_comparison(['rgba_markers'], remove_text=True)
def mutated_test_rgba_markers():
    fig, axs = plt.subplots(ncols=2)
    rcolors = [(1, 0, 0, 1), (1, 0, 0, 0.5)]
    bcolors = [(0, 0, 1, 1), (0, 0, 1, 0.5)]
    alphas = [None, 0.2]
    kw = dict(ms=100, mew=20)
    for i, alpha in enumerate(alphas):
        for j, rcolor in enumerate(rcolors):
            for k, bcolor in enumerate(bcolors):
                axs[i].plot(j + 1, k + 1, 'o', mfc=bcolor, mec=rcolor, alpha=alpha, **kw)
                axs[i].plot(j + 1, k + 3, 'x', mec=rcolor, alpha=alpha, **kw)
    for ax in axs:
        ax.axis([-1, 4, 0, 5])
@image_comparison(['mollweide_grid'], remove_text=True)
def mutated_test_mollweide_grid():
    fig = plt.figure()
    ax = fig.add_subplot(projection='mollweide')
    ax.grid()
@image_comparison(['test_alpha'], remove_text=True)
def mutated_test_alpha():
    np.random.seed(0)
    data = np.random.random(50)
    fig, ax = plt.subplots()
    ax.plot(data, '-D', color=[1, 0, 0], mfc=[1, 0, 0, 0.5], markersize=20, lw=10)
    ax.plot(data + 2, '-D', color=[1, 0, 0, 0.5], mfc=[1, 0, 0, 0.5], markersize=20, lw=10, alpha=1)
    ax.plot(data + 4, '-D', color=[1, 0, 0], mfc=[1, 0, 0], markersize=20, lw=10, alpha=0.5)
    ax.plot(data + 6, '-D', color=[1, 0, 0, 0.5], mfc=[1, 0, 0, 0.5], markersize=20, lw=10)
    ax.plot(data + 8, '-D', color=[1, 0, 0, 0.5], mfc=[1, 0, 0], markersize=20, lw=10)
@image_comparison(['eventplot', 'eventplot'], remove_text=True)
def mutated_test_eventplot():
    np.random.seed(0)
    data1 = np.random.random([32, 20]).tolist()
    data2 = np.random.random([6, 20]).tolist()
    data = data1 + data2
    num_datasets = len(data)
    colors1 = [[0, 1, 0.7]] * len(data1)
    colors2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0.75, 0], [1, 0, 1], [0, 1, 1]]
    colors = colors1 + colors2
    lineoffsets1 = 12 + np.arange(0, len(data1)) * 0.33
    lineoffsets2 = [-15, -3, 1, 1.5, 6, 10]
    lineoffsets = lineoffsets1.tolist() + lineoffsets2
    linelengths1 = [0.33] * len(data1)
    linelengths2 = [5, 2, 1, 1, 3, 1.5]
    linelengths = linelengths1 + linelengths2
    fig = plt.figure()
    axobj = fig.add_subplot()
    colls = axobj.eventplot(data, colors=colors, lineoffsets=lineoffsets, linelengths=linelengths)
    num_collections = len(colls)
    assert num_collections == num_datasets
    data = {'pos': data, 'c': colors, 'lo': lineoffsets, 'll': linelengths}
    fig = plt.figure()
    axobj = fig.add_subplot()
    colls = axobj.eventplot('pos', colors='c', lineoffsets='lo', linelengths='ll', data=data)
    num_collections = len(colls)
    assert num_collections == num_datasets
@image_comparison(['test_eventplot_defaults.png'], remove_text=True)
def mutated_test_eventplot_defaults():
    """
    test that eventplot produces the correct output given the default params
    (see bug #3728)
    """
    np.random.seed(0)
    data1 = np.random.random([32, 20]).tolist()
    data2 = np.random.random([6, 20]).tolist()
    data = data1 + data2
    fig = plt.figure()
    axobj = fig.add_subplot()
    axobj.eventplot(data)
@image_comparison(['test_eventplot_problem_kwargs.png'], remove_text=True)
def mutated_test_eventplot_problem_kwargs(recwarn):
    """
    test that 'singular' versions of LineCollection props raise an
    MatplotlibDeprecationWarning rather than overriding the 'plural' versions
    (e.g., to prevent 'color' from overriding 'colors', see issue #4297)
    """
    np.random.seed(0)
    data1 = np.random.random([20]).tolist()
    data2 = np.random.random([10]).tolist()
    data = [data1, data2]
    fig = plt.figure()
    axobj = fig.add_subplot()
    axobj.eventplot(data, colors=['r', 'b'], color=['c', 'm'], linewidths=[2, 1], linewidth=[1, 2], linestyles=['solid', 'dashed'], linestyle=['dashdot', 'dotted'])
    assert len(recwarn) == 3
    assert all((issubclass(wi.category, mpl.MatplotlibDeprecationWarning) for wi in recwarn))
@image_comparison(['marker_styles.png'], remove_text=True)
def mutated_test_marker_styles():
    fig, ax = plt.subplots()
    markers = sorted(matplotlib.markers.MarkerStyle.markers, key=lambda x: str(type(x)) + str(x))
    markers.remove('none')
    markers = ['none', *markers]
    for y, marker in enumerate(markers):
        ax.plot(y % 2 * 5 + np.arange(10) * 10, np.ones(10) * 10 * y, linestyle='', marker=marker, markersize=10 + y / 5, label=marker)
@image_comparison(['rc_markerfill.png'], tol=0.037 if platform.machine() == 'arm64' else 0)
def mutated_test_markers_fillstyle_rcparams():
    fig, ax = plt.subplots()
    x = np.arange(7)
    for idx, (style, marker) in enumerate([('top', 's'), ('bottom', 'o'), ('none', '^')]):
        matplotlib.rcParams['markers.fillstyle'] = style
        ax.plot(x + idx, marker=marker)
@image_comparison(['vertex_markers.png'], remove_text=True)
def mutated_test_vertex_markers():
    data = list(range(10))
    marker_as_tuple = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    marker_as_list = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    fig, ax = plt.subplots()
    ax.plot(data, linestyle='', marker=marker_as_tuple, mfc='k')
    ax.plot(data[::-1], linestyle='', marker=marker_as_list, mfc='b')
    ax.set_xlim([-1, 10])
    ax.set_ylim([-1, 10])
@image_comparison(['vline_hline_zorder', 'errorbar_zorder'], tol=0 if platform.machine() == 'x86_64' else 0.026)
def mutated_test_eb_line_zorder():
    x = list(range(10))
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(x, lw=10, zorder=5)
    ax.axhline(1, color='red', lw=10, zorder=1)
    ax.axhline(5, color='green', lw=10, zorder=10)
    ax.axvline(7, color='m', lw=10, zorder=7)
    ax.axvline(2, color='k', lw=10, zorder=3)
    ax.set_title('axvline and axhline zorder test')
    fig = plt.figure()
    ax = fig.gca()
    x = list(range(10))
    y = np.zeros(10)
    yerr = list(range(10))
    ax.errorbar(x, y, yerr=yerr, zorder=5, lw=5, color='r')
    for j in range(10):
        ax.axhline(j, lw=5, color='k', zorder=j)
        ax.axhline(-j, lw=5, color='k', zorder=j)
    ax.set_title('errorbar zorder test')
@image_comparison(['vlines_basic', 'vlines_with_nan', 'vlines_masked'], extensions=['png'])
def mutated_test_vlines():
    x1 = [2, 3, 4, 5, 7]
    y1 = [2, -6, 3, 8, 2]
    fig1, ax1 = plt.subplots()
    ax1.vlines(x1, 0, y1, colors='g', linewidth=5)
    x2 = [2, 3, 4, 5, 6, 7]
    y2 = [2, -6, 3, 8, np.nan, 2]
    fig2, (ax2, ax3, ax4) = plt.subplots(nrows=3, figsize=(4, 8))
    ax2.vlines(x2, 0, y2, colors='g', linewidth=5)
    x3 = [2, 3, 4, 5, 6, 7]
    y3 = [np.nan, 2, -6, 3, 8, 2]
    ax3.vlines(x3, 0, y3, colors='r', linewidth=3, linestyle='--')
    x4 = [2, 3, 4, 5, 6, 7]
    y4 = [np.nan, 2, -6, 3, 8, np.nan]
    ax4.vlines(x4, 0, y4, colors='k', linewidth=2)
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_xlim(0, 10)
    assert ax1.get_ylim() == ax2.get_ylim()
    assert ax1.get_ylim() == ax3.get_ylim()
    assert ax1.get_ylim() == ax4.get_ylim()
    fig3, ax5 = plt.subplots()
    x5 = np.ma.masked_equal([2, 4, 6, 8, 10, 12], 8)
    ymin5 = np.ma.masked_equal([0, 1, -1, 0, 2, 1], 2)
    ymax5 = np.ma.masked_equal([13, 14, 15, 16, 17, 18], 18)
    ax5.vlines(x5, ymin5, ymax5, colors='k', linewidth=2)
    ax5.set_xlim(0, 15)
@image_comparison(['hlines_basic', 'hlines_with_nan', 'hlines_masked'], extensions=['png'])
def mutated_test_hlines():
    y1 = [2, 3, 4, 5, 7]
    x1 = [2, -6, 3, 8, 2]
    fig1, ax1 = plt.subplots()
    ax1.hlines(y1, 0, x1, colors='g', linewidth=5)
    y2 = [2, 3, 4, 5, 6, 7]
    x2 = [2, -6, 3, 8, np.nan, 2]
    fig2, (ax2, ax3, ax4) = plt.subplots(nrows=3, figsize=(4, 8))
    ax2.hlines(y2, 0, x2, colors='g', linewidth=5)
    y3 = [2, 3, 4, 5, 6, 7]
    x3 = [np.nan, 2, -6, 3, 8, 2]
    ax3.hlines(y3, 0, x3, colors='r', linewidth=3, linestyle='--')
    y4 = [2, 3, 4, 5, 6, 7]
    x4 = [np.nan, 2, -6, 3, 8, np.nan]
    ax4.hlines(y4, 0, x4, colors='k', linewidth=2)
    for ax in [ax1, ax2, ax3, ax4]:
        ax.set_ylim(0, 10)
    assert ax1.get_xlim() == ax2.get_xlim()
    assert ax1.get_xlim() == ax3.get_xlim()
    assert ax1.get_xlim() == ax4.get_xlim()
    fig3, ax5 = plt.subplots()
    y5 = np.ma.masked_equal([2, 4, 6, 8, 10, 12], 8)
    xmin5 = np.ma.masked_equal([0, 1, -1, 0, 2, 1], 2)
    xmax5 = np.ma.masked_equal([13, 14, 15, 16, 17, 18], 18)
    ax5.hlines(y5, xmin5, xmax5, colors='k', linewidth=2)
    ax5.set_ylim(0, 15)
@image_comparison(['vlines_hlines_blended_transform'], extensions=['png'], style='mpl20')
def mutated_test_vlines_hlines_blended_transform():
    t = np.arange(5.0, 10.0, 0.1)
    s = np.exp(-t) + np.sin(2 * np.pi * t) + 10
    fig, (hax, vax) = plt.subplots(2, 1, figsize=(6, 6))
    hax.plot(t, s, '^')
    hax.hlines([10, 9], xmin=0, xmax=0.5, transform=hax.get_yaxis_transform(), colors='r')
    vax.plot(t, s, '^')
    vax.vlines([6, 7], ymin=0, ymax=0.15, transform=vax.get_xaxis_transform(), colors='r')
@image_comparison(['step_linestyle', 'step_linestyle'], remove_text=True, tol=0.2)
def mutated_test_step_linestyle():
    x = y = np.arange(10)
    fig, ax_lst = plt.subplots(2, 2)
    ax_lst = ax_lst.flatten()
    ln_styles = ['-', '--', '-.', ':']
    for ax, ls in zip(ax_lst, ln_styles):
        ax.step(x, y, lw=5, linestyle=ls, where='pre')
        ax.step(x, y + 1, lw=5, linestyle=ls, where='mid')
        ax.step(x, y + 2, lw=5, linestyle=ls, where='post')
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 7])
    data = {'X': x, 'Y0': y, 'Y1': y + 1, 'Y2': y + 2}
    fig, ax_lst = plt.subplots(2, 2)
    ax_lst = ax_lst.flatten()
    ln_styles = ['-', '--', '-.', ':']
    for ax, ls in zip(ax_lst, ln_styles):
        ax.step('X', 'Y0', lw=5, linestyle=ls, where='pre', data=data)
        ax.step('X', 'Y1', lw=5, linestyle=ls, where='mid', data=data)
        ax.step('X', 'Y2', lw=5, linestyle=ls, where='post', data=data)
        ax.set_xlim([-1, 5])
        ax.set_ylim([-1, 7])
@image_comparison(['mixed_collection'], remove_text=True)
def mutated_test_mixed_collection():
    fig, ax = plt.subplots()
    c = mpatches.Circle((8, 8), radius=4, facecolor='none', edgecolor='green')
    p1 = mpl.collections.PatchCollection([c], match_original=True)
    p1.set_offsets([[0, 0], [24, 24]])
    p1.set_linewidths([1, 5])
    p2 = mpl.collections.PatchCollection([c], match_original=True)
    p2.set_offsets([[48, 0], [-32, -16]])
    p2.set_linewidths([1, 5])
    p2.set_edgecolors([[0, 0, 0.1, 1.0], [0, 0, 0.1, 0.5]])
    ax.patch.set_color('0.5')
    ax.add_collection(p1)
    ax.add_collection(p2)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
@image_comparison(['specgram_freqs.png', 'specgram_freqs_linear.png', 'specgram_noise.png', 'specgram_noise_linear.png'], remove_text=True, tol=0.07, style='default')
def mutated_test_specgram():
    """Test axes.specgram in default (psd) mode."""
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    n = 1000
    Fs = 10.0
    fstims = [[Fs / 4, Fs / 5, Fs / 11], [Fs / 4.7, Fs / 5.6, Fs / 11.9]]
    NFFT_freqs = int(10 * Fs / np.min(fstims))
    x = np.arange(0, n, 1 / Fs)
    y_freqs = np.concatenate(np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1))
    NFFT_noise = int(10 * Fs / 11)
    np.random.seed(0)
    y_noise = np.concatenate([np.random.standard_normal(n), np.random.rand(n)])
    all_sides = ['default', 'onesided', 'twosided']
    for y, NFFT in [(y_freqs, NFFT_freqs), (y_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides)
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, scale='linear', norm=matplotlib.colors.LogNorm())
@image_comparison(['specgram_magnitude_freqs.png', 'specgram_magnitude_freqs_linear.png', 'specgram_magnitude_noise.png', 'specgram_magnitude_noise_linear.png'], remove_text=True, tol=0.07, style='default')
def mutated_test_specgram_magnitude():
    """Test axes.specgram in magnitude mode."""
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    n = 1000
    Fs = 10.0
    fstims = [[Fs / 4, Fs / 5, Fs / 11], [Fs / 4.7, Fs / 5.6, Fs / 11.9]]
    NFFT_freqs = int(100 * Fs / np.min(fstims))
    x = np.arange(0, n, 1 / Fs)
    y = np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1)
    y[:, -1] = 1
    y_freqs = np.hstack(y)
    NFFT_noise = int(10 * Fs / 11)
    np.random.seed(0)
    y_noise = np.concatenate([np.random.standard_normal(n), np.random.rand(n)])
    all_sides = ['default', 'onesided', 'twosided']
    for y, NFFT in [(y_freqs, NFFT_freqs), (y_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, mode='magnitude')
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, mode='magnitude', scale='linear', norm=matplotlib.colors.LogNorm())
@image_comparison(['specgram_angle_freqs.png', 'specgram_phase_freqs.png', 'specgram_angle_noise.png', 'specgram_phase_noise.png'], remove_text=True, tol=0.07, style='default')
def mutated_test_specgram_angle():
    """Test axes.specgram in angle and phase modes."""
    matplotlib.rcParams['image.interpolation'] = 'nearest'
    n = 1000
    Fs = 10.0
    fstims = [[Fs / 4, Fs / 5, Fs / 11], [Fs / 4.7, Fs / 5.6, Fs / 11.9]]
    NFFT_freqs = int(10 * Fs / np.min(fstims))
    x = np.arange(0, n, 1 / Fs)
    y = np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1)
    y[:, -1] = 1
    y_freqs = np.hstack(y)
    NFFT_noise = int(10 * Fs / 11)
    np.random.seed(0)
    y_noise = np.concatenate([np.random.standard_normal(n), np.random.rand(n)])
    all_sides = ['default', 'onesided', 'twosided']
    for y, NFFT in [(y_freqs, NFFT_freqs), (y_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for mode in ['angle', 'phase']:
            for ax, sides in zip(plt.figure().subplots(3), all_sides):
                ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, mode=mode)
                with pytest.raises(ValueError):
                    ax.specgram(y, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, sides=sides, mode=mode, scale='dB')
@image_comparison(['psd_freqs.png', 'csd_freqs.png', 'psd_noise.png', 'csd_noise.png'], remove_text=True, tol=0.002)
def mutated_test_psd_csd():
    n = 10000
    Fs = 100.0
    fstims = [[Fs / 4, Fs / 5, Fs / 11], [Fs / 4.7, Fs / 5.6, Fs / 11.9]]
    NFFT_freqs = int(1000 * Fs / np.min(fstims))
    x = np.arange(0, n, 1 / Fs)
    ys_freqs = np.sin(2 * np.pi * np.multiply.outer(fstims, x)).sum(axis=1)
    NFFT_noise = int(1000 * Fs / 11)
    np.random.seed(0)
    ys_noise = [np.random.standard_normal(n), np.random.rand(n)]
    all_kwargs = [{'sides': 'default'}, {'sides': 'onesided', 'return_line': False}, {'sides': 'twosided', 'return_line': True}]
    for ys, NFFT in [(ys_freqs, NFFT_freqs), (ys_noise, NFFT_noise)]:
        noverlap = NFFT // 2
        pad_to = int(2 ** np.ceil(np.log2(NFFT)))
        for ax, kwargs in zip(plt.figure().subplots(3), all_kwargs):
            ret = ax.psd(np.concatenate(ys), NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, **kwargs)
            assert len(ret) == 2 + kwargs.get('return_line', False)
            ax.set(xlabel='', ylabel='')
        for ax, kwargs in zip(plt.figure().subplots(3), all_kwargs):
            ret = ax.csd(*ys, NFFT=NFFT, Fs=Fs, noverlap=noverlap, pad_to=pad_to, **kwargs)
            assert len(ret) == 2 + kwargs.get('return_line', False)
            ax.set(xlabel='', ylabel='')
@image_comparison(['magnitude_spectrum_freqs_linear.png', 'magnitude_spectrum_freqs_dB.png', 'angle_spectrum_freqs.png', 'phase_spectrum_freqs.png', 'magnitude_spectrum_noise_linear.png', 'magnitude_spectrum_noise_dB.png', 'angle_spectrum_noise.png', 'phase_spectrum_noise.png'], remove_text=True)
def mutated_test_spectrum():
    n = 10000
    Fs = 100.0
    fstims1 = [Fs / 4, Fs / 5, Fs / 11]
    NFFT = int(1000 * Fs / min(fstims1))
    pad_to = int(2 ** np.ceil(np.log2(NFFT)))
    x = np.arange(0, n, 1 / Fs)
    y_freqs = (np.sin(2 * np.pi * np.outer(x, fstims1)) * 10 ** np.arange(3)).sum(axis=1)
    np.random.seed(0)
    y_noise = np.hstack([np.random.standard_normal(n), np.random.rand(n)]) - 0.5
    all_sides = ['default', 'onesided', 'twosided']
    kwargs = {'Fs': Fs, 'pad_to': pad_to}
    for y in [y_freqs, y_noise]:
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.magnitude_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel='', ylabel='')
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.magnitude_spectrum(y, sides=sides, **kwargs, scale='dB')
            ax.set(xlabel='', ylabel='')
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.angle_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel='', ylabel='')
        for ax, sides in zip(plt.figure().subplots(3), all_sides):
            spec, freqs, line = ax.phase_spectrum(y, sides=sides, **kwargs)
            ax.set(xlabel='', ylabel='')
@image_comparison(['twin_spines.png'], remove_text=True, tol=0.022 if platform.machine() == 'arm64' else 0)
def mutated_test_twin_spines():

    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        ax.spines[:].set_visible(False)
    fig = plt.figure(figsize=(4, 3))
    fig.subplots_adjust(right=0.75)
    host = fig.add_subplot()
    par1 = host.twinx()
    par2 = host.twinx()
    par2.spines.right.set_position(('axes', 1.2))
    make_patch_spines_invisible(par2)
    par2.spines.right.set_visible(True)
    p1, = host.plot([0, 1, 2], [0, 1, 2], 'b-')
    p2, = par1.plot([0, 1, 2], [0, 3, 2], 'r-')
    p3, = par2.plot([0, 1, 2], [50, 30, 15], 'g-')
    host.set_xlim(0, 2)
    host.set_ylim(0, 2)
    par1.set_ylim(0, 4)
    par2.set_ylim(1, 65)
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)
@image_comparison(['twin_spines_on_top.png', 'twin_spines_on_top.png'], remove_text=True)
def mutated_test_twin_spines_on_top():
    matplotlib.rcParams['axes.linewidth'] = 48.0
    matplotlib.rcParams['lines.linewidth'] = 48.0
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    data = np.array([[1000, 1100, 1200, 1250], [310, 301, 360, 400]])
    ax2 = ax1.twinx()
    ax1.plot(data[0], data[1] / 1000.0, color='#BEAED4')
    ax1.fill_between(data[0], data[1] / 1000.0, color='#BEAED4', alpha=0.8)
    ax2.plot(data[0], data[1] / 1000.0, color='#7FC97F')
    ax2.fill_between(data[0], data[1] / 1000.0, color='#7FC97F', alpha=0.5)
    data = {'i': data[0], 'j': data[1] / 1000.0}
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = ax1.twinx()
    ax1.plot('i', 'j', color='#BEAED4', data=data)
    ax1.fill_between('i', 'j', color='#BEAED4', alpha=0.8, data=data)
    ax2.plot('i', 'j', color='#7FC97F', data=data)
    ax2.fill_between('i', 'j', color='#7FC97F', alpha=0.5, data=data)
@image_comparison(['pie_default.png'], tol=0.01)
def mutated_test_pie_default():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
@image_comparison(['pie_linewidth_0', 'pie_linewidth_0', 'pie_linewidth_0'], extensions=['png'], style='mpl20', tol=0.01)
def mutated_test_pie_linewidth_0():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0})
    plt.axis('equal')
    data = {'l': labels, 's': sizes, 'c': colors, 'ex': explode}
    fig = plt.figure()
    ax = fig.gca()
    ax.pie('s', explode='ex', labels='l', colors='c', autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, data=data)
    ax.axis('equal')
    plt.figure()
    plt.pie('s', explode='ex', labels='l', colors='c', autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, data=data)
    plt.axis('equal')
@image_comparison(['pie_center_radius.png'], style='mpl20', tol=0.01)
def mutated_test_pie_center_radius():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, center=(1, 2), radius=1.5)
    plt.annotate('Center point', xy=(1, 2), xytext=(1, 1.3), arrowprops=dict(arrowstyle='->', connectionstyle='arc3'), bbox=dict(boxstyle='square', facecolor='lightgrey'))
    plt.axis('equal')
@image_comparison(['pie_linewidth_2.png'], style='mpl20', tol=0.01)
def mutated_test_pie_linewidth_2():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 2})
    plt.axis('equal')
@image_comparison(['pie_ccw_true.png'], style='mpl20', tol=0.01)
def mutated_test_pie_ccw_true():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, counterclock=True)
    plt.axis('equal')
@image_comparison(['pie_frame_grid.png'], style='mpl20', tol=0.002)
def mutated_test_pie_frame_grid():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, frame=True, center=(2, 2))
    plt.pie(sizes[::-1], explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, frame=True, center=(5, 2))
    plt.pie(sizes, explode=explode[::-1], labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, wedgeprops={'linewidth': 0}, frame=True, center=(3, 5))
    plt.axis('equal')
@image_comparison(['pie_rotatelabels_true.png'], style='mpl20', tol=0.009)
def mutated_test_pie_rotatelabels_true():
    labels = ('Hogwarts', 'Frogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, rotatelabels=True)
    plt.axis('equal')
@image_comparison(['pie_no_label.png'], tol=0.01)
def mutated_test_pie_nolabel_but_legend():
    labels = ('Frogs', 'Hogs', 'Dogs', 'Logs')
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, labeldistance=None, rotatelabels=True)
    plt.axis('equal')
    plt.ylim(-1.2, 1.2)
    plt.legend()
@image_comparison(['pie_shadow.png'], style='mpl20', tol=0.002)
def mutated_test_pie_shadow():
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0)
    _, axes = plt.subplots(2, 2)
    axes[0][0].pie(sizes, explode=explode, colors=colors, shadow=True, startangle=90, wedgeprops={'linewidth': 0})
    axes[0][1].pie(sizes, explode=explode, colors=colors, shadow=False, startangle=90, wedgeprops={'linewidth': 0})
    axes[1][0].pie(sizes, explode=explode, colors=colors, shadow={'ox': -0.05, 'oy': -0.05, 'shade': 0.9, 'edgecolor': 'none'}, startangle=90, wedgeprops={'linewidth': 0})
    axes[1][1].pie(sizes, explode=explode, colors=colors, shadow={'ox': 0.05, 'linewidth': 2, 'shade': 0.2}, startangle=90, wedgeprops={'linewidth': 0})
@image_comparison(['set_get_ticklabels.png'], tol=0.025 if platform.machine() == 'arm64' else 0)
def mutated_test_set_get_ticklabels():
    fig, ax = plt.subplots(2)
    ha = ['normal', 'set_x/yticklabels']
    ax[0].plot(np.arange(10))
    ax[0].set_title(ha[0])
    ax[1].plot(np.arange(10))
    ax[1].set_title(ha[1])
    ax[0].set_xticks(range(10))
    ax[0].set_yticks(range(10))
    ax[0].set_xticklabels(['a', 'b', 'c', 'd'] + 6 * [''])
    ax[0].set_yticklabels(['11', '12', '13', '14'] + 6 * [''])
    ax[1].set_xticks(ax[0].get_xticks())
    ax[1].set_yticks(ax[0].get_yticks())
    ax[1].set_xticklabels(ax[0].get_xticklabels())
    ax[1].set_yticklabels(ax[0].get_yticklabels())
@image_comparison(['retain_tick_visibility.png'])
def mutated_test_retain_tick_visibility():
    fig, ax = plt.subplots()
    plt.plot([0, 1, 2], [0, -1, 4])
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='y', which='both', length=0)
@image_comparison(['o_marker_path_snap.png'], savefig_kwarg={'dpi': 72})
def mutated_test_o_marker_path_snap():
    fig, ax = plt.subplots()
    ax.margins(0.1)
    for ms in range(1, 15):
        ax.plot([1, 2], np.ones(2) + ms, 'o', ms=ms)
    for ms in np.linspace(1, 10, 25):
        ax.plot([3, 4], np.ones(2) + ms, 'o', ms=ms)
@image_comparison(['rc_spines.png'], savefig_kwarg={'dpi': 40})
def mutated_test_rc_spines():
    rc_dict = {'axes.spines.left': False, 'axes.spines.right': False, 'axes.spines.top': False, 'axes.spines.bottom': False}
    with matplotlib.rc_context(rc_dict):
        plt.subplots()
@image_comparison(['rc_grid.png'], savefig_kwarg={'dpi': 40})
def mutated_test_rc_grid():
    fig = plt.figure()
    rc_dict0 = {'axes.grid': True, 'axes.grid.axis': 'both'}
    rc_dict1 = {'axes.grid': True, 'axes.grid.axis': 'x'}
    rc_dict2 = {'axes.grid': True, 'axes.grid.axis': 'y'}
    dict_list = [rc_dict0, rc_dict1, rc_dict2]
    for i, rc_dict in enumerate(dict_list, 1):
        with matplotlib.rc_context(rc_dict):
            fig.add_subplot(3, 1, i)
@image_comparison(['dash_offset'], remove_text=True)
def mutated_test_dash_offset():
    fig, ax = plt.subplots()
    x = np.linspace(0, 10)
    y = np.ones_like(x)
    for j in range(0, 100, 2):
        ax.plot(x, j * y, ls=(j, (10, 10)), lw=5, color='k')
@image_comparison(['loglog.png'], remove_text=True, tol=0.02)
def mutated_test_loglog():
    fig, ax = plt.subplots()
    x = np.arange(1, 11)
    ax.loglog(x, x ** 3, lw=5)
    ax.tick_params(length=25, width=2)
    ax.tick_params(length=15, width=2, which='minor')
@image_comparison(['test_loglog_nonpos.png'], remove_text=True, style='mpl20', tol=0.029 if platform.machine() == 'arm64' else 0)
def mutated_test_loglog_nonpos():
    fig, axs = plt.subplots(3, 3)
    x = np.arange(1, 11)
    y = x ** 3
    y[7] = -3.0
    x[4] = -10
    for (mcy, mcx), ax in zip(product(['mask', 'clip', ''], repeat=2), axs.flat):
        if mcx == mcy:
            if mcx:
                ax.loglog(x, y ** 3, lw=2, nonpositive=mcx)
            else:
                ax.loglog(x, y ** 3, lw=2)
        else:
            ax.loglog(x, y ** 3, lw=2)
            if mcx:
                ax.set_xscale('log', nonpositive=mcx)
            if mcy:
                ax.set_yscale('log', nonpositive=mcy)
@image_comparison(['date_timezone_x.png'], tol=1.0)
def mutated_test_date_timezone_x():
    time_index = [datetime.datetime(2016, 2, 22, hour=x, tzinfo=dateutil.tz.gettz('Canada/Eastern')) for x in range(3)]
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date(time_index, [3] * 3, tz='Canada/Eastern')
    plt.subplot(2, 1, 2)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date(time_index, [3] * 3, tz='UTC')
@image_comparison(['date_timezone_y.png'])
def mutated_test_date_timezone_y():
    time_index = [datetime.datetime(2016, 2, 22, hour=x, tzinfo=dateutil.tz.gettz('Canada/Eastern')) for x in range(3)]
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date([3] * 3, time_index, tz='Canada/Eastern', xdate=False, ydate=True)
    plt.subplot(2, 1, 2)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date([3] * 3, time_index, tz='UTC', xdate=False, ydate=True)
@image_comparison(['date_timezone_x_and_y.png'], tol=1.0)
def mutated_test_date_timezone_x_and_y():
    UTC = datetime.timezone.utc
    time_index = [datetime.datetime(2016, 2, 22, hour=x, tzinfo=UTC) for x in range(3)]
    plt.figure(figsize=(20, 12))
    plt.subplot(2, 1, 1)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date(time_index, time_index, tz='UTC', ydate=True)
    plt.subplot(2, 1, 2)
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        plt.plot_date(time_index, time_index, tz='US/Eastern', ydate=True)
@image_comparison(['axisbelow.png'], remove_text=True)
def mutated_test_axisbelow():
    axs = plt.figure().subplots(ncols=3, sharex=True, sharey=True)
    settings = (False, 'line', True)
    for ax, setting in zip(axs, settings):
        ax.plot((0, 10), (0, 10), lw=10, color='m')
        circ = mpatches.Circle((3, 3), color='r')
        ax.add_patch(circ)
        ax.grid(color='c', linestyle='-', linewidth=3)
        ax.tick_params(top=False, bottom=False, left=False, right=False)
        ax.spines[:].set_visible(False)
        ax.set_axisbelow(setting)
        assert ax.get_axisbelow() == setting
@image_comparison(['inset_polar.png'], remove_text=True, style='mpl20')
def mutated_test_inset_polar():
    _, ax = plt.subplots()
    axins = ax.inset_axes([0.5, 0.1, 0.45, 0.45], polar=True)
    assert isinstance(axins, PolarAxes)
    r = np.arange(0, 2, 0.01)
    theta = 2 * np.pi * r
    ax.plot(theta, r)
    axins.plot(theta, r)
@image_comparison(['annotate_across_transforms.png'], style='mpl20', remove_text=True, tol=0.025 if platform.machine() == 'arm64' else 0)
def mutated_test_annotate_across_transforms():
    x = np.linspace(0, 10, 200)
    y = np.exp(-x) * np.sin(x)
    fig, ax = plt.subplots(figsize=(3.39, 3))
    ax.plot(x, y)
    axins = ax.inset_axes([0.4, 0.5, 0.3, 0.3])
    axins.set_aspect(0.2)
    axins.xaxis.set_visible(False)
    axins.yaxis.set_visible(False)
    ax.annotate('', xy=(x[150], y[150]), xycoords=ax.transData, xytext=(1, 0), textcoords=axins.transAxes, arrowprops=dict(arrowstyle='->'))
@image_comparison(['secondary_xy.png'], style='mpl20', tol=0.027 if platform.machine() == 'arm64' else 0)
def mutated_test_secondary_xy():
    fig, axs = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    def invert(x):
        with np.errstate(divide='ignore'):
            return 1 / x
    for nn, ax in enumerate(axs):
        ax.plot(np.arange(2, 11), np.arange(2, 11))
        if nn == 0:
            secax = ax.secondary_xaxis
        else:
            secax = ax.secondary_yaxis
        secax(0.2, functions=(invert, invert))
        secax(0.4, functions=(lambda x: 2 * x, lambda x: x / 2))
        secax(0.6, functions=(lambda x: x ** 2, lambda x: x ** (1 / 2)))
        secax(0.8)
        secax('top' if nn == 0 else 'right', functions=_Translation(2))
        secax(6.25, transform=ax.transData)
@image_comparison(['axis_options.png'], remove_text=True, style='mpl20')
def mutated_test_axis_options():
    fig, axes = plt.subplots(2, 3)
    for i, option in enumerate(('scaled', 'tight', 'image')):
        axes[0, i].plot((1, 2), (1, 3.2))
        axes[0, i].axis(option)
        axes[0, i].add_artist(mpatches.Circle((1.5, 1.5), radius=0.5, facecolor='none', edgecolor='k'))
        axes[1, i].plot((1, 2.25), (1, 1.75))
        axes[1, i].axis(option)
        axes[1, i].add_artist(mpatches.Circle((1.5, 1.25), radius=0.25, facecolor='none', edgecolor='k'))
@image_comparison(['test_centered_bar_label_nonlinear.svg'])
def mutated_test_centered_bar_label_nonlinear():
    _, ax = plt.subplots()
    bar_container = ax.barh(['c', 'b', 'a'], [1000, 5000, 7000])
    ax.set_xscale('log')
    ax.set_xlim(1, None)
    ax.bar_label(bar_container, label_type='center')
    ax.set_axis_off()
@image_comparison(['extent_units.png'], style='mpl20')
def mutated_test_extent_units():
    _, axs = plt.subplots(2, 2)
    date_first = np.datetime64('2020-01-01', 'D')
    date_last = np.datetime64('2020-01-11', 'D')
    arr = [[i + j for i in range(10)] for j in range(10)]
    axs[0, 0].set_title('Date extents on y axis')
    im = axs[0, 0].imshow(arr, origin='lower', extent=[1, 11, date_first, date_last], cmap=mpl.colormaps['plasma'])
    axs[0, 1].set_title('Date extents on x axis (Day of Jan 2020)')
    im = axs[0, 1].imshow(arr, origin='lower', extent=[date_first, date_last, 1, 11], cmap=mpl.colormaps['plasma'])
    axs[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    im = axs[1, 0].imshow(arr, origin='lower', extent=[date_first, date_last, date_first, date_last], cmap=mpl.colormaps['plasma'])
    axs[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    axs[1, 0].set(xlabel='Day of Jan 2020')
    im = axs[1, 1].imshow(arr, origin='lower', cmap=mpl.colormaps['plasma'])
    im.set_extent([date_last, date_first, date_last, date_first])
    axs[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    axs[1, 1].set(xlabel='Day of Jan 2020')
    with pytest.raises(TypeError, match='set_extent\\(\\) got an unexpected'):
        im.set_extent([2, 12, date_first, date_last], clip=False)
@image_comparison(['preset_clip_paths.png'], remove_text=True, style='mpl20', tol=0.027 if platform.machine() == 'arm64' else 0)
def mutated_test_preset_clip_paths():
    fig, ax = plt.subplots()
    poly = mpl.patches.Polygon([[1, 0], [0, 1], [-1, 0], [0, -1]], facecolor='#ddffdd', edgecolor='#00ff00', linewidth=2, alpha=0.5)
    ax.add_patch(poly)
    line = mpl.lines.Line2D((-1, 1), (0.5, 0.5), clip_on=True, clip_path=poly)
    line.set_path_effects([patheffects.withTickedStroke()])
    ax.add_artist(line)
    line = mpl.lines.Line2D((-1, 1), (-0.5, -0.5), color='r', clip_on=True, clip_path=poly)
    ax.add_artist(line)
    poly2 = mpl.patches.Polygon([[-1, 1], [0, 1], [0, -0.25]], facecolor='#beefc0', alpha=0.3, edgecolor='#faded0', linewidth=2, clip_on=True, clip_path=poly)
    ax.add_artist(poly2)
    ax.annotate('Annotation', (-0.75, -0.75), xytext=(0.1, 0.75), arrowprops={'color': 'k'}, clip_on=True, clip_path=poly)
    poly3 = mpl.patches.Polygon([[0, 0], [0, 0.5], [0.5, 0.5], [0.5, 0]], facecolor='g', edgecolor='y', linewidth=2, alpha=0.3, clip_on=True, clip_path=poly)
    fig.add_artist(poly3, clip=True)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
@image_comparison(['axhvlinespan_interpolation.png'], style='default')
def mutated_test_axhvlinespan_interpolation():
    ax = plt.figure().add_subplot(projection='polar')
    ax.set_axis_off()
    ax.axvline(0.1, c='C0')
    ax.axvspan(0.2, 0.3, fc='C1')
    ax.axvspan(0.4, 0.5, 0.1, 0.2, fc='C2')
    ax.axhline(1, c='C0', alpha=0.5)
    ax.axhspan(0.8, 0.9, fc='C1', alpha=0.5)
    ax.axhspan(0.6, 0.7, 0.8, 0.9, fc='C2', alpha=0.5)
