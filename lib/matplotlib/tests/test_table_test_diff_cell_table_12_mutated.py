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

@image_comparison(['table_cell_manipulation.png'], remove_text=True)
def test_diff_cell_table_12_mutated():
    cells = ('horizontal', 'vertical', 'open', 'closed', 'T', 'R', 'B', 'L')
    cellText = [['1'] * len(cells)] * 2
    colWidths = [0.1] * len(cells)
    _, axs = plt.subplots(nrows=len(cells), figsize=(4, len(cells) + 1))
    for ax, cell in zip(axs, cells):
        ax.table(colWidths=colWidths, cellText=cellText, loc='center', edges=cell, rowLoc='right')
        ax.axis('off')
    plt.tight_layout()
# Mutation info: Added rowLoc = right (Call ax.table)