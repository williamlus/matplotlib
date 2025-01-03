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
_Params = namedtuple('_Params', 'wd_list, total, sep, expected')

@image_comparison(['paddedbox.png'], remove_text=True, style='mpl20')
def test_paddedbox_14_mutated():
    fig, ax = plt.subplots()
    ta = TextArea('foo')
    pb = PaddedBox(ta, pad=5, patch_attrs={'facecolor': 'r'}, draw_frame=True)
    ab = AnchoredOffsetbox('upper left', child=pb)
    ax.add_artist(ab)
    ta = TextArea('bar')
    pb = PaddedBox(ta, pad=10, patch_attrs={'facecolor': 'b'})
    ab = AnchoredOffsetbox('upper right', child=pb, frameon=False)
    ax.add_artist(ab)
    ta = TextArea('foobar')
    pb = PaddedBox(ta, pad=15, draw_frame=True)
    ab = AnchoredOffsetbox('lower right', child=pb)
    ax.add_artist(ab)
# Mutation info: Added frameon = False (Call AnchoredOffsetbox)