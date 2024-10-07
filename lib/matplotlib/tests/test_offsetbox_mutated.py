from collections import namedtuple
import io
import numpy as np
from numpy.testing import assert_allclose
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.offsetbox import AnchoredOffsetbox, AnnotationBbox, AnchoredText, DrawingArea, HPacker, OffsetBox, OffsetImage, PaddedBox, TextArea, VPacker, _get_packed_offsets
@image_comparison(['offsetbox_clipping'], remove_text=True)
def mutated_test_offsetbox_clipping():
    fig, ax = plt.subplots()
    size = 100
    da = DrawingArea(size, size, clip=True)
    assert da.clip_children
    bg = mpatches.Rectangle((0, 0), size, size, facecolor='#CCCCCC', edgecolor='None', linewidth=0)
    line = mlines.Line2D([-size * 0.5, size * 1.5], [size / 2, size / 2], color='black', linewidth=10)
    anchored_box = AnchoredOffsetbox(loc='center', child=da, pad=0.0, frameon=False, bbox_to_anchor=(0.5, 0.5), bbox_transform=ax.transAxes, borderpad=0.0)
    da.add_artist(bg)
    da.add_artist(line)
    ax.add_artist(anchored_box)
    ax.set_xlim((0, 1))
    ax.set_ylim((0, 1))
@image_comparison(['anchoredtext_align.png'], remove_text=True, style='mpl20')
def mutated_test_anchoredtext_horizontal_alignment():
    fig, ax = plt.subplots()
    text0 = AnchoredText('test\ntest long text', loc='center left', pad=0.2, prop={'ha': 'left'})
    ax.add_artist(text0)
    text1 = AnchoredText('test\ntest long text', loc='center', pad=0.2, prop={'ha': 'center'})
    ax.add_artist(text1)
    text2 = AnchoredText('test\ntest long text', loc='center right', pad=0.2, prop={'ha': 'right'})
    ax.add_artist(text2)
@image_comparison(['paddedbox.png'], remove_text=True, style='mpl20')
def mutated_test_paddedbox():
    fig, ax = plt.subplots()
    ta = TextArea('foo')
    pb = PaddedBox(ta, pad=5, patch_attrs={'facecolor': 'r'}, draw_frame=True)
    ab = AnchoredOffsetbox('upper left', child=pb)
    ax.add_artist(ab)
    ta = TextArea('bar')
    pb = PaddedBox(ta, pad=10, patch_attrs={'facecolor': 'b'})
    ab = AnchoredOffsetbox('upper right', child=pb)
    ax.add_artist(ab)
    ta = TextArea('foobar')
    pb = PaddedBox(ta, pad=15, draw_frame=True)
    ab = AnchoredOffsetbox('lower right', child=pb)
    ax.add_artist(ab)
