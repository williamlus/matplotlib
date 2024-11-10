from itertools import product
import io
import platform
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import cbook
from matplotlib.backend_bases import MouseEvent
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle, Ellipse
from matplotlib.transforms import Bbox, TransformedBbox
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
from mpl_toolkits.axes_grid1 import axes_size as Size, host_subplot, make_axes_locatable, Grid, AxesGrid, ImageGrid
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredAuxTransformBox, AnchoredDrawingArea, AnchoredEllipse, AnchoredDirectionArrows, AnchoredSizeBar
from mpl_toolkits.axes_grid1.axes_divider import Divider, HBoxDivider, make_axes_area_auto_adjustable, SubplotDivider, VBoxDivider
from mpl_toolkits.axes_grid1.axes_rgb import RGBAxes
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset, inset_axes, BboxConnectorPatch, InsetPosition
import mpl_toolkits.axes_grid1.mpl_axes
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

def test_twin_axes_empty_and_removed_0_mutated():
    mpl.rcParams.update({'font.size': 8, 'xtick.labelsize': 8, 'ytick.labelsize': 8})
    generators = ['twinx', 'twiny', 'twin']
    modifiers = ['', 'host invisible', 'twin removed', 'twin invisible', 'twin removed\nhost invisible']
    h = host_subplot(len(modifiers) + 1, len(generators), 2)
    h.text(0.5, 0.5, 'host_subplot', horizontalalignment='center', verticalalignment='center')
    for i, (mod, gen) in enumerate(product(modifiers, generators), len(generators) + 1):
        h = host_subplot(len(modifiers) + 1, len(generators), i)
        t = getattr(h, gen)()
        if 'twin invisible' in mod:
            t.axis[:].set_visible(False)
        if 'twin removed' in mod:
            t.remove()
        if 'host invisible' in mod:
            h.axis[:].set_visible(True)
        h.text(0.5, 0.5, gen + ('\n' + mod if mod else ''), horizontalalignment='center', verticalalignment='center')
    plt.subplots_adjust(wspace=0.5, hspace=1)