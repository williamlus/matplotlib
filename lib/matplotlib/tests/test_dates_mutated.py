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
@image_comparison(['date_axhspan.png'])
def mutated_test_date_axhspan():
    t0 = datetime.datetime(2009, 1, 20)
    tf = datetime.datetime(2009, 1, 21)
    fig, ax = plt.subplots()
    ax.axhspan(t0, tf, facecolor='blue', alpha=0.25)
    ax.set_ylim(t0 - datetime.timedelta(days=5), tf + datetime.timedelta(days=5))
    fig.subplots_adjust(left=0.25)
@image_comparison(['date_axvspan.png'])
def mutated_test_date_axvspan():
    t0 = datetime.datetime(2000, 1, 20)
    tf = datetime.datetime(2010, 1, 21)
    fig, ax = plt.subplots()
    ax.axvspan(t0, tf, facecolor='blue', alpha=0.25)
    ax.set_xlim(t0 - datetime.timedelta(days=720), tf + datetime.timedelta(days=720))
    fig.autofmt_xdate()
@image_comparison(['date_axhline.png'])
def mutated_test_date_axhline():
    t0 = datetime.datetime(2009, 1, 20)
    tf = datetime.datetime(2009, 1, 31)
    fig, ax = plt.subplots()
    ax.axhline(t0, color='blue', lw=3)
    ax.set_ylim(t0 - datetime.timedelta(days=5), tf + datetime.timedelta(days=5))
    fig.subplots_adjust(left=0.25)
@image_comparison(['date_axvline.png'])
def mutated_test_date_axvline():
    t0 = datetime.datetime(2000, 1, 20)
    tf = datetime.datetime(2000, 1, 21)
    fig, ax = plt.subplots()
    ax.axvline(t0, color='red', lw=3)
    ax.set_xlim(t0 - datetime.timedelta(days=5), tf + datetime.timedelta(days=5))
    fig.autofmt_xdate()
@image_comparison(['RRuleLocator_bounds.png'])
def mutated_test_RRuleLocator():
    import matplotlib.testing.jpl_units as units
    units.register()
    t0 = datetime.datetime(1000, 1, 1)
    tf = datetime.datetime(6000, 1, 1)
    fig = plt.figure()
    ax = plt.subplot()
    ax.set_autoscale_on(True)
    ax.plot([t0, tf], [0.0, 1.0], marker='o')
    rrule = mdates.rrulewrapper(dateutil.rrule.YEARLY, interval=500)
    locator = mdates.RRuleLocator(rrule)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    ax.autoscale_view()
    fig.autofmt_xdate()
@image_comparison(['DateFormatter_fractionalSeconds.png'])
def mutated_test_DateFormatter():
    import matplotlib.testing.jpl_units as units
    units.register()
    t0 = datetime.datetime(2001, 1, 1, 0, 0, 0)
    tf = datetime.datetime(2001, 1, 1, 0, 0, 1)
    fig = plt.figure()
    ax = plt.subplot()
    ax.set_autoscale_on(True)
    ax.plot([t0, tf], [0.0, 1.0], marker='o')
    ax.autoscale_view()
    fig.autofmt_xdate()
@image_comparison(['date_inverted_limit.png'])
def mutated_test_date_inverted_limit():
    t0 = datetime.datetime(2009, 1, 20)
    tf = datetime.datetime(2009, 1, 31)
    fig, ax = plt.subplots()
    ax.axhline(t0, color='blue', lw=3)
    ax.set_ylim(t0 - datetime.timedelta(days=5), tf + datetime.timedelta(days=5))
    ax.invert_yaxis()
    fig.subplots_adjust(left=0.25)
