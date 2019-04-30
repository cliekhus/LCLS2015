# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:47 2019

@author: chelsea
"""

import h5py
from pylab import exp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from itertools import compress
import statistics as stat

ScanName = h5py.File('Data\ldat_xppj6715_Run371.h5')
ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]
diode = [x[2] for x in list(ScanName['/diodeU/channels'])]  
xOn = list(map(bool, ScanName['/lightStatus/xray']))
lOn = list(map(bool, ScanName['/lightStatus/laser']))

xOn = [x==1 for x in xOn]

slope = [a/b for a,b in zip(diode,ipm2)]
xonfilter = [a>0 and b for a,b in zip(slope,xOn)]

plt.figure()
plt.scatter(list(compress(diode, xonfilter)),list(compress(slope, xonfilter)),s=2)

slopemedian = stat.median(list(compress(slope,xonfilter)))
slopestd = stat.stdev(list(compress(slope,xonfilter)))
numstds = .5

slopefilter = [abs(a-slopemedian) < numstds*slopestd and b for a,b in zip(slope,xonfilter)]

plt.scatter(list(compress(diode, slopefilter)),list(compress(slope,slopefilter)),s=2,alpha=.2)

plt.figure()
plt.scatter(ipm2,diode,s=2)
plt.scatter(list(compress(ipm2, slopefilter)), list(compress(diode, slopefilter)),s=2,alpha=.2)

diodefiltered = list(compress(diode,slopefilter))
ipm2filtered = list(compress(ipm2,slopefilter))
slopefiltered = list(compress(slope,slopefilter))

plt.figure()
slopehist = plt.hist(slopefiltered,1000)
slopes = slopehist[1]
slopes = slopes[1:]

def gauss(x,a,x0,sig):
    return a*exp(-(x-x0)**2/2/sig**2)

def gausfit(x,a0,x00,sig0,a1,x01,sig1,a2,x02,sig2):
    return gauss(x,a0,x00,sig0) + gauss(x,a1,x01,sig1) + gauss(x,a2,x02,sig2)

params,cov = curve_fit(gausfit,slopes,slopehist[0])

plt.plot(slopes,gausfit(slopes,*params))

a0fit = [params[0],params[3],params[6]]
x0fit = [params[1],params[4],params[7]]
sigfit = [params[2],params[5],params[8]]

paramssorted = sorted(zip(x0fit,a0fit,sigfit))

desiredgauss = gauss(slopefiltered,paramssorted[2][1],paramssorted[2][0],paramssorted[2][2])
closegauss = gauss(slopefiltered,paramssorted[1][1],paramssorted[1][0],paramssorted[1][2])

gaussfilter = [x>y for x,y in zip(desiredgauss,closegauss)]

plt.figure()
plt.scatter(ipm2filtered,diodefiltered,s=2)
plt.scatter(list(compress(ipm2filtered, gaussfilter)), list(compress(diodefiltered, gaussfilter)), s=2, alpha=.2)

#plt.figure()
#plt.scatter(ipm2, diode, s=2)
#plt.scatter([a for a,b in zip(ipm2,db.labels_) if b ==0], [a for a,b in zip(diode,db.labels_) if b ==0], s=2, alpha = .2)
#plt.scatter([a for a,b in zip(ipm2,db.labels_) if b ==1], [a for a,b in zip(diode,db.labels_) if b ==1], s=2, alpha = .2)
#plt.scatter([a for a,b in zip(ipm2,db.labels_) if b ==2], [a for a,b in zip(diode,db.labels_) if b ==2], s=2, alpha = .2)