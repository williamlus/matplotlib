import datetime
import dateutil.tz
import dateutil.rrule
import functools
import numpy as np
import pytest
from matplotlib import rc_context, style
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
import matplotlib.ticker as mticker

def _new_epoch_decorator(thefunc):

    @functools.wraps(thefunc)
    def wrapper():
        mdates._reset_epoch_test_example()
        mdates.set_epoch('2000-01-01')
        thefunc()
        mdates._reset_epoch_test_example()
    return wrapper

def _test_date2num_dst(date_range, tz_convert):
    BRUSSELS = dateutil.tz.gettz('Europe/Brussels')
    UTC = mdates.UTC
    dtstart = datetime.datetime(2014, 3, 30, 0, 0, tzinfo=UTC)
    interval = datetime.timedelta(minutes=33, seconds=45)
    interval_days = interval.seconds / 86400
    N = 8
    dt_utc = date_range(start=dtstart, freq=interval, periods=N)
    dt_bxl = tz_convert(dt_utc, BRUSSELS)
    t0 = 735322.0 + mdates.date2num(np.datetime64('0000-12-31'))
    expected_ordinalf = [t0 + i * interval_days for i in range(N)]
    actual_ordinalf = list(mdates.date2num(dt_bxl))
    assert actual_ordinalf == expected_ordinalf

def _test_rrulewrapper(attach_tz, get_tz):
    SYD = get_tz('Australia/Sydney')
    dtstart = attach_tz(datetime.datetime(2017, 4, 1, 0), SYD)
    dtend = attach_tz(datetime.datetime(2017, 4, 4, 0), SYD)
    rule = mdates.rrulewrapper(freq=dateutil.rrule.DAILY, dtstart=dtstart)
    act = rule.between(dtstart, dtend)
    exp = [datetime.datetime(2017, 4, 1, 13, tzinfo=dateutil.tz.tzutc()), datetime.datetime(2017, 4, 2, 14, tzinfo=dateutil.tz.tzutc())]
    assert act == exp

@image_comparison(['DateFormatter_fractionalSeconds.png'])
def test_DateFormatter_1_mutated():
    import matplotlib.testing.jpl_units as units
    units.register()
    t0 = datetime.datetime(2001, 1, 1, 0, 0, 0)
    tf = datetime.datetime(2001, 1, 1, 0, 0, 1)
    fig = plt.figure(clear=False)
    ax = plt.subplot()
    ax.set_autoscale_on(True)
    ax.plot([t0, tf], [0.0, 1.0], marker='o')
    ax.autoscale_view()
    fig.autofmt_xdate()
# Mutation info: Added clear = False (Call plt.figure)