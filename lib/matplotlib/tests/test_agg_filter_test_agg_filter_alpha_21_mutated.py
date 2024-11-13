import numpy as np
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison

def test_agg_filter_alpha_21_mutated():
    plt.rcParams['pcolormesh.snap'] = False
    ax = plt.axes()
    x, y = np.mgrid[0:7, 0:8]
    data = x ** 2 - y ** 2
    mesh = ax.pcolormesh(data, cmap='Reds', zorder=5, shading='flat')

    def manual_alpha(im, dpi):
        im[:, :, 3] *= 0.6
        print('CALLED')
        return (im, 0, 0)
    mesh.set_agg_filter(manual_alpha)
    mesh.set_rasterized(True)
    ax.plot([0, 4, 7], [1, 3, 8])
# Mutation info: Added shading = flat (Call ax.pcolormesh)