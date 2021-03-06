"""Importing necessary libraries
"""

import numpy as np
import matplotlib.pyplot as plt

"""Important constants"""

G = 6.67 * 10 ** -11  # Nm/kg^2
M = 6 * 10 ** 24  # kg
r = 12756000 / 2  # m

"""defining necessary functions"""


def earth(r):  # creating earth
    circ = np.linspace(0, 360, 1000)
    plt.figure(figsize=(10, 10))
    circx = r * np.cos(circ)
    circy = r * np.sin(circ)
    plt.plot(circx, circy, '.', linewidth=1)


def ax(x, y):  # component of acceleration in x direction
    return G * M * x / (x ** 2 + y ** 2) ** (3 / 2)


def ay(x, y):  # component of acceleration in y direction
    return G * M * y / (x ** 2 + y ** 2) ** (3 / 2)


def V(x, y, u, a, dt):  # velocity function
    v = u - a(x, y) * dt
    return v


def X(x, y, u, a, dt):  # displacement as a function of x y velocity acceleration and time
    newV = V(x, y, u, ax, dt)
    averageV = (newV + u) / 2
    newX = x + averageV * dt - 0.5 * ax(x, y) * dt ** 2
    return newX, newV


def Y(x, y, u, a, dt):  # displacement in x direction as a function of x y velocity and acceleration, returns new
    newV = V(x, y, u, ay, dt)
    averageV = (newV + u) / 2
    newY = y + averageV * dt - 0.5 * ay(x, y) * dt ** 2
    return newY, newV


def dist_calc(xin, yin, launch_angle):  # stuff for finding the launch range
    if launch_angle < 90:  # fired to the right
        if yin >= 0:
            latn = np.degrees(np.arctan(yin / np.abs(xin)))
            print('the latitude of hit is ', latn, 'N')
            if yin > 0 and xin > 0:
                print('the distance covered is ', np.pi * 2 * r / 360 * (90 - latn) / 1000, 'kms')
            else:
                print('the distance covered is ', np.pi * 2 * r / 360 * (270 + latn) / 1000, 'kms')

        elif yin < 0:
            latn = np.degrees(np.arctan(np.abs(yin) / np.abs(xin)))
            print('the latitude of hit is ', latn, 'S')
            if yin < 0 and xin > 0:
                print('the distance covered is ', np.pi * 2 * r / 360 * (90 + latn) / 1000, 'kms')
            else:
                print('the distance covered is ', np.pi * 2 * r / 360 * (270 - latn) / 1000, 'kms')


    else:  # fired to the left
        if yin >= 0:
            latn = np.degrees(np.arctan(yin / np.abs(xin)))
            print('the latitude of hit is ', latn, 'N')
            if yin > 0 and xin > 0:
                print('the distance covered is ', np.pi * 2 * r / 360 * (270 + latn) / 1000, 'kms')
            else:
                print('the distance covered is ', np.pi * 2 * r / 360 * (90 - latn) / 1000, 'kms')

        elif yin < 0:
            latn = np.degrees(np.arctan(np.abs(yin) / np.abs(xin)))
            print('the latitude of hit is ', latn, 'S')
            if yin < 0 and xin > 0:
                print('the distance covered is ', np.pi * 2 * r / 360 * (270 - latn) / 1000, 'kms')
            else:
                print('the distance covered is ', np.pi * 2 * r / 360 * (90 + latn) / 1000, 'kms')


"""The main stuff"""

m = input("Enter the launch velocity in m/s")  # initial velocity in m/s
u = int(m)
lat = np.radians(90)  # launch latitude
mn = input("Enter the launch angle in degrees")
theta = np.radians(int(mn))  # launch angle
dt = 0.01  # small time?

xpos = 1.01 * r * np.cos(lat)  # launch location
ypos = 1.01 * r * np.sin(lat)

Vx = u * np.cos(theta)  # launch velocity components
Vy = u * np.sin(theta)

xin = xpos  # launch positions
yin = ypos

xo = []  # list to be filled with displacement values
yo = []

for i in range(1000000):
    xin, Vx = X(xin, yin, Vx, ax, dt)  # updating s and y positions 500000 times
    yin, Vy = Y(xin, yin, Vy, ay, dt)

    xo.append(xin)  # adding a component in the list each time loop is conducted
    yo.append(yin)
    if xin ** 2 + yin ** 2 < r ** 2:  # condition for not entering the earth
        dist_calc(xin, yin, np.degrees(theta))

        break  # breaking out of loop if touches earth

plt.figure(figsize=(10, 10))
earth(r)  # creating earth
plt.plot(xo, yo, 'r')  # plotting trajectory
plt.show()
