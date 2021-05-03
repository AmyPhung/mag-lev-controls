"""
Linear model of mag-lev system
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
from math import pi
import json

# Initialize figures
fig, axs = plt.subplots(2)
# fig.suptitle('Vertically stacked subplots')


dt = 0.01 # Timestep size [s]

# Load in constants from json file
f = open('constants.json')
c = json.load(f)

# Define initial conditions
y_hat = -0.01  # Initial position [m]
dy_hat = 0.0 # Initial velocity [m/s]
I_hat = 0.0  # Initial current [A]

# Lists to keep track of system state over time
ts = [0.0]         # Discrete timesteps

ys = [y_hat]     # Magnet position at each timestep
dys = [dy_hat]   # Magnet position derivative at each timestep

Is = [I_hat]     # Circuit current at each timestep
dIs = [0.0]        # Circuit current derivative at each timestep

def controller():
    """ Takes in __ as input, outputs a voltage to send to the system """
    return 5.0

# def sensor():


def animate(i):
    if i == 0:
        return
    i = i + 1

    # Update controller input
    V = controller()

    # Compute current
    dI = (V - Is[-1]*c['R']) / c['L']
    I = Is[-1] + dI

    # Compute new position
    F_g = c['m'] * 9.81 # Force of gravity [N]

    # Nonlinear model
    F_m_abs = (c['mu']*c['N']*I*c['A']*c['m2']) / (c['l']*4*pi*abs(ys[-1]))
    F_net_abs = F_m_abs - F_g

    # Linear model - use difference equation to step through time
    # TODO

    t = float(i*dt)
    dy = float(dys[-1] + F_net_abs*dt)
    y = float(ys[-1] + dy*dt)

    # If y > 0, the magnet will just stick to the electromagnet
    # (it can't phase through it)
    if y > 0.00001:
        y = 0.00001 # Avoiding float division by zero error
        dy = y - ys[-1]

    ts.append(t)
    ys.append(y)
    dys.append(dy)
    Is.append(I)
    dIs.append(dI)

    axs[0].cla()
    axs[0].plot(ts, ys)
    axs[0].set_ylim([-0.1, 0]) # Keep position plot zoomed into the first 10 cm

    axs[1].cla()
    axs[1].plot(ts, Is)

    axs[0].set_ylabel("Magnet Position [m]")
    axs[1].set_ylabel("Circuit Current [A]")
    axs[1].set_xlabel("Time [s]")

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
