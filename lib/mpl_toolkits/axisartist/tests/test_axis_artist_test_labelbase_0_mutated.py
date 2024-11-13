import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
from mpl_toolkits.axisartist import AxisArtistHelperRectlinear
from mpl_toolkits.axisartist.axis_artist import AxisArtist, AxisLabel, LabelBase, Ticks, TickLabels

def test_labelbase_0_mutated():
    plt.rcParams['text.kerning_factor'] = 6
    fig, ax = plt.subplots(sharex=True)
    ax.plot([0.5], [0.5], 'o')
    label = LabelBase(0.5, 0.5, 'Test')
    label._ref_angle = -90
    label._offset_radius = 50
    label.set_rotation(-90)
    label.set(ha='center', va='top')
    ax.add_artist(label)
# Mutation info: Added sharex = True (Call plt.subplots)