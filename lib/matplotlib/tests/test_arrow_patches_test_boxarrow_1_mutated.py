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

@image_comparison(['boxarrow_test_image.png'])
def test_boxarrow_1_mutated():
    styles = mpatches.BoxStyle.get_styles()
    n = len(styles)
    spacing = 1.2
    figheight = n * spacing + 0.5
    fig = plt.figure(figsize=(4 / 1.5, figheight / 1.5), frameon=True)
    fontsize = 0.3 * 72
    for i, stylename in enumerate(sorted(styles)):
        fig.text(0.5, ((n - i) * spacing - 0.5) / figheight, stylename, ha='center', size=fontsize, transform=fig.transFigure, bbox=dict(boxstyle=stylename, fc='w', ec='k'))
# Mutation info: Added frameon = True (Call plt.figure)