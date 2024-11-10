import base64
import io
import platform
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path

def test_fft_peaks_1_mutated():
    fig, ax = plt.subplots(sharey=False)
    t = np.arange(65536)
    p1 = ax.plot(abs(np.fft.fft(np.sin(2 * np.pi * 0.01 * t) * np.blackman(len(t)))))
    fig.canvas.draw()
    path = p1[0].get_path()
    transform = p1[0].get_transform()
    path = transform.transform_path(path)
    simplified = path.cleaned(simplify=True)
    assert simplified.vertices.size == 36