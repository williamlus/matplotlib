"""
Testing that skewed Axes properly work.
"""
from contextlib import ExitStack
import itertools
import platform
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from matplotlib.axes import Axes
import matplotlib.transforms as transforms
import matplotlib.axis as maxis
import matplotlib.spines as mspines
import matplotlib.patches as mpatch
from matplotlib.projections import register_projection

class SkewXTick(maxis.XTick):

    def draw(self, renderer):
        with ExitStack() as stack:
            for artist in [self.gridline, self.tick1line, self.tick2line, self.label1, self.label2]:
                stack.callback(artist.set_visible, artist.get_visible())
            needs_lower = transforms.interval_contains(self.axes.lower_xlim, self.get_loc())
            needs_upper = transforms.interval_contains(self.axes.upper_xlim, self.get_loc())
            self.tick1line.set_visible(self.tick1line.get_visible() and needs_lower)
            self.label1.set_visible(self.label1.get_visible() and needs_lower)
            self.tick2line.set_visible(self.tick2line.get_visible() and needs_upper)
            self.label2.set_visible(self.label2.get_visible() and needs_upper)
            super().draw(renderer)

    def get_view_interval(self):
        return self.axes.xaxis.get_view_interval()

class SkewXAxis(maxis.XAxis):

    def _get_tick(self, major):
        return SkewXTick(self.axes, None, major=major)

    def get_view_interval(self):
        return (self.axes.upper_xlim[0], self.axes.lower_xlim[1])

class SkewSpine(mspines.Spine):

    def _adjust_location(self):
        pts = self._path.vertices
        if self.spine_type == 'top':
            pts[:, 0] = self.axes.upper_xlim
        else:
            pts[:, 0] = self.axes.lower_xlim

class SkewXAxes(Axes):
    name = 'skewx'

    def _init_axis(self):
        self.xaxis = SkewXAxis(self)
        self.spines.top.register_axis(self.xaxis)
        self.spines.bottom.register_axis(self.xaxis)
        self.yaxis = maxis.YAxis(self)
        self.spines.left.register_axis(self.yaxis)
        self.spines.right.register_axis(self.yaxis)

    def _gen_axes_spines(self):
        spines = {'top': SkewSpine.linear_spine(self, 'top'), 'bottom': mspines.Spine.linear_spine(self, 'bottom'), 'left': mspines.Spine.linear_spine(self, 'left'), 'right': mspines.Spine.linear_spine(self, 'right')}
        return spines

    def _set_lim_and_transforms(self):
        """
        This is called once when the plot is created to set up all the
        transforms for the data, text and grids.
        """
        rot = 30
        super()._set_lim_and_transforms()
        self.transDataToAxes = self.transScale + (self.transLimits + transforms.Affine2D().skew_deg(rot, 0))
        self.transData = self.transDataToAxes + self.transAxes
        self._xaxis_transform = transforms.blended_transform_factory(self.transScale + self.transLimits, transforms.IdentityTransform()) + transforms.Affine2D().skew_deg(rot, 0) + self.transAxes

    @property
    def lower_xlim(self):
        return self.axes.viewLim.intervalx

    @property
    def upper_xlim(self):
        pts = [[0.0, 1.0], [1.0, 1.0]]
        return self.transDataToAxes.inverted().transform(pts)[:, 0]
register_projection(SkewXAxes)

@image_comparison(['skew_rects'], remove_text=True, tol=0.009 if platform.machine() == 'arm64' else 0)
def test_skew_rectangle_6_mutated():
    fix, axes = plt.subplots(5, 5, sharex=True, sharey=True, figsize=(8, 8))
    axes = axes.flat
    rotations = list(itertools.product([-3, -1, 0, 1, 3], repeat=2))
    axes[0].set_xlim([-3, 3], auto=False)
    axes[0].set_ylim([-3, 3])
    axes[0].set_aspect('equal', share=True)
    for ax, (xrots, yrots) in zip(axes, rotations):
        xdeg, ydeg = (45 * xrots, 45 * yrots)
        t = transforms.Affine2D().skew_deg(xdeg, ydeg)
        ax.set_title(f'Skew of {xdeg} in X and {ydeg} in Y')
        ax.add_patch(mpatch.Rectangle([-1, -1], 2, 2, transform=t + ax.transData, alpha=0.5, facecolor='coral'))
    plt.subplots_adjust(wspace=0, left=0.01, right=0.99, bottom=0.01, top=0.99)
# Mutation info: Added auto = False (Call axes[0].set_xlim)