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

@image_comparison(['anchoredtext_align.png'], remove_text=True, style='mpl20')
def test_anchoredtext_horizontal_alignment_4_mutated():
    fig, ax = plt.subplots(squeeze=False)
    text0 = AnchoredText('test\ntest long text', loc='center left', pad=0.2, prop={'ha': 'left'})
    ax.add_artist(text0)
    text1 = AnchoredText('test\ntest long text', loc='center', pad=0.2, prop={'ha': 'center'})
    ax.add_artist(text1)
    text2 = AnchoredText('test\ntest long text', loc='center right', pad=0.2, prop={'ha': 'right'})
    ax.add_artist(text2)
# Mutation info: Added squeeze = False (Call plt.subplots)