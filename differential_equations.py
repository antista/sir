from typing import Callable, List, NamedTuple

SIR = NamedTuple('SIR', [('S', float), ('I', float), ('R', float)])
Coefficients = NamedTuple(
    'Coefficients', [('beta', float), ('gamma', float), ('R', float)]
)


def dS(N: int, sir: SIR, coefficients: Coefficients) -> float:
    """Count the next value of differential equation of susceptible people."""
    return sir.S - (coefficients.beta * sir.S * sir.I) / N


def dI(N: int, sir: SIR, coefficients: Coefficients) -> float:
    """Count the next value of differential equation of infected people."""
    return (sir.I + (coefficients.beta * sir.S * sir.I) / N -
            coefficients.gamma * sir.I)


def dR(N: int, sir: SIR, coefficients: Coefficients) -> float:
    """Count the next value of differential equation of recovered people."""
    return sir.R + coefficients.gamma * sir.I


def get_y(
        func: Callable[[int, SIR, Coefficients], float],
        days: List[int],
        start: int,
        N: int,
        curr_sir: SIR,
        coefficients: Coefficients
) -> List[float]:
    """Count all corresponding cases values for dates list.

    Use `func` parameter as a differential equation function
    to numerically solve the system of the differential equations
    for a current parameter.

    Arguments:
        func - differential equation function
        days - days list
        start - start value of
            susceptible if func==dS,
            infected if func==dI,
            recovered if func==dR
        N - population size
        curr_sir - current values of susceptible, infected and recovered people
        coefficients - current values of beta, gamma and R parameters
    """
    cases = [start]
    for _ in range(len(days) - 1):
        cases.append(func(N, curr_sir, coefficients))
        next_sir = SIR(
            dS(N, curr_sir, coefficients),
            dI(N, curr_sir, coefficients),
            dR(N, curr_sir, coefficients)
        )
        curr_sir = next_sir
    return cases
