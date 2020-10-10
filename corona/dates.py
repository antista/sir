import os
from typing import List

from corona.sql_parser import all_cases

# There are approximate counts of the days from the start of the COVID-19
# epidemic when some steps were taken to prevent the spread of the disease

# First steps were taken
first_steps = 94
# Borders were closed
borders_closed = first_steps + 15
# BLM meetings in America
America_meetings = borders_closed + 37
# Almost all infected in meetings people recovered
calm_quarantine = America_meetings + 68
# Almost all social active people infected and recovered
almost_all_recovered = calm_quarantine + 15

# Number of days the COVID-19 disease has existed
DAYS_COUNT = len(all_cases)
# Days enumerator
DAYS = list(range(1, DAYS_COUNT + 1))

# First epidemic day
START_DATE = all_cases[0].date
# Segments of dates of different stages of the epidemic
STAGES_DATES = [
    0,
    first_steps,
    borders_closed,
    America_meetings,
    calm_quarantine,
    almost_all_recovered,
    250,
    DAYS_COUNT
]
# Index of the day when borders was closed in the dates_segments list
BORDERS_CLOSE_DATE_INDEX = 2
# Last day of prediction
LAST_PREDICT_DAY = int(os.getenv('LAST_PREDICT_DAY', 365))
# Days enumerator with future days
ALL_DATES = list(range(1, LAST_PREDICT_DAY + 1))
# Segments of future dates of different stages of the epidemic
FUTURE_STAGES_DATES = [
    DAYS_COUNT,
    289,
    LAST_PREDICT_DAY
]


def get_days_sections(
        dates: List[int], days_sections: List[int]
) -> List[List[int]]:
    """Generate dates sections from dates array."""
    return [
        dates[start:end] for start, end in zip(
            days_sections, days_sections[1:]
        )
    ]
