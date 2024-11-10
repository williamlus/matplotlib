import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from matplotlib.transforms import IdentityTransform
from mpl_toolkits.axisartist.axislines import AxesZero, SubplotZero, Subplot
from mpl_toolkits.axisartist import Axes, SubplotHost

def test_subplotzero_ylabel_14_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(111, axes_class=SubplotZero, projection='lambert')
    ax.set(xlim=(-3, 7), ylim=(-3, 7), xlabel='x', ylabel='y')
    zero_axis = ax.axis['xzero', 'yzero']
    zero_axis.set_visible(True)
    ax.axis['left', 'right', 'bottom', 'top'].set_visible(False)
    zero_axis.set_axisline_style('->')