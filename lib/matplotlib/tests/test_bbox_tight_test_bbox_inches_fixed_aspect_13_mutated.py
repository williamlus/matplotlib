from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_fixed_aspect_13_mutated():
    with plt.rc_context({'figure.constrained_layout.use': True}):
        fig, ax = plt.subplots()
        ax.plot([0, 1])
        ax.set_xlim(0, 1)
        ax.set_aspect('equal')
# Mutation info: (0-th Positional) aspect = 'equal' -> aspect = equal (Call ax.set_aspect)