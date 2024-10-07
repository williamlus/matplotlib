from datetime import datetime
import io
import warnings
import numpy as np
from numpy.testing import assert_almost_equal
from packaging.version import parse as parse_version
import pyparsing
import pytest
import matplotlib as mpl
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.transforms as mtransforms
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
from matplotlib.text import Text, Annotation, OffsetFrom
pyparsing_version = parse_version(pyparsing.__version__)
@image_comparison(['font_styles'])
def mutated_test_font_styles():

    def find_matplotlib_font(**kw):
        prop = FontProperties(**kw)
        path = findfont(prop, directory=mpl.get_data_path())
        return FontProperties(fname=path)
    from matplotlib.font_manager import FontProperties, findfont
    warnings.filterwarnings('ignore', "findfont: Font family \\[u?'Foo'\\] not found. Falling back to .", UserWarning, module='matplotlib.font_manager')
    fig, ax = plt.subplots()
    normal_font = find_matplotlib_font(family='sans-serif', style='normal', variant='normal', size=14)
    a = ax.annotate('Normal Font', (0.1, 0.1), xycoords='axes fraction', fontproperties=normal_font)
    assert a.get_fontname() == 'DejaVu Sans'
    assert a.get_fontstyle() == 'normal'
    assert a.get_fontvariant() == 'normal'
    assert a.get_weight() == 'normal'
    assert a.get_stretch() == 'normal'
    bold_font = find_matplotlib_font(family='Foo', style='normal', variant='normal', weight='bold', stretch=500, size=14)
    ax.annotate('Bold Font', (0.1, 0.2), xycoords='axes fraction', fontproperties=bold_font)
    bold_italic_font = find_matplotlib_font(family='sans serif', style='italic', variant='normal', weight=750, stretch=500, size=14)
    ax.annotate('Bold Italic Font', (0.1, 0.3), xycoords='axes fraction', fontproperties=bold_italic_font)
    light_font = find_matplotlib_font(family='sans-serif', style='normal', variant='normal', weight=200, stretch=500, size=14)
    ax.annotate('Light Font', (0.1, 0.4), xycoords='axes fraction', fontproperties=light_font)
    condensed_font = find_matplotlib_font(family='sans-serif', style='normal', variant='normal', weight=500, stretch=100, size=14)
    ax.annotate('Condensed Font', (0.1, 0.5), xycoords='axes fraction', fontproperties=condensed_font)
    ax.set_xticks([])
    ax.set_yticks([])
@image_comparison(['multiline'])
def mutated_test_multiline():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title('multiline\ntext alignment')
    plt.text(0.2, 0.5, 'TpTpTp\n$M$\nTpTpTp', size=20, ha='center', va='top')
    plt.text(0.5, 0.5, 'TpTpTp\n$M^{M^{M^{M}}}$\nTpTpTp', size=20, ha='center', va='top')
    plt.text(0.8, 0.5, 'TpTpTp\n$M_{q_{q_{q}}}$\nTpTpTp', size=20, ha='center', va='top')
    plt.xlim(0, 1)
    plt.ylim(0, 0.8)
    ax.set_xticks([])
    ax.set_yticks([])
