import re
import dateparser
from regex_extraction import get_time
from constants import nlp, date_normalization_kw

class PartialDate():

    def __init__(self, year, month, day):
        if type(year) == str and "[]" in year:
            year_len = len(year.replace('[]', ''))
            zero_ct = 4 - year_len
            zeros = '0' * zero_ct
            year = year.replace('[]', zeros)

        if type(year) == str and '' == year:
            year = -1
        if type(month) == str and '' == month:
            month = -1
        if type(day) == str and '' == day:
            day = -1

        if type(year) == str:
            year = int(year)
            if year > 0 and year < 30:
                year = 2000 + year
            elif year >= 30 and year < 100:
                year = 1900 + year
        if type(month) == str:
            month = int(month)
        if type(day) == str:
            day = int(day)

        self.year = year
        self.month = month
        self.day = day

    def is_date(self):
        if self.day is None and self.month is None and self.day is None:
            return False
        return True

    def to_num_tuple(self):
        if self.month is None:
            t0 = -1
        else:
            t0 = self.month

        if self.day is None:
            t1 = -1
        else:
            t1 = self.day

        if self.year is None:
            t2 = -1
        else:
            t2 = self.year

        return (t0, t1, t2)

    def __str__(self) -> str:
        if self.month is None:
            t0 = '[]'
        else:
            t0 = self.month

        if self.day is None:
            t1 = '[]'
        else:
            t1 = self.day

        if self.year is None:
            t2 = '[]'
        else:
            t2 = self.year


        return f"{t0}/{t1}/{t2}"

    def __eq__(self, other):
        if self.is_date() and other.is_date():
            self_tuple = self.to_num_tuple()
            other_tuple = other.to_num_tuple()
            return self_tuple == other_tuple
        else:
            return False

def process_date(date_string):

    # date_string = date_string.replace("this ", '')
    # date_string = date_string.replace("the ", '')
    # date_string = date_string.replace("day of ", '')
    # date_string = date_string.replace("month of ", '')

    orig_day_date = dateparser.parse(date_string, settings={'REQUIRE_PARTS': ['day']})
    orig_month_date = dateparser.parse(date_string, settings={'REQUIRE_PARTS': ['month']})
    orig_year_date = dateparser.parse(date_string, settings={'REQUIRE_PARTS': ['year']})

    day_digit = None
    month_digit = None
    year_digit = None

    if orig_day_date is not None:
        day_digit = orig_day_date.day
    if orig_month_date is not None:
        month_digit = orig_month_date.month
    if orig_year_date is not None:
        year_digit = orig_year_date.year

    # Full string is not a valid date, check whether a substring works
    if orig_day_date is None and orig_month_date is None and orig_year_date is None:
        tokenized_string = nlp(date_string.lower())
        new_str = []

        for t in tokenized_string:
            if not str(t) in date_normalization_kw:
                continue
            else:
                new_str.append(str(t))
        new_str = ' '.join(new_str)

        new_day_date = dateparser.parse(new_str, settings={'REQUIRE_PARTS': ['day']})
        new_month_date = dateparser.parse(new_str, settings={'REQUIRE_PARTS': ['month']})
        new_year_date = dateparser.parse(new_str, settings={'REQUIRE_PARTS': ['year']})

        if new_day_date is not None:
            day_digit = new_day_date.day
        if new_month_date is not None:
            month_digit = new_month_date.month
        if new_year_date is not None:
            year_digit = new_year_date.year

    date = PartialDate(year_digit, month_digit, day_digit)
    return date

def process_period(period_string):
    time = get_time(period_string)

    if len(time) == 0:
        return None, None
    if len(time) > 1:
        # Not sure how to process this period
        return None, None

    unit = list(time.keys())[0]
    time = time[unit][0]

    return time, unit

def time_to_dict(time_string):

    # default value
    time_dict = {'date': {'month':-1, 'day':-1, 'year':-1},
                 'period': {'month':-1, 'day':-1, 'year':-1}}

    # the string is a date:
    date = process_date(time_string)
    month = date.month
    day = date.day
    year = date.year

    if month is not None:
        time_dict['date']['month'] = month
    if day is not None:
        time_dict['date']['day'] = day
    if year is not None:
        time_dict['date']['year'] = year

    # The string is a period
    time, unit = process_period(time_string)

    if unit is not None:
        time_dict['period'][unit] = time

    return time_dict

if __name__ == "__main__":
    s = 'last day in February, 2023'
    res = process_date(s)
