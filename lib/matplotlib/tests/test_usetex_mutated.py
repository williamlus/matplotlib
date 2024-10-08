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
@image_comparison(baseline_images=['test_usetex'], extensions=['pdf', 'png'], style='mpl20')
def mutated_test_usetex():
    mpl.rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    kwargs = {'verticalalignment': 'baseline', 'size': 24, 'bbox': dict(pad=0, edgecolor='k', facecolor='none')}
    ax.text(0.2, 0.7, '\\LaTeX\\ $\\left[\\int\\limits_e^{2e}\\sqrt\\frac{\\log^3 x}{x}\\,\\mathrm{d}x \\right\\}$', **kwargs)
    ax.text(0.2, 0.3, 'lg', **kwargs)
    ax.text(0.4, 0.3, '$\\frac{1}{2}\\pi$', **kwargs)
    ax.text(0.6, 0.3, '$p^{3^A}$', **kwargs)
    ax.text(0.8, 0.3, '$p_{3_2}$', **kwargs)
    for x in {t.get_position()[0] for t in ax.texts}:
        ax.axvline(x)
    for y in {t.get_position()[1] for t in ax.texts}:
        ax.axhline(y)
    ax.set_axis_off()
@image_comparison(['eqnarray.png'])
def mutated_test_multiline_eqnarray():
    text = '\\begin{eqnarray*}foo\\\\bar\\\\baz\\\\\\end{eqnarray*}'
    fig = plt.figure(figsize=(1, 1))
    fig.text(0.5, 0.5, text, usetex=True, horizontalalignment='center', verticalalignment='center')
@image_comparison(baseline_images=['rotation'], extensions=['eps', 'pdf', 'png', 'svg'], style='mpl20', tol=3.91 if _old_gs_version else 0)
def mutated_test_rotation():
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
