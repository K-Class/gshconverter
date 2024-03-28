from calendar import isleap

import pandas as pd
from jdatetime.jalali import JalaliToGregorian
from pandas import DataFrame


def s2g(shyear):
    return JalaliToGregorian(shyear, 1, 1).getGregorianList()


df2 = DataFrame([*range(-621, 2378)], columns=['shyear'])
df2 = pd.concat(
    [
        df2,
        DataFrame(
            df2['shyear'].apply(s2g).to_list(),
            columns=['gyear', 'gmonth', 'gday'],
        ),
    ],
    axis=1,
)
assert (df2['gmonth'] == 3).all()
assert (df2['shyear'] == df2['gyear'] - 621).all()

df2['shleap'] = ((df2['shyear'] - 1) % 33).isin((1, 5, 9, 13, 17, 22, 26, 30))
df2['gleap'] = df2['gyear'].apply(isleap)

df2['shleap_count'] = df2['shleap'].cumsum()
df2['gleap_count'] = df2['gleap'].cumsum()

df2['leap_diff'] = df2['shleap_count'] - df2['gleap_count']

df2['calculated_day'] = df2['leap_diff'] + 21
# verify that calculations are correct for all years
assert (df2['calculated_day'] == df2['gday']).all()
