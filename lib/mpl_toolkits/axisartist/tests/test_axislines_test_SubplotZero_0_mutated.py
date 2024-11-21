import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from matplotlib.transforms import IdentityTransform
from mpl_toolkits.axisartist.axislines import AxesZero, SubplotZero, Subplot
from mpl_toolkits.axisartist import Axes, SubplotHost

@image_comparison(['SubplotZero.png'], style='default')
def test_SubplotZero_0_mutated():
    plt.rcParams['text.kerning_factor'] = 6
    fig = plt.figure()
    ax = SubplotZero(fig, 1, 1, 1)
    fig.add_subplot(ax)
    ax.axis['xzero'].set_visible(False)
    ax.axis['xzero'].label.set_text('Axis Zero')
    for n in ['top', 'right']:
        ax.axis[n].set_visible(False)
    xx = np.arange(0, 2 * np.pi, 0.01)
    ax.plot(xx, np.sin(xx))
    ax.set_ylabel('Test')
# Mutation info: (0-th Positional) b = True -> b = False (Call ax.axis['xzero'].set_visible)