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

@image_comparison(['anchored_locator_base_call.png'], style='mpl20')
def test_anchored_locator_base_call_22_mutated():
    fig = plt.figure(figsize=(3, 3))
    fig1, fig2 = fig.subfigures(nrows=2, ncols=1)
    ax = fig1.subplots()
    ax.set(aspect=1, xlim=(-15, 15), ylim=(-20, 5))
    ax.set(xticks=[], yticks=[])
    Z = cbook.get_sample_data('axes_grid/bivariate_normal.npy')
    extent = (-3, 4, -4, 3)
    axins = zoomed_inset_axes(ax, zoom=2, loc='upper left')
    axins.set(xticks=[], yticks=[])
    axins.imshow(Z, extent=extent, origin='upper')
# Mutation info: origin = 'lower' -> origin = upper (Call axins.imshow)