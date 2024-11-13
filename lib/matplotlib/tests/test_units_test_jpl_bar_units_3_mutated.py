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

@pytest.fixture
def quantity_converter():
    qc = munits.ConversionInterface()

    def convert(value, unit, axis):
        if hasattr(value, 'units'):
            return value.to(unit).magnitude
        elif np.iterable(value):
            try:
                return [v.to(unit).magnitude for v in value]
            except AttributeError:
                return [Quantity(v, axis.get_units()).to(unit).magnitude for v in value]
        else:
            return Quantity(value, axis.get_units()).to(unit).magnitude

    def default_units(value, axis):
        if hasattr(value, 'units'):
            return value.units
        elif np.iterable(value):
            for v in value:
                if hasattr(v, 'units'):
                    return v.units
            return None
    qc.convert = MagicMock(side_effect=convert)
    qc.axisinfo = MagicMock(side_effect=lambda u, a: munits.AxisInfo(label=u, default_limits=(0, 100)))
    qc.default_units = MagicMock(side_effect=default_units)
    return qc

class Kernel:

    def __init__(self, array):
        self._array = np.asanyarray(array)

    def __array__(self, dtype=None, copy=None):
        if dtype is not None and dtype != self._array.dtype:
            if copy is not None and (not copy):
                raise ValueError(f'Converting array from {self._array.dtype} to {dtype} requires a copy')
        arr = np.asarray(self._array, dtype=dtype)
        return arr if not copy else np.copy(arr)

    @property
    def shape(self):
        return self._array.shape

def test_jpl_bar_units_3_mutated():
    import matplotlib.testing.jpl_units as units
    units.register()
    day = units.Duration('ET', 24.0 * 60.0 * 60.0)
    x = [0 * units.km, 1 * units.km, 2 * units.km]
    w = [1 * day, 2 * day, 3 * day]
    b = units.Epoch('ET', dt=datetime(2009, 4, 26))
    fig, ax = plt.subplots(squeeze=True)
    ax.bar(x, w, bottom=b)
    ax.set_ylim([b - 1 * day, b + w[-1] + 1.001 * day])
# Mutation info: Added squeeze = True (Call plt.subplots)