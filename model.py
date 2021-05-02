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
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

dt = 0.1 # Timestep size [s]

# Load in constants from json file
f = open('constants.json')
c = json.load(f)

# Define initial conditions
y_hat = 0 # Initial position [m]
dy_hat = 0 # Initial velocity [m/s]

ts = [0]
ys = [-0.01]
dys = [dy_hat]

def controller():
    """ Takes in __ as input, outputs a current to send to the system """
    return 0.3

def animate(i):
    if i == 0:
        return
    i = i + 1

    # Update controller input
    I = controller()

    # Compute new position
    F_g = c['m'] * 9.81 # Force of gravity [N]

    # Nonlinear model
    F_m_abs = (c['mu']*c['N']*I*c['A']*c['m2']) / (c['L']*4*pi*abs(ys[-1]))
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

    ax1.cla()
    ax1.plot(ts, ys)
    plt.ylim([-0.1, 0]) # Keep plot zoomed into the first 10 cm
    plt.ylabel("Magnet Position [m]")
    plt.xlabel("Time [s]")

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
