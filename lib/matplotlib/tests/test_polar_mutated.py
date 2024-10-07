import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal
@image_comparison(['polar_axes'], style='default', tol=0.012)
def mutated_test_polar_annotations():
    r = np.arange(0.0, 1.0, 0.001)
    theta = 2.0 * 2.0 * np.pi * r
    fig = plt.figure()
    ax = fig.add_subplot(polar=True)
    line, = ax.plot(theta, r, color='#ee8d18', lw=3)
    line, = ax.plot((0, 0), (0, 1), color='#0000ff', lw=1)
    ind = 800
    thisr, thistheta = (r[ind], theta[ind])
    ax.plot([thistheta], [thisr], 'o')
    ax.annotate('a polar annotation', xy=(thistheta, thisr), xytext=(0.05, 0.05), textcoords='figure fraction', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='left', verticalalignment='baseline')
    ax.tick_params(axis='x', tick1On=True, tick2On=True, direction='out')
@image_comparison(['polar_coords'], style='default', remove_text=True, tol=0.014)
def mutated_test_polar_coord_annotations():
    el = mpl.patches.Ellipse((0, 0), 10, 20, facecolor='r', alpha=0.5)
    fig = plt.figure()
    ax = fig.add_subplot(aspect='equal')
    ax.add_artist(el)
    el.set_clip_box(ax.bbox)
    ax.annotate('the top', xy=(np.pi / 2.0, 10.0), xytext=(np.pi / 3, 20.0), xycoords='polar', textcoords='polar', arrowprops=dict(facecolor='black', shrink=0.05), horizontalalignment='left', verticalalignment='baseline', clip_on=True)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
@image_comparison(['polar_alignment.png'])
def mutated_test_polar_alignment():
    angles = np.arange(0, 360, 90)
    grid_values = [0, 0.2, 0.4, 0.6, 0.8, 1]
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    horizontal = fig.add_axes(rect, polar=True, label='horizontal')
    horizontal.set_thetagrids(angles)
    vertical = fig.add_axes(rect, polar=True, label='vertical')
    vertical.patch.set_visible(False)
    for i in range(2):
        fig.axes[i].set_rgrids(grid_values, angle=angles[i], horizontalalignment='left', verticalalignment='top')
@image_comparison(['polar_rmin'], style='default')
def mutated_test_polar_rmin():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.plot(theta, r)
    ax.set_rmax(2.0)
    ax.set_rmin(0.5)
@image_comparison(['polar_negative_rmin'], style='default')
def mutated_test_polar_negative_rmin():
    r = np.arange(-3.0, 0.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.plot(theta, r)
    ax.set_rmax(0.0)
    ax.set_rmin(-3.0)
@image_comparison(['polar_rorigin'], style='default')
def mutated_test_polar_rorigin():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.plot(theta, r)
    ax.set_rmax(2.0)
    ax.set_rmin(0.5)
    ax.set_rorigin(0.0)
@image_comparison(['polar_invertedylim.png'], style='default')
def mutated_test_polar_invertedylim():
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.set_ylim(2, 0)
@image_comparison(['polar_invertedylim_rorigin.png'], style='default')
def mutated_test_polar_invertedylim_rorigin():
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.yaxis.set_inverted(True)
    ax.plot([0, 0], [0, 2], c='none')
    ax.margins(0)
    ax.set_rorigin(3)
@image_comparison(['polar_theta_position'], style='default')
def mutated_test_polar_theta_position():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.plot(theta, r)
    ax.set_theta_zero_location('NW', 30)
    ax.set_theta_direction('clockwise')
@image_comparison(['polar_rlabel_position'], style='default')
def mutated_test_polar_rlabel_position():
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
@image_comparison(['polar_theta_wedge'], style='default')
def mutated_test_polar_theta_limits():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    theta_mins = np.arange(15.0, 361.0, 90.0)
    theta_maxs = np.arange(50.0, 361.0, 90.0)
    DIRECTIONS = ('out', 'in', 'inout')
    fig, axs = plt.subplots(len(theta_mins), len(theta_maxs), subplot_kw={'polar': True}, figsize=(8, 6))
    for i, start in enumerate(theta_mins):
        for j, end in enumerate(theta_maxs):
            ax = axs[i, j]
            ax.plot(theta, r)
            if start < end:
                ax.set_thetamin(start)
                ax.set_thetamax(end)
            else:
                ax.set_thetamin(end)
                ax.set_thetamax(start)
                ax.set_theta_direction('clockwise')
            ax.tick_params(tick1On=True, tick2On=True, direction=DIRECTIONS[i % len(DIRECTIONS)], rotation='auto')
            ax.yaxis.set_tick_params(label2On=True, rotation='auto')
            ax.xaxis.get_major_locator().base.set_params(steps=[1, 2, 2.5, 5, 10])
@image_comparison(['polar_log.png'], style='default')
def mutated_test_polar_log():
    fig = plt.figure()
    ax = fig.add_subplot(polar=True)
    ax.set_rscale('log')
    ax.set_rlim(1, 1000)
    n = 100
    ax.plot(np.linspace(0, 2 * np.pi, n), np.logspace(0, 2, n))
