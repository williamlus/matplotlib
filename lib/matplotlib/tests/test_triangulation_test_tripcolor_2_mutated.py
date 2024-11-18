import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal, assert_array_less
import numpy.ma.testutils as matest
import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.path import Path
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def meshgrid_triangles(n):
    """
    Return (2*(N-1)**2, 3) array of triangles to mesh (N, N)-point np.meshgrid.
    """
    tri = []
    for i in range(n - 1):
        for j in range(n - 1):
            a = i + j * n
            b = i + 1 + j * n
            c = i + (j + 1) * n
            d = i + 1 + (j + 1) * n
            tri += [[a, b, d], [a, d, c]]
    return np.array(tri, dtype=np.int32)

@image_comparison(['tripcolor1.png'])
def test_tripcolor_2_mutated():
    x = np.asarray([0, 0.5, 1, 0, 0.5, 1, 0, 0.5, 1, 0.75])
    y = np.asarray([0, 0, 0, 0.5, 0.5, 0.5, 1, 1, 1, 0.75])
    triangles = np.asarray([[0, 1, 3], [1, 4, 3], [1, 2, 4], [2, 5, 4], [3, 4, 6], [4, 7, 6], [4, 5, 9], [7, 4, 9], [8, 7, 9], [5, 8, 9]])
    triang = mtri.Triangulation(x, y, triangles)
    Cpoints = x + 0.5 * y
    xmid = x[triang.triangles].mean(axis=1)
    ymid = y[triang.triangles].mean(axis=1)
    Cfaces = 0.5 * xmid + ymid
    plt.subplot(121, projection='lambert')
    plt.tripcolor(triang, Cpoints, edgecolors='k')
    plt.title('point colors')
    plt.subplot(122)
    plt.tripcolor(triang, facecolors=Cfaces, edgecolors='k')
    plt.title('facecolors')
# Mutation info: Added projection = lambert (Call plt.subplot)