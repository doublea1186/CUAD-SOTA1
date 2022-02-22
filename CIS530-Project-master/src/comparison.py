from number_processing import process_date, process_period
from pint import UnitRegistry
from regex_extraction import get_time
import math
from number_processing import *


def diff_dates(date_str1, date_str2):
    date1 = process_date(str(date_str1))
    date2 = process_date(str(date_str2))
    return diff_processed_dates(date1, date2)

def diff_processed_dates(date1, date2):
    if isinstance(date1, PartialDate) and isinstance(date2, PartialDate):
        if date1 == date2:
            return 0
    return 1

def is_same_date(date_str1, date_str2):
    date_difference = diff_dates(date_str1, date_str2)
    if date_difference == 0:
        return True
    return False

def is_same_processed_date(date1, date2):
    date_difference = diff_processed_dates(date1, date2)
    if date_difference == 0:
        return True
    return False

def diff_periods(period_str1, period_str2, standard_unit = "day"):
    # Assume each string only contains one period
    period1 = process_period(period_str1)
    period2 = process_period(period_str2)

    return diff_processed_periods(period1, period2, standard_unit)

def diff_processed_periods(period1, period2, standard_unit = "day"):
    if not type(period1) == tuple or not type(period1) == tuple:
        return 0

    time1, unit1 = period1
    time2, unit2 = period2
    # Both of the results are None
    if time1 is None and time2 is None:
        return 0
    elif time1 is None:
        return -1
    elif time2 is None:
        return -1

    ureg = UnitRegistry()

    period1 = time1 * ureg(unit1)
    period1 = period1.to(standard_unit)

    period2 = time2 * ureg(unit2)
    period2 = period2.to(standard_unit)

    # Percentage difference
    return float(2 * (period2 - period1) / (period1 + period2))

def is_same_period(period_str1, period_str2, standard_unit = "day", allowance=0.01):
    date_difference = diff_periods(period_str1, period_str2, standard_unit)
    if date_difference < allowance and not date_difference < 0:
        return True
    else:
        return False


def is_same_processed_period(period1, period2, standard_unit = "day", allowance=0.01):
    date_difference = diff_processed_periods(period1, period2, standard_unit)
    if date_difference < allowance and not date_difference < 0:
        return True
    else:
        return False
