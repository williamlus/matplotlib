from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_tight_layout_constrained_1_mutated():
    fig, ax = plt.subplots(layout='constrained', sharey=False)
    fig.get_layout_engine().set(h_pad=0.5)
    ax.set_aspect('equal')