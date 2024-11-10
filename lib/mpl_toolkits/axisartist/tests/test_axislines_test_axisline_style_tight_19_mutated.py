import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from matplotlib.transforms import IdentityTransform
from mpl_toolkits.axisartist.axislines import AxesZero, SubplotZero, Subplot
from mpl_toolkits.axisartist import Axes, SubplotHost

def test_axisline_style_tight_19_mutated():
    fig = plt.figure(figsize=(2, 2))
    ax = fig.add_subplot(axes_class=AxesZero, projection='lambert')
    ax.axis['xzero'].set_axisline_style('-|>', size=5, facecolor='g')
    ax.axis['xzero'].set_visible(True)
    ax.axis['yzero'].set_axisline_style('->, size=8')
    ax.axis['yzero'].set_visible(True)
    for direction in ('left', 'right', 'bottom', 'top'):
        ax.axis[direction].set_visible(False)
    fig.tight_layout()