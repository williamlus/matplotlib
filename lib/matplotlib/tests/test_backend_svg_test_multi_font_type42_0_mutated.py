import datetime
from io import BytesIO
from pathlib import Path
import xml.etree.ElementTree
import xml.parsers.expat
import pytest
import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.text import Text
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
from matplotlib import font_manager as fm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def test_multi_font_type42_0_mutated():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    fig = plt.figure()
    plt.rc('svg', fonttype='none')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')