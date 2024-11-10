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

def test_image_grid_single_bottom_7_mutated():
    imdata = np.arange(100).reshape((10, 10))
    fig = plt.figure(1, (2.5, 1.5), clear=True)
    grid = ImageGrid(fig, (0, 0, 1, 1), nrows_ncols=(1, 3), axes_pad=(0.2, 0.15), cbar_mode='single', cbar_pad=0.3, cbar_location='bottom', cbar_size='10%', label_mode='1')
    assert type(grid.get_divider()) is Divider
    for i in range(3):
        im = grid[i].imshow(imdata, interpolation='none')
    grid.cbar_axes[0].colorbar(im)