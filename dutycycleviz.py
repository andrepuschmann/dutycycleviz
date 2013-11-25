#!/usr/bin/env python
#
# dutycycleviz.py
#
# Copyright (C) 2013, Andre Puschmann <andre.puschmann@tu-ilmenau.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import numpy as np
import pylab as pl
import scipy.special as ss
from random import Random,expovariate,uniform
 
def kumaraswamy(a, b, x):
    e1 = x ** (a - 1)
    e2 = a * b * e1
    e3 = 1 - x ** a
    e4 = b - 1
    return e2 * e3 ** e4

def kumaraswamy_cdf(a, b, x):
    e1 = 1 - x ** a
    e2 = e1 ** b
    return e1 - e2

def kumaraswamy_cdf_invers(a, b, u):
    e1 = 1 / b
    e2 = (1 - u) ** e1
    e3 = 1 - e2
    e4 = 1 / a
    return e3 ** e4

def plot_kumaraswamy(a, b, desc='Kumaraswamy'):
    Ly = []
    Lx = []
    xes = np.mgrid[0:1:1000j]
    for x in xes:
        Lx.append(x)
        Ly.append(kumaraswamy(a, b, x))
    pl.plot(Lx, Ly, label="%s (a=%.2f, b=%.2f)" %(desc, a, b))
    
def beta(a, b, mew):
    e1 = ss.gamma(a + b)
    e2 = ss.gamma(a)
    e3 = ss.gamma(b)
    e4 = mew ** (a - 1)
    e5 = (1 - mew) ** (b - 1)
    return (e1/(e2*e3)) * e4 * e5
 
def plot_beta(a, b):
    Ly = []
    Lx = []
    mews = np.mgrid[0:1:100j]
    for mew in mews:
        Lx.append(mew)
        Ly.append(beta(a, b, mew))
    pl.plot(Lx, Ly, label="Beta: a=%f, b=%f" %(a,b))
 

# mu is location
# sigma is scale
# xi is shape
# U is input
# X = mu + sigma(U^-xi - 1) / xi  (http://en.wikipedia.org/wiki/Generalized_Pareto_distribution)
def gpd_cdf_invers(mu, sigma, xi, U):
    e1 = U ** (-xi) - 1
    e2 = sigma * e1 / xi
    return mu + e2


# based on invers CDF of the Kumaraswamy distribution found
# here: http://www.johndcook.com/blog/2009/11/24/kumaraswamy-distribution/ 
def plot_activity(a, b, N=10):
    start = 0
    end = N * 100
    Ly = []
    Lx = []
    samples = xrange(start, end, N)
    
    print samples
    for x in samples:
        r = uniform(0, 1)
        #print "r: %.2f" % (r)
        hui = kumaraswamy_cdf_invers(a, b, r)
        holds = xrange(0, N, 1)
        for hold in holds:
            print "y: %i" % (x+hold)
            Lx.append(x+hold)
            Ly.append(hui)
    pl.plot(Lx, Ly, label="CDF: a=%f, b=%f" %(a,b))
    

def plot_gpd_activity(busy_mu, busy_sigma, busy_xi, idle_mu, idle_sigma, idle_xi, desc="Random"):
    Ly = []
    Lx = []
    current_time = 0
    total_busy_time = 0
    iterations = xrange(0,40)
    for i in iterations:
        # start a new busy period
        Lx.append(current_time)
        Ly.append(1)
        # get length of next busy period
        u = uniform(0, 1)
        next_busy = gpd_cdf_invers(busy_mu, busy_sigma, busy_xi, u)
        #print "next_busy: %f" % next_busy
        current_time += next_busy
        total_busy_time += next_busy
        Lx.append(current_time)
        Ly.append(1)
        
        # start a new idle period
        Lx.append(current_time)
        Ly.append(0)
        # compute length for next idle period
        u = uniform(0, 1)
        next_idle = gpd_cdf_invers(idle_mu, idle_sigma, idle_xi, u)
        #print "next_idle: %f" % next_idle
        current_time += next_idle
        Lx.append(current_time)
        Ly.append(0)

    # compute duty_cycle for current example
    duty_cycle = total_busy_time / current_time
    #print "total_busy_time: %f" % total_busy_time
    #print "current_time: %f" % current_time
    #print "duty_cycle: %f" % duty_cycle
    
    #plt.axis( [0, 10, 0, 6])
    pl.ylim(-0.1, 1.1)
    pl.legend()
    
    return pl.plot(Lx, Ly, label="%s, DC=%.2f" % (desc, duty_cycle))


def main():
    #plot_beta(0.1, 0.1)
    #plot_beta(1, 1)
    #plot_beta(2, 3)
    #plot_beta(8, 4)   

    #plot_kumaraswamy(0.66, 20.8, "Sporadic use") # L1 case
    #plot_kumaraswamy(0.17, 0.35, "Intermittent use, high-load after low-load periods") # M1 case
    #plot_kumaraswamy(11.49, 0.38, "Used most of the time") # H1 case
    #plot_kumaraswamy(2.44, 317.31, "Regularly use, low activity") # L2 case
    #plot_kumaraswamy(8.60, 1581.54, "Weak oscillations around mean") # M2 case
    #plot_kumaraswamy(19.81, 10.59, "Constant itensive use") # H2 case
    #pl.xlim(0.0, 1.0)
    #pl.ylim(0.0, 20.0)
    
    #plot_activity(0.17, 0.35, 10)
    #plot_activity(19.81, 10.59)
    
    pl.figure( 1 )
    ax1 = pl.subplot( 5, 1, 1 ) # 2 rows, 1 column, figure 1
    
    # for low load level
    plot_gpd_activity(3.5150, 1.6960, 0.0285, 3.61, 38.3633, 0.2125, "Very low")
    
    ax2 = pl.subplot( 5, 1, 2 )
    plot_gpd_activity(3.5150, 2.6240, 0.1884, 3.578, 10.9356, 0.1784, "Low")
    
    ax3 = pl.subplot( 5, 1, 3 )
    plot_gpd_activity(3.5150, 5.1483, 0.1978, 3.5160, 4.6583, 0.2156, "Medium")
    
    ax4 = pl.subplot( 5, 1, 4 )
    plot_gpd_activity(3.5470, 10.7968, 0.1929, 3.5310, 2.6272, 0.2119, "High")
    
    ax5 = pl.subplot( 5, 1, 5 )
    plot_gpd_activity(3.5940, 52.8611, 0.2377, 3.5160, 1.6609, 0.0068, "Very high")
    
    # Have a single legend for each subplot
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()

    pl.show()
 
if __name__ == "__main__":
    main()
