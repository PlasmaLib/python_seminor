#!/usr/bin/env python

import numpy as np
import scipy.integrate as desol
import matplotlib.pyplot as plt

def predator_prey(f, t, a, b, c, d):
    #
    #  dx/dt = ax - bxy
    #  dy/dt = cxy - dy
    #
    #  f[0]    - x: Population of prey
    #  f[1]    - y: Population of predetor
    #  t       - Time
    #  a,b,c,d - Control parameters
    #
    return [a*f[0]-b*f[0]*f[1], c*f[0]*f[1]-d*f[1]]


#model
#eq1 = r"$\frac{dx}{dt} = ax - bxy$"
#eq2 = r"$\frac{dy}{dt} = cxy - dy$"
eq1 = r"$dx/dt = ax - bxy$"
eq2 = r"$dy/dt = cxy - dy$"

#input parameters
a = 1.0
b = 1.0
c = 1.0
d = 1.0
header = r"$a={0:.1f}, b={1:.1f}, c={2:.1f}, d={3:.1f}$".format(a, b, c, d)

#initial condition
f0 = [1.0, 0.1]

#independent variable
nt   = 1000
tmax = 30.0
dt = tmax/nt
t  = dt*np.arange(nt)

f = desol.odeint(predator_prey, f0, t, args=(a,b,c,d))

#plot
prey = f[:,0]
predator = f[:,1]

fig = plt.figure()
ax = fig.add_axes([0.15, 0.1, 0.8, 0.8])
ax.plot(t, prey, color='r', label=r"$x$: prey")
ax.plot(t, predator, color='b', label=r"$y$: predator")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='best')
ax.text(21, 2.7, eq1, fontsize=16)
ax.text(21, 2.5, eq2, fontsize=16)
ax.set_xlabel("Time")
ax.set_ylabel("Population")
ax.set_title(header)
plt.show()
