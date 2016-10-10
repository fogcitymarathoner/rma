__author__ = 'marc'

from datetime import datetime as dt


def quarter_query_range(year, quarter):
    """
    returns start and end dates for a quarter (year, quarter number)
    :param year:
    :param quarter:
    :return:
    """
    year = int(year)
    if quarter == '0':
        begin = dt(year, 1, 1)
        end = dt(year, 3, 31)
    elif quarter == '1':
        begin = dt(year, 4, 1)
        end = dt(year, 6, 30)
    elif quarter == '2':
        begin = dt(year, 7, 1)
        end = dt(year, 9, 30)
    else:
        begin = dt(year, 10, 1)
        end = dt(year, 12, 31)
    return (begin, end)

def quarter_to_str(quarter):
    """
    given 0-3 return human nth term
    :param quarter:
    :return:
    """
    if quarter == '0':
        return '1st'
    elif quarter == '1':
        return '2nd'
    elif quarter == '2':
        return '3rd'
    else:
        return '4th'
