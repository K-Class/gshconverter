from functools import partial
from pathlib import Path
from pandas import read_csv, Timestamp, Timedelta

from gshconverter import gregorian_to_solar_hijri, solar_hijri_to_gregorian


testdata = Path(__file__).parent / 'testdata'

df = read_csv(
    testdata / 'kabise.txt',
    sep=' ',
    comment='#',
    names=['shYear', 'gDate'],
    parse_dates=['gDate'],
)

df['leapType'] = (
    df['shYear'].str.contains(r'\d\*$') * 4
    + df['shYear'].str.contains(r'\d\*\*$') * 5
)

df['shYear'] = df['shYear'].str.rstrip('*').astype('uint16')


def test_solar_hijri_to_gregorian():
    converted = (
        df['shYear']
        .map(partial(solar_hijri_to_gregorian, sh_month=1, sh_day=1))
        .map(lambda x: Timestamp(*x))
    )
    assert (converted == df['gDate']).all()


def test_gregorian_to_solar_hijri():
    assert (
        df['gDate'].map(
            lambda x: gregorian_to_solar_hijri(x.year, x.month, x.day)
        )
        == df['shYear'].map(lambda y: (y, 1, 1))
    ).all()
