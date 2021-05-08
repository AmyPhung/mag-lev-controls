"""
Linear model of mag-lev system

Current assumptions:
- Hall effect sensor is only dependent on permanent magnet's location
- Magnets are "far away" from electromagnet - assuming point-like poles
instead of finite surfaces
- Setpoint is chosen such that constants in linearized ODE cancel out with
gravity
- Electromagnet inductance isn't important to consider
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
from math import pi, sqrt
import json

# Initialize figures
fig, axs = plt.subplots(3)
# fig.suptitle('Vertically stacked subplots')


dt = 0.01 # Timestep size [s]

# Load in constants from json file
f = open('constants.json')
c = json.load(f)

# Define initial conditions
y_hat = -0.04  # Initial position [m]
dy_hat = 0.0 # Initial velocity [m/s]
I_hat = 0.0  # Initial current [A]

# Lists to keep track of system state over time
ts = [0.0]              # Discrete timesteps

ys = [y_hat]            # Magnet position at each timestep (nonlinear model)
ys_approx = [y_hat]     # Magnet position at each timestep (linear model)
dys = [dy_hat]          # Magnet position derivative at each timestep (nonlinear model)

Is = [I_hat]            # Circuit current at each timestep
dIs = [0.0]             # Circuit current derivative at each timestep

# Defining additional constants to make code cleaner
a2 = (c['mu']*c['N']*c['A']*c['m2']) / (c['l']*4*pi*(y_hat**2))
a3 = -(c['mu']*c['N']*I_hat*c['A']*c['m2']) / (c['l']*2*pi*(y_hat**3))

# Necessary global temporary variable
y_approx = 0

def controller(y_measured):
    """ Takes in position measurement as input, outputs a voltage to
    send to the system """
    return -1

def hallToPosition(V_h, V_e):
    """ Takes in hall effect sensor voltage as input, outputs a voltage to
    send to the system """
    return

def sensor(y):
    """ Compute hall effect sensor reading based on magnet position """
    # Compute magnetic flux density for cylindrical magnet
    B = (c['B_r']/2) * (                                          \
        (c['d'] + y) / sqrt(c['r']**2 + (c['d'] + y)**2) -        \
        y / sqrt(c['r']**2 + y**2) )

    # TODO: Figure out how to get hall effect coefficient
    V_h = c['R_h'] * (c['I_h'] / c['t_h'] * B)
    return V_h

def animate(i):
    if i == 0:
        return
    i = i + 1

    if i*dt > 0.2:
        return

    # Compute sensor response based on last timestep
    V_h = sensor(ys[-1])

    # Update controller input
    V = controller(V_h)

    # UNCOMMENT FOR WITH-INDUCTOR MODEL
    # Compute current - Inductor model
    # Note: For certain constant values, the effect of the inductor will be too
    # small, and cause rounding errors.
    # dI = (V - Is[-1]*c['R']) / c['L']
    # I = Is[-1] + dI*dt

    # UNCOMMENT FOR NO-INDUCTOR MODEL
    # Compute current - excluding inductor
    # Works well for small inductance values (assume electromagnet responds)
    # instantaneously
    dI = 0
    I = V / c['R']
    print(I)

    # Compute new position
    F_g = c['m'] * 9.81 # Force of gravity [N]

    # Nonlinear model
    F_m_abs = (c['mu']*c['N']*I*c['A']*c['m2']) / (c['l']*4*pi*abs(ys[-1]**2))
    F_net_abs = F_m_abs - F_g

    t = float(i*dt)
    dy = float(dys[-1] + (F_net_abs/c['m'])*dt)
    y = float(ys[-1] + dy*dt)

    # Linear model - use difference equation to step through time
    if len(ys) < 2: # For first step, use dy_hat as second initial condition
        y_approx = ys_approx[-1] + dy_hat
    else:
        # Assumes linearization constants cancel with effect of gravity
        y_approx = (dt**2 / c['m']) * (a2*I + a3*ys_approx[-2]) + \
            2*ys_approx[-1] - ys_approx[-2]
        # print(ys_approx[-1])
        # print(y_approx)

    # If y > 0, the magnet will just stick to the electromagnet
    # (it can't phase through it)
    if y > 0.00001:
        y = 0.00001 # Avoiding float division by zero error
        dy = y - ys[-1]
    if y_approx > 0.00001:
        y_approx = 0.00001 # Avoiding float division by zero error

    ts.append(t)
    ys.append(y)
    dys.append(dy)
    Is.append(I)
    dIs.append(dI)
    ys_approx.append(y_approx)

    axs[0].cla()
    axs[0].plot(ts, ys)
    axs[0].set_ylim([-0.1, 0.01]) # Keep position plot zoomed into the first 10 cm

    axs[1].cla()
    axs[1].plot(ts, ys_approx)
    axs[1].set_ylim([-0.1, 0.01]) # Keep position plot zoomed into the first 10 cm

    axs[2].cla()
    axs[2].plot(ts, Is)

    axs[0].set_ylabel("Magnet Position [m] (nonlinear)")
    axs[1].set_ylabel("Magnet Position [m] (linear)")
    axs[2].set_ylabel("Circuit Current [A]")
    axs[2].set_xlabel("Time [s]")



ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
