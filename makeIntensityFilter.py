# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:47 2019

@author: chelsea
"""

def makeDiodeFilter(ipm2, diode, xOn, lOn, slope, slopemedian, slopestd, ploton):
    
    from pylab import exp
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    from itertools import compress
    import numpy as np
    
    xonfilter = [a>0 and b for a,b in zip(slope,xOn)]
    
    if ploton:
            
        plt.figure()
        plt.scatter(list(compress(diode, xonfilter)),list(compress(slope, xonfilter)),s=2)
    
    numstds = 5
    
    slopefilter = [abs(a-c) < numstds*d and b for a,b,c,d in zip(slope,xonfilter,slopemedian, slopestd)]
    
    if ploton:
            
        plt.scatter(list(compress(diode, slopefilter)),list(compress(slope,slopefilter)),s=2)
        plt.xlabel('diode')
        plt.ylabel('slope')
        
        plt.figure()
        plt.scatter(ipm2,diode,s=2)
        plt.scatter(list(compress(ipm2, slopefilter)), list(compress(diode, slopefilter)),s=2)
        plt.xlabel('ipm2')
        plt.ylabel('diode')
    
    slopefiltered = list(compress(slope,slopefilter))
    
    if ploton:
            
        plt.figure()
        plt.hist(slopefilter, 2000)
    slopehist = np.histogram(slopefiltered,2000)
    
    if ploton:
        plt.xlabel('slope')
        plt.ylabel('counts')
    
    slopes = slopehist[1]
    slopes = slopes[1:]
    
    def gauss(x,a,x0,sig):
        return a*exp(-(x-x0)**2/2/sig**2)
    
    def gausfit(x,a0,x00,sig0,a1,x01,sig1,a2,x02,sig2):
        return gauss(x,a0,x00,sig0) + gauss(x,a1,x01,sig1) + gauss(x,a2,x02,sig2)
    
    params,cov = curve_fit(gausfit,slopes,slopehist[0],p0 = [100*max(slopehist[0])/116,.04,.01,60*max(slopehist[0])/116,.06,.01,30*max(slopehist[0])/116,.12,.01])
    #print('this is fake data mode')
    #params = np.array([1,1,1,2,2,2,3,3,3])
    if ploton:
        plt.plot(slopes,gausfit(slopes,*params))
    
    a0fit = [params[0],params[3],params[6]]
    x0fit = [params[1],params[4],params[7]]
    sigfit = [params[2],params[5],params[8]]
    
    paramssorted = sorted(zip(x0fit,a0fit,sigfit))
    
    gauss0 = gauss(slope,paramssorted[0][1],paramssorted[0][0],paramssorted[0][2])
    gauss1 = gauss(slope,paramssorted[1][1],paramssorted[1][0],paramssorted[1][2])
    gauss2 = gauss(slope,paramssorted[2][1],paramssorted[2][0],paramssorted[2][2])
    
    if ploton:
            
        plt.figure()
        plt.scatter(slope, gauss0)
        plt.scatter(slope, gauss1)
        plt.scatter(slope, gauss2)
        plt.title('fits to slope peaks')
    
    gaussamp = 20
    
    gaussfilter = [bool(x > paramssorted[0][1]/gaussamp or y > paramssorted[1][1]/gaussamp or z > paramssorted[2][1]/gaussamp and a) for x,y,z,a in zip(gauss0, gauss1, gauss2, slopefilter)]
    
    #gaussfilter = [True for x in diode]
    
    #gaussfilter = [x>y and x>z and a for x,y,z,a in zip(desiredgauss,closegauss1,closegauss2,slopefilter)]
    
    #gaussfilter = slopefilter
    
    if ploton:
            
        plt.figure()
        plt.scatter(ipm2,diode,s=2)
        plt.scatter(list(compress(ipm2, gaussfilter)), list(compress(diode, gaussfilter)), s=2)
        plt.xlabel('ipm2')
        plt.ylabel('diode')
    
    return gaussfilter
