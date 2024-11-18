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

@image_comparison(['image_grid_each_left_label_mode_all.png'], style='mpl20', savefig_kwarg={'bbox_inches': 'tight'})
def test_image_grid_each_left_label_mode_all_18_mutated():
    imdata = np.arange(100).reshape((10, 10))
    fig = plt.figure(1, (3, 3))
    grid = ImageGrid(fig, (1, 1, 1), nrows_ncols=(3, 2), axes_pad=(0.5, 0.3), cbar_mode='each', cbar_location='left', cbar_size='15%', label_mode='all')
    assert isinstance(grid.get_divider(), SubplotDivider)
    assert grid.get_axes_pad() == (0.5, 0.3)
    assert grid.get_aspect()
    for ax, cax in zip(grid, grid.cbar_axes):
        im = ax.imshow(imdata, interpolation='none', resample=False)
        cax.colorbar(im)
# Mutation info: Added resample = False (Call ax.imshow)