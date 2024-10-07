import copy
import numpy as np
from numpy.testing import assert_allclose, assert_almost_equal, assert_array_equal, assert_array_almost_equal
import pytest
from matplotlib import scale
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from matplotlib.transforms import Affine2D, Bbox, TransformedBbox
from matplotlib.path import Path
from matplotlib.testing.decorators import image_comparison, check_figures_equal

class TestAffine2D:
    single_point = [1.0, 1.0]
    multiple_points = [[0.0, 2.0], [3.0, 3.0], [4.0, 0.0]]
    pivot = single_point

    def test_init(self):
        Affine2D([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        Affine2D(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], int))
        Affine2D(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], float))

    def test_values(self):
        np.random.seed(19680801)
        values = np.random.random(6)
        assert_array_equal(Affine2D.from_values(*values).to_values(), values)

    def test_modify_inplace(self):
        trans = Affine2D()
        mtx = trans.get_matrix()
        mtx[0, 0] = 42
        assert_array_equal(trans.get_matrix(), [[42, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_clear(self):
        a = Affine2D(np.random.rand(3, 3) + 5)
        a.clear()
        assert_array_equal(a.get_matrix(), [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def test_rotate(self):
        r_pi_2 = Affine2D().rotate(np.pi / 2)
        r90 = Affine2D().rotate_deg(90)
        assert_array_equal(r_pi_2.get_matrix(), r90.get_matrix())
        assert_array_almost_equal(r90.transform(self.single_point), [-1, 1])
        assert_array_almost_equal(r90.transform(self.multiple_points), [[-2, 0], [-3, 3], [0, 4]])
        r_pi = Affine2D().rotate(np.pi)
        r180 = Affine2D().rotate_deg(180)
        assert_array_equal(r_pi.get_matrix(), r180.get_matrix())
        assert_array_almost_equal(r180.transform(self.single_point), [-1, -1])
        assert_array_almost_equal(r180.transform(self.multiple_points), [[0, -2], [-3, -3], [-4, 0]])
        r_pi_3_2 = Affine2D().rotate(3 * np.pi / 2)
        r270 = Affine2D().rotate_deg(270)
        assert_array_equal(r_pi_3_2.get_matrix(), r270.get_matrix())
        assert_array_almost_equal(r270.transform(self.single_point), [1, -1])
        assert_array_almost_equal(r270.transform(self.multiple_points), [[2, 0], [3, -3], [0, -4]])
        assert_array_equal((r90 + r90).get_matrix(), r180.get_matrix())
        assert_array_equal((r90 + r180).get_matrix(), r270.get_matrix())

    def test_rotate_around(self):
        r_pi_2 = Affine2D().rotate_around(*self.pivot, np.pi / 2)
        r90 = Affine2D().rotate_deg_around(*self.pivot, 90)
        assert_array_equal(r_pi_2.get_matrix(), r90.get_matrix())
        assert_array_almost_equal(r90.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r90.transform(self.multiple_points), [[0, 0], [-1, 3], [2, 4]])
        r_pi = Affine2D().rotate_around(*self.pivot, np.pi)
        r180 = Affine2D().rotate_deg_around(*self.pivot, 180)
        assert_array_equal(r_pi.get_matrix(), r180.get_matrix())
        assert_array_almost_equal(r180.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r180.transform(self.multiple_points), [[2, 0], [-1, -1], [-2, 2]])
        r_pi_3_2 = Affine2D().rotate_around(*self.pivot, 3 * np.pi / 2)
        r270 = Affine2D().rotate_deg_around(*self.pivot, 270)
        assert_array_equal(r_pi_3_2.get_matrix(), r270.get_matrix())
        assert_array_almost_equal(r270.transform(self.single_point), [1, 1])
        assert_array_almost_equal(r270.transform(self.multiple_points), [[2, 2], [3, -1], [0, -2]])
        assert_array_almost_equal((r90 + r90).get_matrix(), r180.get_matrix())
        assert_array_almost_equal((r90 + r180).get_matrix(), r270.get_matrix())

    def test_scale(self):
        sx = Affine2D().scale(3, 1)
        sy = Affine2D().scale(1, -2)
        trans = Affine2D().scale(3, -2)
        assert_array_equal((sx + sy).get_matrix(), trans.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [3, -2])
        assert_array_equal(trans.transform(self.multiple_points), [[0, -4], [9, -6], [12, 0]])

    def test_skew(self):
        trans_rad = Affine2D().skew(np.pi / 8, np.pi / 12)
        trans_deg = Affine2D().skew_deg(22.5, 15)
        assert_array_equal(trans_rad.get_matrix(), trans_deg.get_matrix())
        trans = Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_almost_equal(trans.transform(self.single_point), [1.5, 1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[1, 2], [4.5, 3.75], [4, 1]])

    def test_translate(self):
        tx = Affine2D().translate(23, 0)
        ty = Affine2D().translate(0, 42)
        trans = Affine2D().translate(23, 42)
        assert_array_equal((tx + ty).get_matrix(), trans.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [24, 43])
        assert_array_equal(trans.transform(self.multiple_points), [[23, 44], [26, 45], [27, 42]])

    def test_rotate_plus_other(self):
        trans = Affine2D().rotate_deg(90).rotate_deg_around(*self.pivot, 180)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().rotate_deg_around(*self.pivot, 180)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [3, 1])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[4, 2], [5, -1], [2, -2]])
        trans = Affine2D().rotate_deg(90).scale(3, -2)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-3, -2])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-6, -0], [-9, -6], [0, -8]])
        trans = Affine2D().rotate_deg(90).skew_deg(26.5650512, 14.0362435)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-0.5, 0.75])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-2, -0.5], [-1.5, 2.25], [2, 4]])
        trans = Affine2D().rotate_deg(90).translate(23, 42)
        trans_added = Affine2D().rotate_deg(90) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [22, 43])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[21, 42], [20, 45], [23, 46]])

    def test_rotate_around_plus_other(self):
        trans = Affine2D().rotate_deg_around(*self.pivot, 90).rotate_deg(180)
        trans_added = Affine2D().rotate_deg_around(*self.pivot, 90) + Affine2D().rotate_deg(180)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-1, -1])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[0, 0], [1, -3], [-2, -4]])
        trans = Affine2D().rotate_deg_around(*self.pivot, 90).scale(3, -2)
        trans_added = Affine2D().rotate_deg_around(*self.pivot, 90) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [3, -2])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[0, 0], [-3, -6], [6, -8]])
        trans = Affine2D().rotate_deg_around(*self.pivot, 90).skew_deg(26.5650512, 14.0362435)
        trans_added = Affine2D().rotate_deg_around(*self.pivot, 90) + Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [1.5, 1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[0, 0], [0.5, 2.75], [4, 4.5]])
        trans = Affine2D().rotate_deg_around(*self.pivot, 90).translate(23, 42)
        trans_added = Affine2D().rotate_deg_around(*self.pivot, 90) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [24, 43])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[23, 42], [22, 45], [25, 46]])

    def test_scale_plus_other(self):
        trans = Affine2D().scale(3, -2).rotate_deg(90)
        trans_added = Affine2D().scale(3, -2) + Affine2D().rotate_deg(90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [2, 3])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[4, 0], [6, 9], [0, 12]])
        trans = Affine2D().scale(3, -2).rotate_deg_around(*self.pivot, 90)
        trans_added = Affine2D().scale(3, -2) + Affine2D().rotate_deg_around(*self.pivot, 90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [4, 3])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[6, 0], [8, 9], [2, 12]])
        trans = Affine2D().scale(3, -2).skew_deg(26.5650512, 14.0362435)
        trans_added = Affine2D().scale(3, -2) + Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [2, -1.25])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-2, -4], [6, -3.75], [12, 3]])
        trans = Affine2D().scale(3, -2).translate(23, 42)
        trans_added = Affine2D().scale(3, -2) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_equal(trans.transform(self.single_point), [26, 40])
        assert_array_equal(trans.transform(self.multiple_points), [[23, 38], [32, 36], [35, 42]])

    def test_skew_plus_other(self):
        trans = Affine2D().skew_deg(26.5650512, 14.0362435).rotate_deg(90)
        trans_added = Affine2D().skew_deg(26.5650512, 14.0362435) + Affine2D().rotate_deg(90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-1.25, 1.5])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-2, 1], [-3.75, 4.5], [-1, 4]])
        trans = Affine2D().skew_deg(26.5650512, 14.0362435).rotate_deg_around(*self.pivot, 90)
        trans_added = Affine2D().skew_deg(26.5650512, 14.0362435) + Affine2D().rotate_deg_around(*self.pivot, 90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [0.75, 1.5])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[0, 1], [-1.75, 4.5], [1, 4]])
        trans = Affine2D().skew_deg(26.5650512, 14.0362435).scale(3, -2)
        trans_added = Affine2D().skew_deg(26.5650512, 14.0362435) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [4.5, -2.5])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[3, -4], [13.5, -7.5], [12, -2]])
        trans = Affine2D().skew_deg(26.5650512, 14.0362435).translate(23, 42)
        trans_added = Affine2D().skew_deg(26.5650512, 14.0362435) + Affine2D().translate(23, 42)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [24.5, 43.25])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[24, 44], [27.5, 45.75], [27, 43]])

    def test_translate_plus_other(self):
        trans = Affine2D().translate(23, 42).rotate_deg(90)
        trans_added = Affine2D().translate(23, 42) + Affine2D().rotate_deg(90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-43, 24])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-44, 23], [-45, 26], [-42, 27]])
        trans = Affine2D().translate(23, 42).rotate_deg_around(*self.pivot, 90)
        trans_added = Affine2D().translate(23, 42) + Affine2D().rotate_deg_around(*self.pivot, 90)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [-41, 24])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[-42, 23], [-43, 26], [-40, 27]])
        trans = Affine2D().translate(23, 42).scale(3, -2)
        trans_added = Affine2D().translate(23, 42) + Affine2D().scale(3, -2)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [72, -86])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[69, -88], [78, -90], [81, -84]])
        trans = Affine2D().translate(23, 42).skew_deg(26.5650512, 14.0362435)
        trans_added = Affine2D().translate(23, 42) + Affine2D().skew_deg(26.5650512, 14.0362435)
        assert_array_equal(trans.get_matrix(), trans_added.get_matrix())
        assert_array_almost_equal(trans.transform(self.single_point), [45.5, 49])
        assert_array_almost_equal(trans.transform(self.multiple_points), [[45, 49.75], [48.5, 51.5], [48, 48.75]])

    def test_invalid_transform(self):
        t = mtransforms.Affine2D()
        with pytest.raises(ValueError):
            t.transform(1)
        with pytest.raises(ValueError):
            t.transform([[[1]]])
        with pytest.raises(RuntimeError):
            t.transform([])
        with pytest.raises(RuntimeError):
            t.transform([1])
        with pytest.raises(ValueError):
            t.transform([[1]])
        with pytest.raises(ValueError):
            t.transform([[1, 2, 3]])

    def test_copy(self):
        a = mtransforms.Affine2D()
        b = mtransforms.Affine2D()
        s = a + b
        s.get_matrix()
        s1 = copy.copy(s)
        assert not s._invalid and (not s1._invalid)
        a.translate(1, 2)
        assert s._invalid and s1._invalid
        assert (s1.get_matrix() == a.get_matrix()).all()
        s.get_matrix()
        b1 = copy.copy(b)
        b1.translate(3, 4)
        assert not s._invalid
        assert_array_equal(s.get_matrix(), a.get_matrix())

    def test_deepcopy(self):
        a = mtransforms.Affine2D()
        b = mtransforms.Affine2D()
        s = a + b
        s.get_matrix()
        s1 = copy.deepcopy(s)
        assert not s._invalid and (not s1._invalid)
        a.translate(1, 2)
        assert s._invalid and (not s1._invalid)
        assert_array_equal(s1.get_matrix(), mtransforms.Affine2D().get_matrix())
        s.get_matrix()
        b1 = copy.deepcopy(b)
        b1.translate(3, 4)
        assert not s._invalid
        assert_array_equal(s.get_matrix(), a.get_matrix())

