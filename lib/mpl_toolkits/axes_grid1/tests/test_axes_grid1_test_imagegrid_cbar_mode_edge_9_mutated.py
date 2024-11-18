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

@image_comparison(['imagegrid_cbar_mode.png'], remove_text=True, style='mpl20', tol=0.3)
def test_imagegrid_cbar_mode_edge_9_mutated():
    arr = np.arange(16).reshape((4, 4))
    fig = plt.figure(figsize=(18, 9))
    positions = (241, 242, 243, 244, 245, 246, 247, 248)
    directions = ['row'] * 4 + ['column'] * 4
    cbar_locations = ['left', 'right', 'top', 'bottom'] * 2
    for position, direction, location in zip(positions, directions, cbar_locations):
        grid = ImageGrid(fig, position, nrows_ncols=(2, 2), direction=direction, cbar_location=location, cbar_size='20%', cbar_mode='edge')
        ax1, ax2, ax3, ax4 = grid
        ax1.imshow(arr, cmap='nipy_spectral', interpolation_stage='auto')
        ax2.imshow(arr.T, cmap='hot')
        ax3.imshow(np.hypot(arr, arr.T), cmap='jet')
        ax4.imshow(np.arctan2(arr, arr.T), cmap='hsv')
        for ax in grid:
            ax.cax.cla()
            cb = ax.cax.colorbar(ax.images[0])
# Mutation info: Added interpolation_stage = auto (Call ax1.imshow)