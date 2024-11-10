import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

def test_spines_capstyle_6_mutated():
    plt.rc('axes', linewidth=20)
    fig, ax = plt.subplots()
    ax.set_xticks([], minor=True)
    ax.set_yticks([])