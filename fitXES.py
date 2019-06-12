# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""

def fitXES(TCenters, XESDiffplus, XESDiffminus, ploton):
    
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from scipy.special import erf
    
    
    def gauss(t,sig):
        return [math.exp(-(tt)**2/2/sig**2) for tt in t]
    
    
    
    def expdecay(a,t,t0,rate):
        
        out = []
        
        for ii in range(len(t)):
            if t[ii] < t0:
                out = out + [0]
            else:
                out = out + [a*math.exp(-(t[ii]-t0)/rate)]
            
        return out
    
    
    
    def convolved(t, a, rate, t0, sig):
        
        gout = gauss(t, sig)
        eout = expdecay(a, t, t0, rate)
        out = np.convolve(gout, eout, mode='full')
        times = np.linspace(2*min(t), 2*max(t)-2, len(t)*2)
        out = [x for x,y in zip(out,times) if y <= max(t) and y >= min(t)]
        
        return out
    
    
    
    def convolvednew(t,a,rate,t0,sig):
        
        out = [a*(sig/rate-(tt-t0)/sig)*math.exp(-(tt-t0)/rate) for tt in t]
        
        return out
    
    
    starta = 10
    startrate = 60
    startt0 = -30
    startsig = 7
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiffplus, 'o')
        plt.plot(TCenters, convolved(TCenters, starta, startrate, startt0, startsig))
        plt.plot(TCenters, XESDiffminus, 'o')
        plt.plot(TCenters, convolved(TCenters, -starta, startrate, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    
    
    
    def combinedconvolved(t, a1, rate1, a2, rate2, t0, sig):
                
        tfirst = t[0:int(len(t)/2)]
        out1 = convolved(tfirst, a1,rate1,t0,sig)
        
        tsecond = t[int(len(t)/2):]
        out2 = convolved(tsecond, a2, rate2, t0, sig)
        
        return out1+out2
        
    
    params,cov = curve_fit(combinedconvolved, TCenters+TCenters, XESDiffminus+XESDiffplus, p0 = [-starta, startrate, starta, startrate, startt0, startsig])
    
    Fitminus = convolved(TCenters, params[0], params[1], params[4], params[5])
    Fitplus = convolved(TCenters, params[2], params[3], params[4], params[5])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiffminus, 'o')
        plt.plot(TCenters, Fitminus)
        plt.plot(TCenters, XESDiffplus, 'x')
        plt.plot(TCenters, Fitplus)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitminus, Fitplus, params, 'amplitude1, rate1, amplitude2, rate2, t0, instrument response'



















