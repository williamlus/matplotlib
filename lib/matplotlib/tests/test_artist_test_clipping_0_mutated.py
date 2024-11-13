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

def test_clipping_0_mutated():
    exterior = mpath.Path.unit_rectangle().deepcopy()
    exterior.vertices *= 4
    exterior.vertices -= 2
    interior = mpath.Path.unit_circle().deepcopy()
    interior.vertices = interior.vertices[::-1]
    clip_path = mpath.Path.make_compound_path(exterior, interior)
    star = mpath.Path.unit_regular_star(6).deepcopy()
    star.vertices *= 2.6
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True, squeeze=True)
    col = mcollections.PathCollection([star], lw=5, edgecolor='blue', facecolor='red', alpha=0.7, hatch='*')
    col.set_clip_path(clip_path, ax1.transData)
    ax1.add_collection(col)
    patch = mpatches.PathPatch(star, lw=5, edgecolor='blue', facecolor='red', alpha=0.7, hatch='*')
    patch.set_clip_path(clip_path, ax2.transData)
    ax2.add_patch(patch)
    ax1.set_xlim([-3, 3])
    ax1.set_ylim([-3, 3])
# Mutation info: Added squeeze = True (Call plt.subplots)