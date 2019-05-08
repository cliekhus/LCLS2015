"""
Find t0

"""

def find_t0_XAS(XOn, LOn, XEnergy, TimeTool, Ipm2Sum, RowlandY, Filter, ploton):
    
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
    RowlandY = list(compress(RowlandY, Filter))
    
    
    NumTTSteps_ES = 200
    
    TTDelay = [x*1000 for x in TimeTool]
    
    TTSteps = np.linspace(-1e3,1e3,NumTTSteps_ES+1)
    
    XES = []
    NumCounts = []
    DelayTime = []
    Peak1 = []
    Peak2 = []
    Intensity = []
    
    nancheck = [not a and not b for a,b in zip([math.isnan(sum(x)) for x in RowlandY], [math.isnan(x) for x in Ipm2Sum])]
    
    pickenergy = [x > 0 for x in XEnergy]
    
    for ii in range(len(TTSteps)-1):
        
        ttfilter = [a and b and c and d and e and f for a,b,c,d,e,f in zip(TTDelay >= TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn, nancheck, pickenergy)]
        #ttfilter = [a and b and c and d for a,b,c,d in zip(TTDelay > TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn)]
        numshots = sum([int(a) for a in ttfilter])
                
        if numshots > 0:
            xes = [sum(list(compress(RowlandY, ttfilter)))]
            XES = XES + xes
            NumCounts = NumCounts + [sum([int(x) for x in ttfilter])]
            intensity = sum(list(compress(Ipm2Sum, ttfilter)))
            Intensity = Intensity + [intensity]
            DelayTime = DelayTime + [(TTSteps[ii]+TTSteps[ii+1])/2]
            xesp = xes[0]
            Peak1 = Peak1 + [xesp[71]]
            Peak2 = Peak2 + [xesp[36]]

    ttfilteroff = [a and not b and c and d for a,b,c,d in zip(XOn, LOn, nancheck, pickenergy)]
    
    if ploton:
            
        plt.figure()
        plt.plot(sum(list(compress(RowlandY, ttfilteroff))))
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
    
    meanx0 = (meanx0+params[1])/2
    
    return meanx0