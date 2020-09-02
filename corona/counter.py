from typing import Iterable, List

import numpy
from scipy import optimize

from corona import dates
from corona.consts import DURATION, N
from corona.reports import print_report
from core.differential_equations import SIR, Coefficients, dI, dR, dS, get_y


def get_curr_s(curr_i: List[int], curr_r: List[int]) -> List[int]:
    """Calculate count of currently susceptible people for each day.

    Arguments:
        curr_i - list of currently infected people for each day
        curr_r - list of currently recovered people for each day
    """
    return [N - curr_i[i] - curr_r[i] for i in range(len(curr_i))]


def get_curr_i(total_i: List[int], curr_r: List[int]) -> List[int]:
    """Calculate count of currently infected people for each day.

    Arguments:
        total_i - list of total infected people for each day
        curr_r - list of currently recovered people for each day
    """
    curr_i = []
    for i in range(len(total_i)):
        curr_i.append(total_i[i] - curr_r[i])
    return curr_i


def get_curr_r(new_cases_daily: List[int]) -> List[int]:
    """Calculate count of currently recovered people for each day.

    Arguments:
        new_cases_daily - list of new infected cases for every day
    """
    recov = [0 for _ in range(DURATION)]
    recov += [r for r in new_cases_daily]
    total_r = []
    sum_recov = 0
    for r in recov:
        sum_recov += r
        total_r.append(sum_recov)
    return total_r


def count_beta(sirs: List[SIR]) -> float:
    """Calculate average beta accounting to differential equations."""
    betas = []
    for last_sir, curr_sir in zip(sirs, sirs[1:]):
        if last_sir.S * last_sir.I != 0:
            betas.append(
                N * (last_sir.S - curr_sir.S) / (last_sir.S * last_sir.I)
            )
    return sum(betas) / len(betas)


def count_gamma(sir: List[SIR]) -> float:
    """Calculate average gamma accounting to differential equations."""
    gammas = []
    for last_sir, curr_sir in zip(sir, sir[1:]):
        if last_sir.I != 0:
            gammas.append(
                (-curr_sir.I - curr_sir.S + last_sir.S + last_sir.I
                 ) / last_sir.I
            )
    return sum(gammas) / len(gammas)


def get_trend(value: float, a: float, b: float) -> float:
    """Get trend value by given parameters."""
    return a * numpy.exp(b * value)


def get_trend_parameters(
        dates: List[int], curr_i: List[int]
) -> Iterable[float]:
    """Count trend parameters for disease cases for current period.

    Arguments:
        dates - list of days numbers
        curr_i - list of currently infected people for each day
    """
    return optimize.curve_fit(get_trend, dates, curr_i, p0=(4, 0.1))[0]


def get_i_trend(dates: List[int], parameters: Iterable[float]):
    """Return I values averaged by a trend parameters.

    Arguments:
        dates - list of days numbers
        parameters - trend line parameters
    """
    return [int(get_trend(x, *parameters)) for x in dates]


def get_all_coefficients(sirs: List[SIR]) -> List[Coefficients]:
    """Count all coefficients (beta, gamma, R) for given values."""
    all_coefficients = []
    for sir in sirs:
        curr_beta = count_beta(sir)
        curr_gamma = count_gamma(sir)
        curr_coefficients = Coefficients(
            beta=curr_beta, gamma=curr_gamma, R=curr_beta / curr_gamma
        )
        all_coefficients.append(curr_coefficients)
    return all_coefficients


def get_all_sirs(
        days_sections: List[List[int]], curr_i: List[int]
) -> List[SIR]:
    """Return SIR parameters for every day."""
    all_r_trend = [0 for _ in range(DURATION)]
    all_sirs = []

    for days_section in days_sections:
        start, end = days_section[0] - 1, days_section[-1]
        trend_parameters = get_trend_parameters(
            days_section, curr_i[start:end]
        )
        curr_i_trend = get_i_trend(days_section, trend_parameters)

        all_r_trend += curr_i_trend
        curr_r_trend = all_r_trend[start:end]

        curr_s_trend = get_curr_s(curr_i_trend, curr_r_trend)

        all_sirs.append([
            SIR(s, i, r) for s, i, r in
            zip(curr_s_trend, curr_i_trend, curr_r_trend)
        ])
    return all_sirs


def generate_i(
        days_sections: List[List[int]],
        all_sirs: List[SIR],
        all_coefficients: List[Coefficients]
) -> List[List[float]]:
    """Generate value of infected people count for each day."""
    gen_yI = []
    for i, days_section in enumerate(days_sections):
        last_dot = gen_yI[-1][-1:] if gen_yI else []
        gen_yI.append(last_dot + get_y(
            dI,
            days_section,
            all_sirs[i][0].I,
            N,
            all_sirs[i][0],
            all_coefficients[i]
        ))

        print_report(
            all_coefficients[i],
            days_section[0] - 1,
            days_section[-1],
            last_ratio=all_coefficients[i - 1].R if i != 0 else None
        )
    return gen_yI


def get_beta_ratios(all_coefficients: List[Coefficients]) -> List[float]:
    """Return list of future beta change ratios."""
    return [
        1,
        (
                all_coefficients[dates.BORDERS_CLOSE_DATE_INDEX - 1].beta /
                all_coefficients[dates.BORDERS_CLOSE_DATE_INDEX].beta
        ),
    ]


def get_future_coefficients(
        all_last_coefficients: List[Coefficients]
) -> List[Coefficients]:
    """Return all predicted coefficients."""
    all_coefficients = []
    last_coefficients = all_last_coefficients[-1]
    beta_ratios = get_beta_ratios(all_last_coefficients)
    for beta_ratio in beta_ratios:
        curr_beta = last_coefficients.beta * beta_ratio
        all_coefficients.append(
            Coefficients(
                beta=curr_beta,
                gamma=last_coefficients.gamma,
                R=curr_beta / last_coefficients.gamma
            )
        )
    return all_coefficients


def get_predicted_i(
        days_sections: List[List[int]],
        last_sir: SIR,
        future_coefficients: List[Coefficients]
) -> List[List[float]]:
    """Return all predicted infected people count values."""
    all_predicted_i = []

    for i, days_section in enumerate(days_sections):
        curr_coefficients = future_coefficients[i]
        yS = get_y(
            dS, days_section, last_sir.S, N, last_sir, curr_coefficients
        )
        yI = get_y(
            dI, days_section, last_sir.I, N, last_sir, curr_coefficients
        )
        yR = get_y(
            dR, days_section, last_sir.R, N, last_sir, curr_coefficients
        )
        all_predicted_i += yI

        print_report(
            curr_coefficients,
            days_section[0] - 1,
            days_section[-1],
            last_ratio=future_coefficients[i - 1].R if i != 0 else None
        )

        last_sir = SIR(yS[-1], yI[-1], yR[-1])

    return all_predicted_i
