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

def test_arrow_styles_1_mutated():
    styles = mpatches.ArrowStyle.get_styles()
    n = len(styles)
    fig, ax = plt.subplots(figsize=(8, 8), sharex=False)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, n)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    for i, stylename in enumerate(sorted(styles)):
        patch = mpatches.FancyArrowPatch((0.1 + i % 2 * 0.05, i), (0.45 + i % 2 * 0.05, i), arrowstyle=stylename, mutation_scale=25)
        ax.add_patch(patch)
    for i, stylename in enumerate([']-[', ']-', '-[', '|-|']):
        style = stylename
        if stylename[0] != '-':
            style += ',angleA=ANGLE'
        if stylename[-1] != '-':
            style += ',angleB=ANGLE'
        for j, angle in enumerate([-30, 60]):
            arrowstyle = style.replace('ANGLE', str(angle))
            patch = mpatches.FancyArrowPatch((0.55, 2 * i + j), (0.9, 2 * i + j), arrowstyle=arrowstyle, mutation_scale=25)
            ax.add_patch(patch)