@image_comparison(['multiline2'], style='mpl20')
def mutated_test_multiline2():
    plt.rcParams['text.kerning_factor'] = 6
    fig, ax = plt.subplots()
    ax.set_xlim([0, 1.4])
    ax.set_ylim([0, 2])
    ax.axhline(0.5, color='C2', linewidth=0.3)
    sts = ['Line', '2 Lineg\n 2 Lg', '$\\sum_i x $', 'hi $\\sum_i x $\ntest', 'test\n $\\sum_i x $', '$\\sum_i x $\n $\\sum_i x $']
    renderer = fig.canvas.get_renderer()

    def draw_box(ax, tt):
        r = mpatches.Rectangle((0, 0), 1, 1, clip_on=False, transform=ax.transAxes)
        r.set_bounds(tt.get_window_extent(renderer).transformed(ax.transAxes.inverted()).bounds)
        ax.add_patch(r)
    horal = 'left'
    for nn, st in enumerate(sts):
        tt = ax.text(0.2 * nn + 0.1, 0.5, st, horizontalalignment=horal, verticalalignment='bottom')
        draw_box(ax, tt)
    ax.text(1.2, 0.5, 'Bottom align', color='C2')
    ax.axhline(1.3, color='C2', linewidth=0.3)
    for nn, st in enumerate(sts):
        tt = ax.text(0.2 * nn + 0.1, 1.3, st, horizontalalignment=horal, verticalalignment='top')
        draw_box(ax, tt)
    ax.text(1.2, 1.3, 'Top align', color='C2')
    ax.axhline(1.8, color='C2', linewidth=0.3)
    for nn, st in enumerate(sts):
        tt = ax.text(0.2 * nn + 0.1, 1.8, st, horizontalalignment=horal, verticalalignment='baseline')
        draw_box(ax, tt)
    ax.text(1.2, 1.8, 'Baseline align', color='C2')
    ax.axhline(0.1, color='C2', linewidth=0.3)
    for nn, st in enumerate(sts):
        tt = ax.text(0.2 * nn + 0.1, 0.1, st, horizontalalignment=horal, verticalalignment='bottom', rotation=20)
        draw_box(ax, tt)
    ax.text(1.2, 0.1, 'Bot align, rot20', color='C2')
@image_comparison(['antialiased.png'], style='mpl20')
def mutated_test_antialiasing():
    mpl.rcParams['text.antialiased'] = False
    fig = plt.figure(figsize=(5.25, 0.75))
    fig.text(0.3, 0.75, 'antialiased', horizontalalignment='center', verticalalignment='center', antialiased=True)
    fig.text(0.3, 0.25, '$\\sqrt{x}$', horizontalalignment='center', verticalalignment='center', antialiased=True)
    mpl.rcParams['text.antialiased'] = True
    fig.text(0.7, 0.75, 'not antialiased', horizontalalignment='center', verticalalignment='center', antialiased=False)
    fig.text(0.7, 0.25, '$\\sqrt{x}$', horizontalalignment='center', verticalalignment='center', antialiased=False)
    mpl.rcParams['text.antialiased'] = False
@image_comparison(['text_contains.png'])
def mutated_test_contains():
    fig = plt.figure()
    ax = plt.axes()
    mevent = MouseEvent('button_press_event', fig.canvas, 0.5, 0.5, 1, None)
    xs = np.linspace(0.25, 0.75, 30)
    ys = np.linspace(0.25, 0.75, 30)
    xs, ys = np.meshgrid(xs, ys)
    txt = plt.text(0.5, 0.4, 'hello world', ha='center', fontsize=30, rotation=30)
    fig.canvas.draw()
    for x, y in zip(xs.flat, ys.flat):
        mevent.x, mevent.y = plt.gca().transAxes.transform([x, y])
        contains, _ = txt.contains(mevent)
        color = 'yellow' if contains else 'red'
        vl = ax.viewLim.frozen()
        ax.plot(x, y, 'o', color=color)
        ax.viewLim.set(vl)
@image_comparison(['titles'])
def mutated_test_titles():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title('left title', loc='left')
    ax.set_title('right title', loc='right')
    ax.set_xticks([])
    ax.set_yticks([])