class TestAffineDeltaTransform:

    def test_invalidate(self):
        before = np.array([[1.0, 4.0, 0.0], [5.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        after = np.array([[1.0, 3.0, 0.0], [5.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        base = mtransforms.Affine2D.from_values(1, 5, 4, 1, 2, 3)
        t = mtransforms.AffineDeltaTransform(base)
        assert_array_equal(t.get_matrix(), before)
        base.get_matrix()[0, 1:] = 3
        assert_array_equal(t.get_matrix(), after)
        base.invalidate()
        assert_array_equal(t.get_matrix(), after)
@image_comparison(['pre_transform_data'], remove_text=True, style='mpl20', tol=0.05)
def mutated_test_pre_transform_plotting():
    ax = plt.axes()
    times10 = mtransforms.Affine2D().scale(10)
    ax.contourf(np.arange(48).reshape(6, 8), transform=times10 + ax.transData)
    ax.pcolormesh(np.linspace(0, 4, 7), np.linspace(5.5, 8, 9), np.arange(48).reshape(8, 6), transform=times10 + ax.transData)
    ax.scatter(np.linspace(0, 10), np.linspace(10, 0), transform=times10 + ax.transData)
    x = np.linspace(8, 10, 20)
    y = np.linspace(1, 5, 20)
    u = 2 * np.sin(x) + np.cos(y[:, np.newaxis])
    v = np.sin(x) - np.cos(y[:, np.newaxis])
    ax.streamplot(x, y, u, v, transform=times10 + ax.transData, linewidth=np.hypot(u, v))
    x, y = (x[::3], y[::3])
    u, v = (u[::3, ::3], v[::3, ::3])
    ax.quiver(x, y + 5, u, v, transform=times10 + ax.transData)
    ax.barbs(x - 3, y + 5, u ** 2, v ** 2, transform=times10 + ax.transData)
