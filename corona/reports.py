import datetime

from corona.dates import START_DATE
from core.differential_equations import Coefficients


def print_prediction_header():
    """Print a header for prediction section."""
    print()
    print('-' * 60)
    print('Predictions about future evolution of the epidemic.')
    print('-' * 60)
    print()


def print_report(
        coefficients: Coefficients,
        segment_start: int,
        segment_end: int,
        last_ratio: float = None
):
    """Print report about epidemic parameters for given period."""
    print(
        'Period from {start} to {end}'.format(
            start=(
                    START_DATE + datetime.timedelta(days=segment_start)
            ).strftime('%d %B %Y'),
            end=(
                    START_DATE + datetime.timedelta(days=segment_end)
            ).strftime('%d %B %Y')
        )
    )
    if last_ratio:
        ratio = round(
            max(last_ratio, coefficients.R) / min(last_ratio, coefficients.R),
            4
        )
        print(
            'The number of social contacts {0} in {1} times.'.format(
                'decreased' if last_ratio > coefficients.R else 'increased',
                ratio
            )
        )
    print(
        '\tbeta = {beta}\n'
        '\tgamma = {gamma}\n'
        '\tR = {R}'.format(
            beta=round(coefficients.beta, 4),
            gamma=round(coefficients.gamma, 4),
            R=round(coefficients.R, 4)
        )
    )
    print()
