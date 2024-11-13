from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_tight_suptitle_non_default_5_mutated():
    fig, ax = plt.subplots(squeeze=True)
    fig.suptitle('Booo', x=0.5, y=1.1)
# Mutation info: Added squeeze = True (Call plt.subplots)