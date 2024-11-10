import platform
import numpy as np
import matplotlib as mpl
from matplotlib.colors import same_color
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

def test_fancy_0_mutated():
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ax.plot(np.arange(10), np.full(10, 5), np.full(10, 5), 'o--', label='line')
    ax.scatter(np.arange(10), np.arange(10, 0, -1), label='scatter')
    ax.errorbar(np.full(10, 5), np.arange(10), np.full(10, 10), xerr=0.5, zerr=0.5, label='errorbar')
    ax.legend(loc='lower left', ncols=2, title='My legend', numpoints=1)