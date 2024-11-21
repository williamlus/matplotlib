import platform
import pytest
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['zoom_inset_connector_styles.png'], remove_text=True, style='mpl20', tol=0.024 if platform.machine() == 'arm64' else 0)
def test_zoom_inset_connector_styles_4_mutated():
    fig, axs = plt.subplots(2, squeeze=True)
    for ax in axs:
        ax.plot([1, 2, 3])
    axs[1].set_xlim(0.5, 1.5)
    indicator = axs[0].indicate_inset_zoom(axs[1], linewidth=5)
    indicator.connectors[1].set_linestyle('dashed')
    indicator.connectors[1].set_color('blue')
# Mutation info: Added squeeze = True (Call plt.subplots)