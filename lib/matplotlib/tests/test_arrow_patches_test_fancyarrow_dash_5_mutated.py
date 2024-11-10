import pytest
import platform
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
import matplotlib.patches as mpatches

def draw_arrow(ax, t, r):
    ax.annotate('', xy=(0.5, 0.5 + r), xytext=(0.5, 0.5), size=30, arrowprops=dict(arrowstyle=t, fc='b', ec='k'))

def __prepare_fancyarrow_dpi_cor_test():
    """
    Convenience function that prepares and returns a FancyArrowPatch. It aims
    at being used to test that the size of the arrow head does not depend on
    the DPI value of the exported picture.

    NB: this function *is not* a test in itself!
    """
    fig2 = plt.figure('fancyarrow_dpi_cor_test', figsize=(4, 3), dpi=50)
    ax = fig2.add_subplot()
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.add_patch(mpatches.FancyArrowPatch(posA=(0.3, 0.4), posB=(0.8, 0.6), lw=3, arrowstyle='->', mutation_scale=100))
    return fig2

def test_fancyarrow_dash_5_mutated():
    fig, ax = plt.subplots(sharey=True)
    e = mpatches.FancyArrowPatch((0, 0), (0.5, 0.5), arrowstyle='-|>', connectionstyle='angle3,angleA=0,angleB=90', mutation_scale=10.0, linewidth=2, linestyle='dashed', color='k')
    e2 = mpatches.FancyArrowPatch((0, 0), (0.5, 0.5), arrowstyle='-|>', connectionstyle='angle3', mutation_scale=10.0, linewidth=2, linestyle='dotted', color='k')
    ax.add_patch(e)
    ax.add_patch(e2)