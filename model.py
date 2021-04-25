import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random


fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

ts = []
ys = []

dt = 0.1

def animate(i):
    t = float(i*dt)
    y = random.randint(0,5)

    ts.append(t)
    ys.append(y)

    ax1.cla()
    ax1.plot(ts, ys)

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