@image_comparison(['text_alignment'], style='mpl20')
def mutated_test_alignment():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    x = 0.1
    for rotation in (0, 30):
        for alignment in ('top', 'bottom', 'baseline', 'center'):
            ax.text(x, 0.5, alignment + ' Tj', va=alignment, rotation=rotation, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            ax.text(x, 1.0, '$\\sum_{i=0}^{j}$', va=alignment, rotation=rotation)
            x += 0.1
    ax.plot([0, 1], [0.5, 0.5])
    ax.plot([0, 1], [1.0, 1.0])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
@image_comparison(['axes_titles.png'])
def mutated_test_axes_titles():
    plt.figure()
    ax = plt.subplot(1, 1, 1)
    ax.set_title('center', loc='center', fontsize=20, fontweight=700)
    ax.set_title('left', loc='left', fontsize=12, fontweight=400)
    ax.set_title('right', loc='right', fontsize=12, fontweight=400)
@image_comparison(['text_bboxclip'])
def mutated_test_bbox_clipping():
    plt.text(0.9, 0.2, 'Is bbox clipped?', backgroundcolor='r', clip_on=True)
    t = plt.text(0.9, 0.5, 'Is fancy bbox clipped?', clip_on=True)
    t.set_bbox({'boxstyle': 'round, pad=0.1'})
@image_comparison(['annotation_negative_ax_coords.png'])
def mutated_test_annotation_negative_ax_coords():
    fig, ax = plt.subplots()
    ax.annotate('+ pts', xytext=[30, 20], textcoords='axes points', xy=[30, 20], xycoords='axes points', fontsize=32)
    ax.annotate('- pts', xytext=[30, -20], textcoords='axes points', xy=[30, -20], xycoords='axes points', fontsize=32, va='top')
    ax.annotate('+ frac', xytext=[0.75, 0.05], textcoords='axes fraction', xy=[0.75, 0.05], xycoords='axes fraction', fontsize=32)
    ax.annotate('- frac', xytext=[0.75, -0.05], textcoords='axes fraction', xy=[0.75, -0.05], xycoords='axes fraction', fontsize=32, va='top')
    ax.annotate('+ pixels', xytext=[160, 25], textcoords='axes pixels', xy=[160, 25], xycoords='axes pixels', fontsize=32)
    ax.annotate('- pixels', xytext=[160, -25], textcoords='axes pixels', xy=[160, -25], xycoords='axes pixels', fontsize=32, va='top')
@image_comparison(['annotation_negative_fig_coords.png'])
def mutated_test_annotation_negative_fig_coords():
    fig, ax = plt.subplots()
    ax.annotate('+ pts', xytext=[10, 120], textcoords='figure points', xy=[10, 120], xycoords='figure points', fontsize=32)
    ax.annotate('- pts', xytext=[-10, 180], textcoords='figure points', xy=[-10, 180], xycoords='figure points', fontsize=32, va='top')
    ax.annotate('+ frac', xytext=[0.05, 0.55], textcoords='figure fraction', xy=[0.05, 0.55], xycoords='figure fraction', fontsize=32)
    ax.annotate('- frac', xytext=[-0.05, 0.5], textcoords='figure fraction', xy=[-0.05, 0.5], xycoords='figure fraction', fontsize=32, va='top')
    ax.annotate('+ pixels', xytext=[50, 50], textcoords='figure pixels', xy=[50, 50], xycoords='figure pixels', fontsize=32)
    ax.annotate('- pixels', xytext=[-50, 100], textcoords='figure pixels', xy=[-50, 100], xycoords='figure pixels', fontsize=32, va='top')
@image_comparison(['agg_text_clip.png'])
def mutated_test_agg_text_clip():
    np.random.seed(1)
    fig, (ax1, ax2) = plt.subplots(2)
    for x, y in np.random.rand(10, 2):
        ax1.text(x, y, 'foo', clip_on=True)
        ax2.text(x, y, 'foo')
@image_comparison(['font_scaling.pdf'])
def mutated_test_font_scaling():
    mpl.rcParams['pdf.fonttype'] = 42
    fig, ax = plt.subplots(figsize=(6.4, 12.4))
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.set_ylim(-10, 600)
    for i, fs in enumerate(range(4, 43, 2)):
        ax.text(0.1, i * 30, f'{fs} pt font size', fontsize=fs)
@image_comparison(['text_as_path_opacity.svg'])
def mutated_test_text_as_path_opacity():
    plt.figure()
    plt.gca().set_axis_off()
    plt.text(0.25, 0.25, 'c', color=(0, 0, 0, 0.5))
    plt.text(0.25, 0.5, 'a', alpha=0.5)
    plt.text(0.25, 0.75, 'x', alpha=0.5, color=(0, 0, 0, 1))
@image_comparison(['text_as_text_opacity.svg'])
def mutated_test_text_as_text_opacity():
    mpl.rcParams['svg.fonttype'] = 'none'
    plt.figure()
    plt.gca().set_axis_off()
    plt.text(0.25, 0.25, '50% using `color`', color=(0, 0, 0, 0.5))
    plt.text(0.25, 0.5, '50% using `alpha`', alpha=0.5)
    plt.text(0.25, 0.75, '50% using `alpha` and 100% `color`', alpha=0.5, color=(0, 0, 0, 1))
@image_comparison(['large_subscript_title.png'], style='mpl20')
def mutated_test_large_subscript_title():
    plt.rcParams['text.kerning_factor'] = 6
    plt.rcParams['axes.titley'] = None
    fig, axs = plt.subplots(1, 2, figsize=(9, 2.5), constrained_layout=True)
    ax = axs[0]
    ax.set_title('$\\sum_{i} x_i$')
    ax.set_title('New way', loc='left')
    ax.set_xticklabels([])
    ax = axs[1]
    ax.set_title('$\\sum_{i} x_i$', y=1.01)
    ax.set_title('Old Way', loc='left')
    ax.set_xticklabels([])
@image_comparison(['text_pdf_kerning.pdf'], style='mpl20')
def mutated_test_pdf_kerning():
    plt.figure()
    plt.figtext(0.1, 0.5, 'ATATATATATATATATATA', size=30)
@image_comparison(['text_pdf_font42_kerning.pdf'], style='mpl20')
def mutated_test_pdf_font42_kerning():
    plt.rcParams['pdf.fonttype'] = 42
    plt.figure()
    plt.figtext(0.1, 0.5, 'ATAVATAVATAVATAVATA', size=30)
@image_comparison(['text_pdf_chars_beyond_bmp.pdf'], style='mpl20')
def mutated_test_pdf_chars_beyond_bmp():
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['mathtext.fontset'] = 'stixsans'
    plt.figure()
    plt.figtext(0.1, 0.5, 'Mass $m$ 𐌈', size=30)
@image_comparison(baseline_images=['basictext_wrap'], extensions=['png'])
def mutated_test_basic_wrap():
    fig = plt.figure()
    plt.axis([0, 10, 0, 10])
    t = "This is a really long string that I'd rather have wrapped so that it doesn't go outside of the figure, but if it's long enough it will go off the top or bottom!"
    plt.text(4, 1, t, ha='left', rotation=15, wrap=True)
    plt.text(6, 5, t, ha='left', rotation=15, wrap=True)
    plt.text(5, 5, t, ha='right', rotation=-15, wrap=True)
    plt.text(5, 10, t, fontsize=18, style='oblique', ha='center', va='top', wrap=True)
    plt.text(3, 4, t, family='serif', style='italic', ha='right', wrap=True)
    plt.text(-1, 0, t, ha='left', rotation=-15, wrap=True)
@image_comparison(baseline_images=['fonttext_wrap'], extensions=['png'])
def mutated_test_font_wrap():
    fig = plt.figure()
    plt.axis([0, 10, 0, 10])
    t = "This is a really long string that I'd rather have wrapped so that it doesn't go outside of the figure, but if it's long enough it will go off the top or bottom!"
    plt.text(4, -1, t, fontsize=18, family='serif', ha='left', rotation=15, wrap=True)
    plt.text(6, 5, t, family='sans serif', ha='left', rotation=15, wrap=True)
    plt.text(5, 10, t, weight='heavy', ha='center', va='top', wrap=True)
    plt.text(3, 4, t, family='monospace', ha='right', wrap=True)
    plt.text(-1, 0, t, fontsize=14, style='italic', ha='left', rotation=-15, wrap=True)
