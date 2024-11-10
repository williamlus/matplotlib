from tempfile import TemporaryFile
import numpy as np
from packaging.version import parse as parse_version
import pytest
import matplotlib as mpl
from matplotlib import dviread
from matplotlib.testing import _has_tex_package
from matplotlib.testing.decorators import check_figures_equal, image_comparison
from matplotlib.testing._markers import needs_usetex
import matplotlib.pyplot as plt
pytestmark = needs_usetex
try:
    _old_gs_version = mpl._get_executable_info('gs').version < parse_version('9.55')
except mpl.ExecutableNotFoundError:
    _old_gs_version = True

def test_multiline_eqnarray_0_mutated():
    text = '\\begin{eqnarray*}foo\\\\bar\\\\baz\\\\\\end{eqnarray*}'
    fig = plt.figure(figsize=(1, 1))
    fig.text(0.5, 0.5, text, usetex=True, horizontalalignment='center', verticalalignment='center')