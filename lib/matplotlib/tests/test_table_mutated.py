import datetime
from unittest.mock import Mock
import numpy as np
import pytest
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.path import Path
from matplotlib.table import CustomCell, Table
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.transforms import Bbox
import matplotlib.units as munits
@image_comparison(['table_zorder.png'], remove_text=True)
def mutated_test_zorder():
    data = [[66386, 174296], [58230, 381139]]
    colLabels = ('Freeze', 'Wind')
    rowLabels = ['%d year' % x for x in (100, 50)]
    cellText = []
    yoff = np.zeros(len(colLabels))
    for row in reversed(data):
        yoff += row
        cellText.append(['%1.1f' % (x / 1000.0) for x in yoff])
    t = np.linspace(0, 2 * np.pi, 100)
    plt.plot(t, np.cos(t), lw=4, zorder=2)
    plt.table(cellText=cellText, rowLabels=rowLabels, colLabels=colLabels, loc='center', zorder=-2)
    plt.table(cellText=cellText, rowLabels=rowLabels, colLabels=colLabels, loc='upper center', zorder=4)
    plt.yticks([])
@image_comparison(['table_labels.png'])
def mutated_test_label_colours():
    dim = 3
    c = np.linspace(0, 1, dim)
    colours = plt.cm.RdYlGn(c)
    cellText = [['1'] * dim] * dim
    fig = plt.figure()
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.axis('off')
    ax1.table(cellText=cellText, rowColours=colours, loc='best')
    ax2 = fig.add_subplot(4, 1, 2)
    ax2.axis('off')
    ax2.table(cellText=cellText, rowColours=colours, rowLabels=['Header'] * dim, loc='best')
    ax3 = fig.add_subplot(4, 1, 3)
    ax3.axis('off')
    ax3.table(cellText=cellText, colColours=colours, loc='best')
    ax4 = fig.add_subplot(4, 1, 4)
    ax4.axis('off')
    ax4.table(cellText=cellText, colColours=colours, colLabels=['Header'] * dim, loc='best')
@image_comparison(['table_cell_manipulation.png'], remove_text=True)
def mutated_test_diff_cell_table():
    cells = ('horizontal', 'vertical', 'open', 'closed', 'T', 'R', 'B', 'L')
    cellText = [['1'] * len(cells)] * 2
    colWidths = [0.1] * len(cells)
    _, axs = plt.subplots(nrows=len(cells), figsize=(4, len(cells) + 1))
    for ax, cell in zip(axs, cells):
        ax.table(colWidths=colWidths, cellText=cellText, loc='center', edges=cell)
        ax.axis('off')
    plt.tight_layout()
@image_comparison(['table_auto_column.png'])
def mutated_test_auto_column():
    fig = plt.figure()
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.axis('off')
    tb1 = ax1.table(cellText=[['Fit Text', 2], ['very long long text, Longer text than default', 1]], rowLabels=['A', 'B'], colLabels=['Col1', 'Col2'], loc='center')
    tb1.auto_set_font_size(False)
    tb1.set_fontsize(12)
    tb1.auto_set_column_width([-1, 0, 1])
    ax2 = fig.add_subplot(4, 1, 2)
    ax2.axis('off')
    tb2 = ax2.table(cellText=[['Fit Text', 2], ['very long long text, Longer text than default', 1]], rowLabels=['A', 'B'], colLabels=['Col1', 'Col2'], loc='center')
    tb2.auto_set_font_size(False)
    tb2.set_fontsize(12)
    tb2.auto_set_column_width((-1, 0, 1))
    ax3 = fig.add_subplot(4, 1, 3)
    ax3.axis('off')
    tb3 = ax3.table(cellText=[['Fit Text', 2], ['very long long text, Longer text than default', 1]], rowLabels=['A', 'B'], colLabels=['Col1', 'Col2'], loc='center')
    tb3.auto_set_font_size(False)
    tb3.set_fontsize(12)
    tb3.auto_set_column_width(-1)
    tb3.auto_set_column_width(0)
    tb3.auto_set_column_width(1)
    ax4 = fig.add_subplot(4, 1, 4)
    ax4.axis('off')
    tb4 = ax4.table(cellText=[['Fit Text', 2], ['very long long text, Longer text than default', 1]], rowLabels=['A', 'B'], colLabels=['Col1', 'Col2'], loc='center')
    tb4.auto_set_font_size(False)
    tb4.set_fontsize(12)
    with pytest.warns(mpl.MatplotlibDeprecationWarning, match="'col' must be an int or sequence of ints"):
        tb4.auto_set_column_width('-101')
    with pytest.warns(mpl.MatplotlibDeprecationWarning, match="'col' must be an int or sequence of ints"):
        tb4.auto_set_column_width(['-101'])
