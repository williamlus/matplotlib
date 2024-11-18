from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

@image_comparison(['bbox_inches_tight_suptile_legend'], savefig_kwarg={'bbox_inches': 'tight'}, tol=0.02 if platform.machine() == 'arm64' else 0)
def test_bbox_inches_tight_suptile_legend_8_mutated():
    plt.plot(np.arange(10), label='a straight line')
    plt.legend(bbox_to_anchor=(0.9, 1), loc='upper left')
    plt.title('Axis title')
    plt.suptitle('Figure title', va='center')

    def y_formatter(y, pos):
        if int(y) == 4:
            return 'The number 4'
        else:
            return str(y)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(y_formatter))
    plt.xlabel('X axis')
# Mutation info: Added va = center (Call plt.suptitle)