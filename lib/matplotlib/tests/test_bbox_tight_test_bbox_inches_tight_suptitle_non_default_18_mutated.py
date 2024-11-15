from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

def test_bbox_inches_tight_suptitle_non_default_18_mutated():
    fig, ax = plt.subplots()
    fig.suptitle('Booo', x=0.5, y=1.1, ha='left')
# Mutation info: Added ha = left (Call fig.suptitle)