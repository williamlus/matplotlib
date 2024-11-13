import platform
import numpy as np
import matplotlib as mpl
from matplotlib.colors import same_color
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

def test_legend_bar_1_mutated():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x = np.arange(10)
    b1 = ax.bar(x, x, zdir='x', align='edge', color='m')
    b2 = ax.bar(x, x[::-1], zdir='x', align='edge', color='g')
    ax.legend([b1[0], b2[0]], ['up', 'down'])
# Mutation info: zdir = <ast.Constant object at 0x7fc056eb4ad0> -> zdir = x (Call ax.bar)