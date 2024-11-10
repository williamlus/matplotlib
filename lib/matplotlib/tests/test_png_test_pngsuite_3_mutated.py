from io import BytesIO
from pathlib import Path
import pytest
from matplotlib.testing.decorators import image_comparison
from matplotlib import cm, pyplot as plt

def test_pngsuite_3_mutated():
    files = sorted((Path(__file__).parent / 'baseline_images/pngsuite').glob('basn*.png'))
    plt.figure(figsize=(len(files), 2))
    for i, fname in enumerate(files):
        data = plt.imread(fname)
        cmap = None
        if data.ndim == 2:
            cmap = cm.gray
        plt.imshow(data, extent=(i, i + 1, 0, 1), cmap=cmap, interpolation_stage='data', aspect='auto')
    plt.gca().patch.set_facecolor('#ddffff')
    plt.gca().set_xlim(0, len(files))