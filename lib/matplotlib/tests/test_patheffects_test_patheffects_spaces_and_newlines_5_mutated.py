import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.backend_bases import RendererBase
from matplotlib.patheffects import PathEffectRenderer

@image_comparison(['spaces_and_newlines.png'], remove_text=True)
def test_patheffects_spaces_and_newlines_5_mutated():
    ax = plt.subplot(projection=None)
    s1 = '         '
    s2 = '\nNewline also causes problems'
    text1 = ax.text(0.5, 0.75, s1, ha='center', va='center', size=20, bbox={'color': 'salmon'})
    text2 = ax.text(0.5, 0.25, s2, ha='center', va='center', size=20, bbox={'color': 'thistle'})
    text1.set_path_effects([path_effects.Normal()])
    text2.set_path_effects([path_effects.Normal()])
# Mutation info: Added projection = None (Call plt.subplot)