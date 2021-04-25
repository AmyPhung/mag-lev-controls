import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

dt = 0.1 # Timestep size [s]
m = 0.5 # Object mass [kg]
F_g = m * -9.81 # Force of gravity [N]

y_hat = 0 # Initial position [m]
dy_hat = 0 # Initial velocity [m/s]

ts = [0]
ys = [y_hat]
dys = [dy_hat]

def animate(i):
    if i == 0:
        return
    i = i + 1
    t = float(i*dt)
    dy = float(dys[-1] + F_g*dt)
    y = float(ys[-1] + dy*dt)

    ts.append(t)
    ys.append(y)
    dys.append(dy)

    ax1.cla()
    ax1.plot(ts, ys)

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
