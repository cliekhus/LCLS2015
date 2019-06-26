"""
Find t0

"""

def find_t0_XAS(XOn, LOn, XEnergy, TimeTool, Ipm2Sum, Diode2, Filter, ploton):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from itertools import compress
    import math
    from pylab import exp
    from scipy.optimize import curve_fit
    
    XOn = list(compress(XOn, Filter))
    LOn = list(compress(LOn, Filter))
    XEnergy = list(compress(XEnergy, Filter))
    TimeTool = list(compress(TimeTool, Filter))
    Ipm2Sum = list(compress(Ipm2Sum, Filter))
    Diode2 = list(compress(Diode2, Filter))
    
    
    NumTTSteps_ES = 50
    
    TTDelay = [x*1000 for x in TimeTool]
    
    TTSteps = np.linspace(-1e3,1e3,NumTTSteps_ES+1)
    
    XES = []
    NumCounts = []
    DelayTime = []
    Peak1 = []
    Peak2 = []
    Intensity = []
    
    nancheck = [not a and not b for a,b in zip([math.isnan(sum(x)) for x in RowlandY], [math.isnan(x) for x in Ipm2Sum])]
    
    pickenergy = [x > 7116 and x < 7119 for x in XEnergy]
    
    OffFilter = [a and not b and c and d for a,b,c,d in zip(XOn, LOn, nancheck, pickenergy)]
    
    XESOff = list(compress(RowlandY, OffFilter))
    IntensityOff = list(compress(Ipm2Sum, OffFilter))
    
    XESOffNorm = list(sum(list([x/a for x,a in zip(XESOff, IntensityOff)])))
    
    for ii in range(len(TTSteps)-1):
        
        ttfilter = [a and b and c and d and e and f for a,b,c,d,e,f in zip(TTDelay >= TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn, nancheck, pickenergy)]
        #ttfilter = [a and b and c and d for a,b,c,d in zip(TTDelay > TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn)]
        numshots = sum([int(a) for a in ttfilter])
                
        if numshots > 0:
            xes = list(compress(RowlandY, ttfilter))
            intensity = list(compress(Ipm2Sum, ttfilter))
            #xesp = sum([x/a for x,a in zip(xes, intensity)])
            xesp = sum(xes)
            XES = XES + [xesp]
            numcounts = [sum([int(x) for x in ttfilter])]
            NumCounts = NumCounts + numcounts
            
            Intensity = Intensity + [sum(intensity)]
            DelayTime = DelayTime + [(TTSteps[ii]+TTSteps[ii+1])/2]
            #xespp = xesp[0]
            
            #Peak1 = Peak1 + [xesp[71]/sum(xesp)-XESOffNorm[71]/sum(XESOffNorm)]
            #Peak2 = Peak2 + [xesp[36]/sum(xesp)-XESOffNorm[36]/sum(XESOffNorm)]
            Peak2 = Peak2 + [sum(xesp)/numcounts]

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