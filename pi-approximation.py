from matplotlib import animation
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
total = 0
points_in_circle = 0

def init():
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

def update(frame):
    global total, points_in_circle
    x = np.random.random(1)
    y = np.random.random(1)
    total += 1
    color = np.full(1, '#FF0000')
    
    if x[0]**2 + y[0]**2 <= 1:
        points_in_circle += 1
        color[0] = '#00FF00'
    ax.scatter(x, y, color=color)
    plt.title(f'Pi is Approximately: {points_in_circle/total * 4}')

def approximate_pi(n):
    x_arr = np.random.random(n)
    y_arr = np.random.random(n)
    points_in_circle = 0
    
    for i in range(n):

        if x_arr[i]**2 + y_arr[i]**2 <= 1:
            points_in_circle += 1

    
    print(points_in_circle/n * 4)

if __name__ == '__main__':
    approximate_pi(100000000)
    #ani = FuncAnimation(fig, update, interval=10, init_func=init)
    #plt.show()