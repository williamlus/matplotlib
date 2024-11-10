from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_tight_suptitle_non_default_4_mutated():
    fig, ax = plt.subplots(sharey=False)
    fig.suptitle('Booo', x=0.5, y=1.1)