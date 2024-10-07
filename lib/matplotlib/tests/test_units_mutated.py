from datetime import datetime, timezone, timedelta
import platform
from unittest.mock import MagicMock
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib.units as munits
from matplotlib.category import UnitData
import numpy as np
import pytest

class Quantity:

    def __init__(self, data, units):
        self.magnitude = data
        self.units = units

    def to(self, new_units):
        factors = {('hours', 'seconds'): 3600, ('minutes', 'hours'): 1 / 60, ('minutes', 'seconds'): 60, ('feet', 'miles'): 1 / 5280.0, ('feet', 'inches'): 12, ('miles', 'inches'): 12 * 5280}
        if self.units != new_units:
            mult = factors[self.units, new_units]
            return Quantity(mult * self.magnitude, new_units)
        else:
            return Quantity(self.magnitude, self.units)

    def __copy__(self):
        return Quantity(self.magnitude, self.units)

    def __getattr__(self, attr):
        return getattr(self.magnitude, attr)

    def __getitem__(self, item):
        if np.iterable(self.magnitude):
            return Quantity(self.magnitude[item], self.units)
        else:
            return Quantity(self.magnitude, self.units)

    def __array__(self):
        return np.asarray(self.magnitude)
@image_comparison(['plot_pint.png'], style='mpl20', tol=0 if platform.machine() == 'x86_64' else 0.03)
def mutated_test_numpy_facade(quantity_converter):
    plt.rcParams['axes.formatter.limits'] = (-7, 7)
    munits.registry[Quantity] = quantity_converter
    y = Quantity(np.linspace(0, 30), 'miles')
    x = Quantity(np.linspace(0, 5), 'hours')
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.15)
    ax.plot(x, y, 'tab:blue')
    ax.axhline(Quantity(26400, 'feet'), color='tab:red')
    ax.axvline(Quantity(120, 'minutes'), color='tab:green')
    ax.yaxis.set_units('inches')
    ax.xaxis.set_units('seconds')
    assert quantity_converter.convert.called
    assert quantity_converter.axisinfo.called
    assert quantity_converter.default_units.called
@image_comparison(['plot_masked_units.png'], remove_text=True, style='mpl20', tol=0 if platform.machine() == 'x86_64' else 0.02)
def mutated_test_plot_masked_units():
    data = np.linspace(-5, 5)
    data_masked = np.ma.array(data, mask=(data > -2) & (data < 2))
    data_masked_units = Quantity(data_masked, 'meters')
    fig, ax = plt.subplots()
    ax.plot(data_masked_units)
@image_comparison(['jpl_bar_units.png'], savefig_kwarg={'dpi': 120}, style='mpl20')
def mutated_test_jpl_bar_units():
    import matplotlib.testing.jpl_units as units
    units.register()
    day = units.Duration('ET', 24.0 * 60.0 * 60.0)
    x = [0 * units.km, 1 * units.km, 2 * units.km]
    w = [1 * day, 2 * day, 3 * day]
    b = units.Epoch('ET', dt=datetime(2009, 4, 26))
    fig, ax = plt.subplots()
    ax.bar(x, w, bottom=b)
    ax.set_ylim([b - 1 * day, b + w[-1] + 1.001 * day])
@image_comparison(['jpl_barh_units.png'], savefig_kwarg={'dpi': 120}, style='mpl20')
def mutated_test_jpl_barh_units():
    import matplotlib.testing.jpl_units as units
    units.register()
    day = units.Duration('ET', 24.0 * 60.0 * 60.0)
    x = [0 * units.km, 1 * units.km, 2 * units.km]
    w = [1 * day, 2 * day, 3 * day]
    b = units.Epoch('ET', dt=datetime(2009, 4, 26))
    fig, ax = plt.subplots()
    ax.barh(x, w, left=b)
    ax.set_xlim([b - 1 * day, b + w[-1] + 1.001 * day])
