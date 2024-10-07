from pathlib import Path
import matplotlib
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
@image_comparison(['truetype-conversion.pdf'])
def mutated_test_truetype_conversion(recwarn):
    matplotlib.rcParams['pdf.fonttype'] = 3
    fig, ax = plt.subplots()
    ax.text(0, 0, 'ABCDE', font=Path(__file__).with_name('mpltest.ttf'), fontsize=80)
    ax.set_xticks([])
    ax.set_yticks([])
