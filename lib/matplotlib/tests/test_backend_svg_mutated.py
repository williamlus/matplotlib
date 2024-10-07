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
@image_comparison(['fill_black_with_alpha.svg'], remove_text=True)
def mutated_test_fill_black_with_alpha():
    fig, ax = plt.subplots()
    ax.scatter(x=[0, 0.1, 1], y=[0, 0, 0], c='k', alpha=0.1, s=10000)
@image_comparison(['noscale'], remove_text=True)
def mutated_test_noscale():
    X, Y = np.meshgrid(np.arange(-5, 5, 1), np.arange(-5, 5, 1))
    Z = np.sin(Y ** 2)
    fig, ax = plt.subplots()
    ax.imshow(Z, cmap='gray', interpolation='none')
@image_comparison(['bold_font_output.svg'])
def mutated_test_bold_font_output():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10))
    ax.set_xlabel('nonbold-xlabel')
    ax.set_ylabel('bold-ylabel', fontweight='bold')
    ax.set_title('bold-title', fontweight='bold')
@image_comparison(['bold_font_output_with_none_fonttype.svg'])
def mutated_test_bold_font_output_with_none_fonttype():
    plt.rcParams['svg.fonttype'] = 'none'
    fig, ax = plt.subplots()
    ax.plot(np.arange(10), np.arange(10))
    ax.set_xlabel('nonbold-xlabel')
    ax.set_ylabel('bold-ylabel', fontweight='bold')
    ax.set_title('bold-title', fontweight='bold')
@image_comparison(['multi_font_aspath.svg'], tol=1.8)
def mutated_test_multi_font_type3():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('svg', fonttype='path')
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
@image_comparison(['multi_font_astext.svg'])
def mutated_test_multi_font_type42():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    fig = plt.figure()
    plt.rc('svg', fonttype='none')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
