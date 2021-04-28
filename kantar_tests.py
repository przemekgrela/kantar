import datetime

import pytest

from kantar import (
    convert_dates_to_datetimes,
    get_endtime,
    get_duration,
    get_end_of_day,
    sort_sessions,
)


@pytest.mark.parametrize('sample_datetime, end_of_day', [
    (datetime.datetime(2020, 1, 1, 13, 0),
     datetime.datetime(2020, 1, 1, 23, 59, 59)),
    (datetime.datetime(2020, 1, 1, 22, 34),
     datetime.datetime(2020, 1, 1, 23, 59, 59)),
    (datetime.datetime(2020, 1, 1, 10, 22),
     datetime.datetime(2020, 1, 1, 23, 59, 59))
])
def test_get_end_of_day(sample_datetime, end_of_day):
    assert get_end_of_day(sample_datetime) == end_of_day


@pytest.mark.parametrize('sample_datetime, endtime', [
    (datetime.datetime(2020, 1, 1, 13, 0),
     datetime.datetime(2020, 1, 1, 12, 59, 59)),
    (datetime.datetime(2020, 1, 1, 22, 34),
     datetime.datetime(2020, 1, 1, 22, 33, 59)),
    (datetime.datetime(2020, 1, 1, 10, 22),
     datetime.datetime(2020, 1, 1, 10, 21, 59))
])
def test_get_endtime(sample_datetime, endtime):
    assert get_endtime(sample_datetime) == endtime


@pytest.mark.usefixtures('sessions')
def test_convert_dates(sessions):
    converted = convert_dates_to_datetimes(sessions)
    for i in converted:
        assert type(i['Starttime']) == datetime.datetime


@pytest.mark.usefixtures('sessions')
def test_sorting(sessions):
    assert sessions[0]['HomeNo'] != sessions[1]['HomeNo']
    converted = convert_dates_to_datetimes(sessions)
    sorted_sessions = sort_sessions(converted)
    assert sorted_sessions[0]['HomeNo'] == sorted_sessions[1]['HomeNo']
    assert sorted_sessions[0]['Starttime'] < sorted_sessions[1]['Starttime']


@pytest.mark.parametrize('start, end, duration', [
    (datetime.datetime(2020, 1, 1, 13, 0),
     datetime.datetime(2020, 1, 1, 13, 9, 59), 600),
    (datetime.datetime(2020, 1, 1, 11, 22, 22),
     datetime.datetime(2020, 1, 1, 11, 25, 8), 167),
])
def test_get_endtime(start, end, duration):
    assert get_duration(end, start) == duration


@pytest.fixture
def sessions():
    return [
        {'HomeNo': '1234', 'Channel': '101',
        'Starttime': '20200101180000', 'Activity': 'Live'},
        {'HomeNo': '45678', 'Channel': '104',
        'Starttime': '20200101193000', 'Activity': 'Live'},
        {'HomeNo': '1234', 'Channel': '102',
        'Starttime': '20200101183000', 'Activity': 'Live'},
        {'HomeNo': '45678', 'Channel': '103',
        'Starttime': '20200101190000', 'Activity': 'PlayBack'},
    ]
