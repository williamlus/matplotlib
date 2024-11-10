import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.backend_bases import RendererBase
from matplotlib.patheffects import PathEffectRenderer

def test_patheffect2_16_mutated():
    ax2 = plt.subplot(projection=None)
    arr = np.arange(25).reshape((5, 5))
    ax2.imshow(arr, interpolation='nearest')
    cntr = ax2.contour(arr, colors='k')
    cntr.set(path_effects=[path_effects.withStroke(linewidth=3, foreground='w')])
    clbls = ax2.clabel(cntr, fmt='%2.0f', use_clabeltext=True)
    plt.setp(clbls, path_effects=[path_effects.withStroke(linewidth=3, foreground='w')])