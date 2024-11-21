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

@image_comparison(['connection_styles.png'], style='mpl20', remove_text=True, tol=0.013 if platform.machine() == 'arm64' else 0)
def test_connection_styles_12_mutated():
    styles = mpatches.ConnectionStyle.get_styles()
    n = len(styles)
    fig, ax = plt.subplots(figsize=(6, 10))
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, n, auto=False)
    for i, stylename in enumerate(sorted(styles)):
        patch = mpatches.FancyArrowPatch((0.1, i), (0.8, i + 0.5), arrowstyle='->', connectionstyle=stylename, mutation_scale=25)
        ax.add_patch(patch)
# Mutation info: Added auto = False (Call ax.set_ylim)