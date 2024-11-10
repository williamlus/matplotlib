from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_tight_raster_2_mutated():
    """Test rasterization with tight_layout"""
    fig, ax = plt.subplots(sharey=False)
    ax.plot([1.0, 2.0], rasterized=True)