import io
from itertools import chain
import numpy as np
import pytest
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.path as mpath
import matplotlib.transforms as mtransforms
import matplotlib.collections as mcollections
import matplotlib.artist as martist
import matplotlib.backend_bases as mbackend_bases
import matplotlib as mpl
from matplotlib.testing.decorators import check_figures_equal, image_comparison
@image_comparison(['clip_path_clipping'], remove_text=True)
def mutated_test_clipping():
    exterior = mpath.Path.unit_rectangle().deepcopy()
    exterior.vertices *= 4
    exterior.vertices -= 2
    interior = mpath.Path.unit_circle().deepcopy()
    interior.vertices = interior.vertices[::-1]
    clip_path = mpath.Path.make_compound_path(exterior, interior)
    star = mpath.Path.unit_regular_star(6).deepcopy()
    star.vertices *= 2.6
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
    col = mcollections.PathCollection([star], lw=5, edgecolor='blue', facecolor='red', alpha=0.7, hatch='*')
    col.set_clip_path(clip_path, ax1.transData)
    ax1.add_collection(col)
    patch = mpatches.PathPatch(star, lw=5, edgecolor='blue', facecolor='red', alpha=0.7, hatch='*')
    patch.set_clip_path(clip_path, ax2.transData)
    ax2.add_patch(patch)
    ax1.set_xlim([-3, 3])
    ax1.set_ylim([-3, 3])
@image_comparison(['hatching'], remove_text=True, style='default')
def mutated_test_hatching():
    fig, ax = plt.subplots(1, 1)
    rect1 = mpatches.Rectangle((0, 0), 3, 4, hatch='/')
    ax.add_patch(rect1)
    rect2 = mcollections.RegularPolyCollection(4, sizes=[16000], offsets=[(1.5, 6.5)], offset_transform=ax.transData, hatch='/')
    ax.add_collection(rect2)
    rect3 = mpatches.Rectangle((4, 0), 3, 4, hatch='/', edgecolor='C1')
    ax.add_patch(rect3)
    rect4 = mcollections.RegularPolyCollection(4, sizes=[16000], offsets=[(5.5, 6.5)], offset_transform=ax.transData, hatch='/', edgecolor='C1')
    ax.add_collection(rect4)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 9)
@image_comparison(['default_edges.png'], remove_text=True, style='default')
def mutated_test_default_edges():
    plt.rcParams['text.kerning_factor'] = 6
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    ax1.plot(np.arange(10), np.arange(10), 'x', np.arange(10) + 1, np.arange(10), 'o')
    ax2.bar(np.arange(10), np.arange(10), align='edge')
    ax3.text(0, 0, 'BOX', size=24, bbox=dict(boxstyle='sawtooth'))
    ax3.set_xlim((-1, 1))
    ax3.set_ylim((-1, 1))
    pp1 = mpatches.PathPatch(mpath.Path([(0, 0), (1, 0), (1, 1), (0, 0)], [mpath.Path.MOVETO, mpath.Path.CURVE3, mpath.Path.CURVE3, mpath.Path.CLOSEPOLY]), fc='none', transform=ax4.transData)
    ax4.add_patch(pp1)
