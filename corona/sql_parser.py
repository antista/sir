from collections import namedtuple

import datadotworld as dw

DayStat = namedtuple('DayStat', 'date, new_cases, total_cases')

query = dw.query(
    'markmarkoh/coronavirus-data',
    'SELECT date, new_cases, total_cases '
    'FROM full_data WHERE location = "World"'
)

df = query.dataframe

all_cases = [
    DayStat(*day_stat) for day_stat in
    zip(df.date, df.new_cases, df.total_cases)
]
