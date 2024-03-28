from calendar import isleap

import pandas as pd
from jdatetime.jalali import GregorianToJalali
from pandas import DataFrame


def g2s(gyear):
    return GregorianToJalali(gyear, 1, 1).getJalaliList()


df = DataFrame([*range(1, 3000)], columns=['gyear'])
df = pd.concat(
    [
        df,
        DataFrame(
            df['gyear'].apply(g2s).to_list(),
            columns=['shyear', 'shmonth', 'shday'],
        ),
    ],
    axis=1,
)
assert (df['shmonth'] == 10).all()
assert (df['shyear'] == df['gyear'] - 622).all()

df['shleap'] = (df['shyear'] % 33).isin((1, 5, 9, 13, 17, 22, 26, 30))
df['gleap'] = df['gyear'].apply(isleap)


df['shleap_count'] = df['shleap'].cumsum()
df['gleap_count'] = df['gleap'].cumsum()

df['leap_diff'] = df['gleap_count'] - df['shleap_count']

df['calculated_day'] = df['leap_diff'].shift(fill_value=0) + 11
# verify that calculations are correct for all years
assert (df['calculated_day'] == df['shday']).all()
