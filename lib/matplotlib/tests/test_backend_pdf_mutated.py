import datetime
import decimal
import io
import os
from pathlib import Path
import numpy as np
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt, rcParams, font_manager as fm
from matplotlib.cbook import _get_data_path
from matplotlib.ft2font import FT2Font
from matplotlib.font_manager import findfont, FontProperties
from matplotlib.backends._backend_pdf_ps import get_glyphs_subset
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
@image_comparison(['pdf_use14corefonts.pdf'])
def mutated_test_use14corefonts():
    rcParams['pdf.use14corefonts'] = True
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.size'] = 8
    rcParams['font.sans-serif'] = ['Helvetica']
    rcParams['pdf.compression'] = 0
    text = 'A three-line text positioned just above a blue line\nand containing some French characters and the euro symbol:\n"Merci pépé pour les 10 €"'
    fig, ax = plt.subplots()
    ax.set_title('Test PDF backend with option use14corefonts=True')
    ax.text(0.5, 0.5, text, horizontalalignment='center', verticalalignment='bottom', fontsize=14)
    ax.axhline(0.5, linewidth=0.5)
@image_comparison(['hatching_legend.pdf'])
def mutated_test_hatching_legend():
    """Test for correct hatching on patches in legend"""
    fig = plt.figure(figsize=(1, 2))
    a = Rectangle([0, 0], 0, 0, facecolor='green', hatch='XXXX')
    b = Rectangle([0, 0], 0, 0, facecolor='blue', hatch='XXXX')
    fig.legend([a, b, a, b], ['', '', '', ''])
@image_comparison(['grayscale_alpha.pdf'])
def mutated_test_grayscale_alpha():
    """Masking images with NaN did not work for grayscale images"""
    x, y = np.ogrid[-2:2:0.1, -2:2:0.1]
    dd = np.exp(-(x ** 2 + y ** 2))
    dd[dd < 0.1] = np.nan
    fig, ax = plt.subplots()
    ax.imshow(dd, interpolation='none', cmap='gray_r')
    ax.set_xticks([])
    ax.set_yticks([])
@image_comparison(['kerning.pdf'])
def mutated_test_kerning():
    fig = plt.figure()
    s = 'AVAVAVAVAVAVAVAV€AAVV'
    fig.text(0, 0.25, s, size=5)
    fig.text(0, 0.75, s, size=20)
@image_comparison(['multi_font_type3.pdf'], tol=4.6)
def mutated_test_multi_font_type3():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('pdf', fonttype=3)
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
@image_comparison(['multi_font_type42.pdf'], tol=2.2)
def mutated_test_multi_font_type42():
    fp = fm.FontProperties(family=['WenQuanYi Zen Hei'])
    if Path(fm.findfont(fp)).name != 'wqy-zenhei.ttc':
        pytest.skip('Font may be missing')
    plt.rc('font', family=['DejaVu Sans', 'WenQuanYi Zen Hei'], size=27)
    plt.rc('pdf', fonttype=42)
    fig = plt.figure()
    fig.text(0.15, 0.475, 'There are 几个汉字 in between!')
