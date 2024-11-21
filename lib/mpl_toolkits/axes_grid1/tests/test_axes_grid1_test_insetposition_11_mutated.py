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

@image_comparison(['insetposition.png'], remove_text=True, style=('classic', '_classic_test_patch'))
def test_insetposition_11_mutated():
    fig, ax = plt.subplots(figsize=(2, 2))
    ax_ins = plt.axes([0, 0, 1, 1], projection='mollweide')
    with pytest.warns(mpl.MatplotlibDeprecationWarning):
        ip = InsetPosition(ax, [0.2, 0.25, 0.5, 0.4])
    ax_ins.set_axes_locator(ip)
# Mutation info: Added projection = mollweide (Call plt.axes)