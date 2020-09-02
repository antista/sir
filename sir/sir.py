import os

import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.widgets import Slider

from core.differential_equations import SIR, Coefficients, dI, dR, dS, get_y

N = int(os.getenv('POPULATION', 0))
if not N:
    N = int(input('Enter an initial population: '))
days_count = int(os.getenv('DAYS_COUNT', 0), )
if not days_count:
    days_count = int(input('Enter count of days: '))

sir = SIR(S=N - 1, I=1, R=0)
coefficients = Coefficients(beta=0.75, gamma=0.25, R=None)

fig, ax = plt.subplots(figsize=(13, 9))
fig.subplots_adjust(bottom=0.2, top=0.95, left=0.075, right=0.95)

days = list(range(0, days_count))


def get_yS():
    return get_y(dS, days, sir.S, N, sir, coefficients)


def get_yI():
    return get_y(dI, days, sir.I, N, sir, coefficients)


def get_yR():
    return get_y(dR, days, sir.R, N, sir, coefficients)


yS = get_yS()
lS, = plt.plot(days, yS, linewidth=2, color='blue', label='Susceptible')

yI = get_yI()
lI, = plt.plot(days, yI, linewidth=2, color='crimson', label='Infected')

yR = get_yR()
lR, = plt.plot(days, yR, linewidth=2, color='green', label='Recovered')

plt.margins(0)
plt.xlim([0, days_count])
plt.ylim([0, N * 1.1])

# Create fields for buttons
axbeta = plt.axes([0.2, 0.1, 0.55, 0.03])
axgamma = plt.axes([0.2, 0.05, 0.55, 0.03])

sbeta = Slider(
    axbeta, 'beta', 0.0, 1.0, valinit=coefficients.beta, valstep=0.005
)
sgamma = Slider(
    axgamma, 'gamma', 0.0, 1.0, valinit=coefficients.gamma, valstep=0.005
)


def update(_):
    global coefficients
    coefficients = Coefficients(beta=sbeta.val, gamma=sgamma.val, R=None)
    lS.set_ydata(get_yS())
    lI.set_ydata(get_yI())
    lR.set_ydata(get_yR())
    fig.canvas.draw_idle()


sbeta.on_changed(update)
sgamma.on_changed(update)


def set_locators(ax):
    ax.xaxis.set_major_locator(ticker.MultipleLocator(days_count // 10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(N // 10))
    ax.grid(which='major', color='k')
    ax.minorticks_on()
    ax.grid(which='minor', color='gray', linestyle=':')


ax.set_xlabel('Days')
ax.set_ylabel('Population')
ax.legend()

set_locators(ax)
