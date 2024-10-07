"""
Tests specific to the patches module.
"""
import platform
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal
import pytest
import matplotlib as mpl
from matplotlib.patches import Annulus, Ellipse, Patch, Polygon, Rectangle, FancyArrowPatch, FancyArrow, BoxStyle, Arc
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
from matplotlib import collections as mcollections, colors as mcolors, patches as mpatches, path as mpath, transforms as mtransforms, rcParams
@image_comparison(['clip_to_bbox'])
def mutated_test_clip_to_bbox():
    fig, ax = plt.subplots()
    ax.set_xlim([-18, 20])
    ax.set_ylim([-150, 100])
    path = mpath.Path.unit_regular_star(8).deepcopy()
    path.vertices *= [10, 100]
    path.vertices -= [5, 25]
    path2 = mpath.Path.unit_circle().deepcopy()
    path2.vertices *= [10, 100]
    path2.vertices += [10, -25]
    combined = mpath.Path.make_compound_path(path, path2)
    patch = mpatches.PathPatch(combined, alpha=0.5, facecolor='coral', edgecolor='none')
    ax.add_patch(patch)
    bbox = mtransforms.Bbox([[-12, -77.5], [50, -110]])
    result_path = combined.clip_to_bbox(bbox)
    result_patch = mpatches.PathPatch(result_path, alpha=0.5, facecolor='green', lw=4, edgecolor='black')
    ax.add_patch(result_patch)
