import platform
import numpy as np
import matplotlib as mpl
from matplotlib.colors import same_color
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

def test_legend_plot_1_mutated():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x = np.arange(10)
    ax.plot(x, 5 - x, 'o', zdir='z', label='z=1')
    ax.plot(x, x - 5, 'o', zdir='y', label='z=-1')
    ax.legend()
# Mutation info: zdir = <ast.Constant object at 0x7fc05658b350> -> zdir = z (Call ax.plot)