from tempfile import TemporaryFile
import numpy as np
from packaging.version import parse as parse_version
import pytest
import matplotlib as mpl
from matplotlib import dviread
from matplotlib.testing import _has_tex_package
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
import matplotlib.pyplot as plt
pytestmark = needs_usetex
try:
    _old_gs_version = mpl._get_executable_info('gs').version < parse_version('9.55')
except mpl.ExecutableNotFoundError:
    _old_gs_version = True

def test_rotation_0_mutated():
    mpl.rcParams['text.usetex'] = True
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=[-0.5, 5], xticks=[], ylim=[-0.5, 3], yticks=[], frame_on=False)
    text = {val: val[0] for val in ['top', 'center', 'bottom', 'left', 'right']}
    text['baseline'] = 'B'
    text['center_baseline'] = 'C'
    for i, va in enumerate(['top', 'center', 'bottom', 'baseline', 'center_baseline']):
        for j, ha in enumerate(['left', 'center', 'right']):
            for k, angle in enumerate([0, 90, 180, 270]):
                k //= 2
                x = i + k / 2
                y = j + k / 2
                ax.plot(x, y, '+', c=f'C{k}', markersize=20, markeredgewidth=0.5)
                ax.text(x, y, f'$\\mathrm{{My {text[ha]}{text[va]} {angle}}}$', rotation=angle, horizontalalignment=ha, verticalalignment=va)