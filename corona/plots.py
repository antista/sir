from functools import reduce
from typing import List

import matplotlib.pyplot as plt
from matplotlib import ticker

from corona.dates import DAYS, LAST_PREDICT_DAY


def plot_averaged_i(days_sections: List[List[int]], curr_i: List[List[float]]):
    """Plot averaged real infected plot."""
    last_day = []
    for days_section, yI in zip(days_sections, curr_i):
        genI, = plt.plot(last_day + days_section, yI, linewidth=3, color='red')
        if last_day:
            marker = plt.scatter(
                last_day, yI[0], linewidth=2, color='orange', marker='o'
            )
            marker.set_zorder(10)
        last_day = days_section[-1:]
    genI.set_label('SIR infected')


def plot_real_i(curr_i: List[float]):
    """Plot real infected plot."""
    plt.plot(DAYS, curr_i, linewidth=2, color='blue', label='Real infected')


def plot_predicted_i(
        curr_i: List[List[float]], days_sections: List[List[int]]
):
    """Plot predicted future infected plot."""
    plt.plot(
        reduce(lambda x, y: x + y, days_sections), curr_i,
        linewidth=2,
        color='green',
        label='Predicted infected',
    )


def plot_all(
        days_sections: List[List[int]],
        gen_yI: List[List[float]],
        curr_i: List[float],
        all_predicted_i: List[List[float]],
        future_days_sections: List[List[int]]
):
    """Plot all infected plots.

    Plot real infected plot, averaged infected plot and predicted infected plot
    """
    fig, ax = plt.subplots(figsize=(15, 9))
    fig.subplots_adjust(bottom=0.075, top=0.95, left=0.05, right=0.95)

    plot_averaged_i(days_sections, gen_yI)
    plot_real_i(curr_i)
    plot_predicted_i(all_predicted_i, future_days_sections)

    plt.margins(0)
    plt.xlim([0, LAST_PREDICT_DAY])
    plt.ylim(top=max(*curr_i, *all_predicted_i) * 1.1)

    def set_locators(ax):
        ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
        ax.grid(which='major', color='k')
        ax.minorticks_on()
        ax.grid(which='minor', color='gray', linestyle=':')

    ax.set_xlabel('Days')
    ax.set_ylabel('Population')
    ax.legend()
    set_locators(ax)
