import platform
import pytest
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_zoom_inset_connector_styles_3_mutated():
    fig, axs = plt.subplots(2, squeeze=True)
    for ax in axs:
        ax.plot([1, 2, 3])
    axs[1].set_xlim(0.5, 1.5)
    indicator = axs[0].indicate_inset_zoom(axs[1], linewidth=5)
    indicator.connectors[1].set_linestyle('dashed')
    indicator.connectors[1].set_color('blue')