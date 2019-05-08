"""
Find t0

"""

def find_t0_XAS(XASDiff, TTSteps, OutEnergy):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from itertools import compress
    import math
    from pylab import exp
    from scipy.optimize import curve_fit
    
    pickenergy = [x > 7116 and x < 7119 for x in XEnergy]
    
    
    
    
    if ploton:
            
        plt.figure()
        plt.plot(XESOffNorm)
        plt.xlabel('rowland pixel')
        plt.ylabel('signal')
    
    def gauss(x,a,x0,sig):
        return a*exp(-(x-x0)**2/2/sig**2)
    
    if ploton:
            
        plt.figure()
        plt.plot(Intensity)
        plt.title('Intensity over time')
        
        plt.figure()
        plt.plot(DelayTime, Peak1, marker='.')
    params,cov = curve_fit(gauss,DelayTime, Peak1, p0 = [max(Peak1), -70, 100])
    if ploton:
        plt.plot(DelayTime,gauss(DelayTime,*params))
        plt.xlabel('Delay Time')
        plt.ylabel('fit peak 1')
    
    
    meanx0 = params[1]
    
    if ploton:
        plt.figure()
        plt.plot(DelayTime, Peak2, marker='.')
    params,cov = curve_fit(gauss,DelayTime, Peak2, p0 = [max(Peak2), -70, 100])
    if ploton:    
        plt.plot(DelayTime, gauss(DelayTime,*params))
        plt.xlabel('Delay Time')
        plt.ylabel('fit peak 2')
        
        plt.figure()
        plt.pcolor(XES)
    
    meanx0 = (meanx0+params[1])/2
    
    return meanx0