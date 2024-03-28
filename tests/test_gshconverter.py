from datetime import datetime, timedelta
from timeit import timeit

from jdatetime import GregorianToJalali, JalaliToGregorian

from gshconverter import gregorian_to_solar_hijri, solar_hijri_to_gregorian


def test_g_to_sh():
    y, m, d = (2024, 3, 20)
    assert (
        gregorian_to_solar_hijri(y, m, d)
        == GregorianToJalali(y, m, d).getJalaliList()
    ), f'\n{GregorianToJalali(y, m ,d).getJalaliList()=}\n{gregorian_to_solar_hijri(y, m ,d)=}'
    t1 = timeit(
        'gregorian_to_solar_hijri(y, m ,d)',
        number=100_000,
        globals=globals() | locals(),
    )
    t2 = timeit(
        'GregorianToJalali(y, m ,d).getJalaliList()',
        number=100_000,
        globals=globals() | locals(),
    )
    print(t1 / t2)

    od = timedelta(days=1)
    date = datetime(1, 1, 1)
    for i in range(1, 3000 * 366):
        y, m, d = date.day, date.month, date.day
        assert (
            gregorian_to_solar_hijri(y, m, d)
            == GregorianToJalali(y, m, d).getJalaliList()
        ), f'\n{y,m,d=}\n{GregorianToJalali(y, m ,d).getJalaliList()=}\n{gregorian_to_solar_hijri(y, m ,d)=}'
        date += od


def test_sh_to_g():
    y, m, d = (10, 12, 10)
    assert (
        solar_hijri_to_gregorian(y, m, d)
        == JalaliToGregorian(y, m, d).getGregorianList()
    ), f'\n{GregorianToJalali(y, m ,d).getJalaliList()=}\n{gregorian_to_solar_hijri(y, m ,d)=}'
    t1 = timeit(
        'solar_hijri_to_gregorian(y, m ,d)',
        number=100_000,
        globals=globals() | locals(),
    )
    t2 = timeit(
        'JalaliToGregorian(y, m ,d).getGregorianList()',
        number=100_000,
        globals=globals() | locals(),
    )

    print(t1 / t2)

    od = timedelta(days=1)
    date = datetime(1, 1, 1)
    for i in range(1, 3000 * 366):
        y, m, d = date.day, date.month, date.day
        assert (
            solar_hijri_to_gregorian(y, m, d)
            == JalaliToGregorian(y, m, d).getGregorianList()
        ), f'\n{y,m,d=}\n{JalaliToGregorian(y, m, d).getGregorianList()=}\n{solar_hijri_to_gregorian(y, m ,d)=}'
        date += od