@image_comparison(['patch_alpha_coloring'], remove_text=True)
def mutated_test_patch_alpha_coloring():
    """
    Test checks that the patch and collection are rendered with the specified
    alpha values in their facecolor and edgecolor.
    """
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    verts = np.concatenate([circle.vertices, star.vertices[::-1]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star1 = mpath.Path(verts, codes)
    cut_star2 = mpath.Path(verts + 1, codes)
    ax = plt.axes()
    col = mcollections.PathCollection([cut_star2], linewidth=5, linestyles='dashdot', facecolor=(1, 0, 0, 0.5), edgecolor=(0, 0, 1, 0.75))
    ax.add_collection(col)
    patch = mpatches.PathPatch(cut_star1, linewidth=5, linestyle='dashdot', facecolor=(1, 0, 0, 0.5), edgecolor=(0, 0, 1, 0.75))
    ax.add_patch(patch)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
@image_comparison(['patch_alpha_override'], remove_text=True)
def mutated_test_patch_alpha_override():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    verts = np.concatenate([circle.vertices, star.vertices[::-1]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star1 = mpath.Path(verts, codes)
    cut_star2 = mpath.Path(verts + 1, codes)
    ax = plt.axes()
    col = mcollections.PathCollection([cut_star2], linewidth=5, linestyles='dashdot', alpha=0.25, facecolor=(1, 0, 0, 0.5), edgecolor=(0, 0, 1, 0.75))
    ax.add_collection(col)
    patch = mpatches.PathPatch(cut_star1, linewidth=5, linestyle='dashdot', alpha=0.25, facecolor=(1, 0, 0, 0.5), edgecolor=(0, 0, 1, 0.75))
    ax.add_patch(patch)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
@image_comparison(['patch_custom_linestyle'], remove_text=True)
def mutated_test_patch_custom_linestyle():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    verts = np.concatenate([circle.vertices, star.vertices[::-1]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star1 = mpath.Path(verts, codes)
    cut_star2 = mpath.Path(verts + 1, codes)
    ax = plt.axes()
    col = mcollections.PathCollection([cut_star2], linewidth=5, linestyles=[(0, (5, 7, 10, 7))], facecolor=(1, 0, 0), edgecolor=(0, 0, 1))
    ax.add_collection(col)
    patch = mpatches.PathPatch(cut_star1, linewidth=5, linestyle=(0, (5, 7, 10, 7)), facecolor=(1, 0, 0), edgecolor=(0, 0, 1))
    ax.add_patch(patch)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
@image_comparison(['wedge_range'], remove_text=True, tol=0.009 if platform.machine() == 'arm64' else 0)
def mutated_test_wedge_range():
    ax = plt.axes()
    t1 = 2.313869244286224
    args = [[52.31386924, 232.31386924], [52.313869244286224, 232.31386924428622], [t1, t1 + 180.0], [0, 360], [90, 90 + 360], [-180, 180], [0, 380], [45, 46], [46, 45]]
    for i, (theta1, theta2) in enumerate(args):
        x = i % 3
        y = i // 3
        wedge = mpatches.Wedge((x * 3, y * 3), 1, theta1, theta2, facecolor='none', edgecolor='k', lw=3)
        ax.add_artist(wedge)
    ax.set_xlim(-2, 8)
    ax.set_ylim(-2, 9)
@image_comparison(['multi_color_hatch'], remove_text=True, style='default')
def mutated_test_multi_color_hatch():
    fig, ax = plt.subplots()
    rects = ax.bar(range(5), range(1, 6))
    for i, rect in enumerate(rects):
        rect.set_facecolor('none')
        rect.set_edgecolor(f'C{i}')
        rect.set_hatch('/')
    ax.autoscale_view()
    ax.autoscale(False)
    for i in range(5):
        with mpl.style.context({'hatch.color': f'C{i}'}):
            r = Rectangle((i - 0.8 / 2, 5), 0.8, 1, hatch='//', fc='none')
        ax.add_patch(r)
@image_comparison(['units_rectangle.png'])
def mutated_test_units_rectangle():
    import matplotlib.testing.jpl_units as U
    U.register()
    p = mpatches.Rectangle((5 * U.km, 6 * U.km), 1 * U.km, 2 * U.km)
    fig, ax = plt.subplots()
    ax.add_patch(p)
    ax.set_xlim([4 * U.km, 7 * U.km])
    ax.set_ylim([5 * U.km, 9 * U.km])
@image_comparison(['connection_patch.png'], style='mpl20', remove_text=True, tol=0.024 if platform.machine() == 'arm64' else 0)
def mutated_test_connection_patch():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    con = mpatches.ConnectionPatch(xyA=(0.1, 0.1), xyB=(0.9, 0.9), coordsA='data', coordsB='data', axesA=ax2, axesB=ax1, arrowstyle='->')
    ax2.add_artist(con)
    xyA = (0.6, 1.0)
    xyB = (0.0, 0.2)
    coordsA = 'axes fraction'
    coordsB = ax2.get_yaxis_transform()
    con = mpatches.ConnectionPatch(xyA=xyA, xyB=xyB, coordsA=coordsA, coordsB=coordsB, arrowstyle='-')
    ax2.add_artist(con)
@image_comparison(['large_arc.svg'], style='mpl20')
def mutated_test_large_arc():
    fig, (ax1, ax2) = plt.subplots(1, 2)
    x = 210
    y = -2115
    diameter = 4261
    for ax in [ax1, ax2]:
        a = Arc((x, y), diameter, diameter, lw=2, color='k')
        ax.add_patch(a)
        ax.set_axis_off()
        ax.set_aspect('equal')
    ax1.set_xlim(7, 8)
    ax1.set_ylim(5, 6)
    ax2.set_xlim(-25000, 18000)
    ax2.set_ylim(-20000, 6600)
@image_comparison(['all_quadrants_arcs.svg'], style='mpl20')
def mutated_test_rotated_arcs():
    fig, ax_arr = plt.subplots(2, 2, squeeze=False, figsize=(10, 10))
    scale = 10000000
    diag_centers = ((-1, -1), (-1, 1), (1, 1), (1, -1))
    on_axis_centers = ((0, 1), (1, 0), (0, -1), (-1, 0))
    skews = ((2, 2), (2, 1 / 10), (2, 1 / 100), (2, 1 / 1000))
    for ax, (sx, sy) in zip(ax_arr.ravel(), skews):
        k = 0
        for prescale, centers in zip((1 - 0.0001, (1 - 0.0001) / np.sqrt(2)), (on_axis_centers, diag_centers)):
            for j, (x_sign, y_sign) in enumerate(centers, start=k):
                a = Arc((x_sign * scale * prescale, y_sign * scale * prescale), scale * sx, scale * sy, lw=4, color=f'C{j}', zorder=1 + j, angle=np.rad2deg(np.arctan2(y_sign, x_sign)) % 360, label=f'big {j}', gid=f'big {j}')
                ax.add_patch(a)
            k = j + 1
        ax.set_xlim(-scale / 4000, scale / 4000)
        ax.set_ylim(-scale / 4000, scale / 4000)
        ax.axhline(0, color='k')
        ax.axvline(0, color='k')
        ax.set_axis_off()
        ax.set_aspect('equal')
@image_comparison(baseline_images=['annulus'], extensions=['png'])
def mutated_test_annulus():
    fig, ax = plt.subplots()
    cir = Annulus((0.5, 0.5), 0.2, 0.05, fc='g')
    ell = Annulus((0.5, 0.5), (0.5, 0.3), 0.1, 45, fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal')
@image_comparison(baseline_images=['annulus'], extensions=['png'])
def mutated_test_annulus_setters():
    fig, ax = plt.subplots()
    cir = Annulus((0.0, 0.0), 0.2, 0.01, fc='g')
    ell = Annulus((0.0, 0.0), (1, 2), 0.1, 0, fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal')
    cir.center = (0.5, 0.5)
    cir.radii = 0.2
    cir.width = 0.05
    ell.center = (0.5, 0.5)
    ell.radii = (0.5, 0.3)
    ell.width = 0.1
    ell.angle = 45
@image_comparison(baseline_images=['annulus'], extensions=['png'])
def mutated_test_annulus_setters2():
    fig, ax = plt.subplots()
    cir = Annulus((0.0, 0.0), 0.2, 0.01, fc='g')
    ell = Annulus((0.0, 0.0), (1, 2), 0.1, 0, fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal')
    cir.center = (0.5, 0.5)
    cir.set_semimajor(0.2)
    cir.set_semiminor(0.2)
    assert cir.radii == (0.2, 0.2)
    cir.width = 0.05
    ell.center = (0.5, 0.5)
    ell.set_semimajor(0.5)
    ell.set_semiminor(0.3)
    assert ell.radii == (0.5, 0.3)
    ell.width = 0.1
    ell.angle = 45
@image_comparison(['autoscale_arc'], extensions=['png', 'svg'], style='mpl20', remove_text=True)
def mutated_test_autoscale_arc():
    fig, axs = plt.subplots(1, 3, figsize=(4, 1))
    arc_lists = ([Arc((0, 0), 1, 1, theta1=0, theta2=90)], [Arc((0.5, 0.5), 1.5, 0.5, theta1=10, theta2=20)], [Arc((0.5, 0.5), 1.5, 0.5, theta1=10, theta2=20), Arc((0.5, 0.5), 2.5, 0.5, theta1=110, theta2=120), Arc((0.5, 0.5), 3.5, 0.5, theta1=210, theta2=220), Arc((0.5, 0.5), 4.5, 0.5, theta1=310, theta2=320)])
    for ax, arcs in zip(axs, arc_lists):
        for arc in arcs:
            ax.add_patch(arc)
        ax.autoscale()
