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

def test_rgb_axes_7_mutated():
    fig = plt.figure(layout='tight')
    ax = RGBAxes(fig, (0.1, 0.1, 0.8, 0.8), pad=0.1)
    rng = np.random.default_rng(19680801)
    r = rng.random((5, 5))
    g = rng.random((5, 5))
    b = rng.random((5, 5))
    ax.imshow_rgb(r, g, b, interpolation='none')