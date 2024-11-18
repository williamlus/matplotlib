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

@image_comparison(['fancyarrow_test_image'], tol=0.012 if platform.machine() == 'arm64' else 0)
def test_fancyarrow_6_mutated():
    r = [0.4, 0.3, 0.2, 0.1, 0]
    t = ['fancy', 'simple', mpatches.ArrowStyle.Fancy()]
    fig, axs = plt.subplots(len(t), len(r), squeeze=False, figsize=(8, 4.5), subplot_kw=dict(aspect=1))
    for i_r, r1 in enumerate(r):
        for i_t, t1 in enumerate(t):
            ax = axs[i_t, i_r]
            draw_arrow(ax, t1, r1)
            ax.tick_params(labelleft=False, labelbottom=False, which='major')
# Mutation info: Added which = major (Call ax.tick_params)