from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter
@image_comparison(['bbox_inches_tight'], remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_bbox_inches_tight():
    data = [[66386, 174296, 75131, 577908, 32015], [58230, 381139, 78045, 99308, 160454], [89135, 80552, 152558, 497981, 603535], [78415, 81858, 150656, 193263, 69638], [139361, 331509, 343164, 781380, 52269]]
    col_labels = row_labels = [''] * 5
    rows = len(data)
    ind = np.arange(len(col_labels)) + 0.3
    cell_text = []
    width = 0.4
    yoff = np.zeros(len(col_labels))
    fig, ax = plt.subplots(1, 1)
    for row in range(rows):
        ax.bar(ind, data[row], width, bottom=yoff, align='edge', color='b')
        yoff = yoff + data[row]
        cell_text.append([''])
    plt.xticks([])
    plt.xlim(0, 5)
    plt.legend([''] * 5, loc=(1.2, 0.2))
    fig.legend([''] * 5, bbox_to_anchor=(0, 0.2), loc='lower left')
    cell_text.reverse()
    plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels, loc='bottom')
@image_comparison(['bbox_inches_tight_suptile_legend'], savefig_kwarg={'bbox_inches': 'tight'}, tol=0.02 if platform.machine() == 'arm64' else 0)
def mutated_test_bbox_inches_tight_suptile_legend():
    plt.plot(np.arange(10), label='a straight line')
    plt.legend(bbox_to_anchor=(0.9, 1), loc='upper left')
    plt.title('Axis title')
    plt.suptitle('Figure title')

    def y_formatter(y, pos):
        if int(y) == 4:
            return 'The number 4'
        else:
            return str(y)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))
    plt.xlabel('X axis')
@image_comparison(['bbox_inches_tight_suptile_non_default.png'], savefig_kwarg={'bbox_inches': 'tight'}, tol=0.1)
def mutated_test_bbox_inches_tight_suptitle_non_default():
    fig, ax = plt.subplots()
    fig.suptitle('Booo', x=0.5, y=1.1)
@image_comparison(['bbox_inches_tight_layout.png'], remove_text=True, style='mpl20', savefig_kwarg=dict(bbox_inches='tight', pad_inches='layout'))
def mutated_test_bbox_inches_tight_layout_constrained():
    fig, ax = plt.subplots(layout='constrained')
    fig.get_layout_engine().set(h_pad=0.5)
    ax.set_aspect('equal')
@image_comparison(['bbox_inches_tight_clipping'], remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_bbox_inches_tight_clipping():
    plt.scatter(np.arange(10), np.arange(10))
    ax = plt.gca()
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    patch = mpatches.Rectangle([-50, -50], 100, 100, transform=ax.transData, facecolor='blue', alpha=0.5)
    path = mpath.Path.unit_regular_star(5).deepcopy()
    path.vertices *= 0.25
    patch.set_clip_path(path, transform=ax.transAxes)
    plt.gcf().artists.append(patch)
@image_comparison(['bbox_inches_tight_raster'], remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_bbox_inches_tight_raster():
    """Test rasterization with tight_layout"""
    fig, ax = plt.subplots()
    ax.plot([1.0, 2.0], rasterized=True)
@image_comparison(['bbox_inches_fixed_aspect'], extensions=['png'], remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def mutated_test_bbox_inches_fixed_aspect():
    with plt.rc_context({'figure.constrained_layout.use': True}):
        fig, ax = plt.subplots()
        ax.plot([0, 1])
        ax.set_xlim(0, 1)
        ax.set_aspect('equal')
