from corona import counter, dates
from corona.plots import plot_all
from corona.reports import print_prediction_header
from corona.sql_parser import all_cases


def main():
    """Main program function."""  # noqa: D401
    new_cases_daily = [s.new_cases for s in all_cases]

    total_i = [s.total_cases for s in all_cases]
    curr_r = counter.get_curr_r(new_cases_daily)
    curr_i = counter.get_curr_i(total_i, curr_r)

    # Split days on sections with different beta and gamma parameters
    days_sections = dates.get_days_sections(dates.DAYS, dates.STAGES_DATES)

    # Get SIR parameters for each day
    all_sirs = counter.get_all_sirs(days_sections, curr_i)
    # Get beta, gamma and R parameters for each day
    all_coefficients = counter.get_all_coefficients(all_sirs)
    # Generate infected people count values for each section and day
    gen_yI = counter.generate_i(days_sections, all_sirs, all_coefficients)

    print_prediction_header()

    # Split future days on sections with different beta and gamma parameters
    future_days_sections = dates.get_days_sections(
        dates.ALL_DATES, dates.FUTURE_STAGES_DATES
    )
    # Predict future beta and gamma coefficients
    future_coefficients = counter.get_future_coefficients(all_coefficients)
    # Count infected people count values by predicted beta and gamma parameters
    all_predicted_i = counter.get_predicted_i(
        future_days_sections, all_sirs[-1][-1], future_coefficients
    )

    plot_all(
        days_sections, gen_yI, curr_i, all_predicted_i, future_days_sections
    )
