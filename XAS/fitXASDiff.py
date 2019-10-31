# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""

def fitXASDiff(XEnergy, XASDiff, XASOff, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasdiff
    from fittingfunctions import xasoff
    
    sigA = 1 
    aA = .01
    x0Ap = 7112
    sigB = 1
    aB = .005
    x0B = 7114.1
    x0Bp = 7114.8
    sigC = 1
    aC = .01
    x0C = 7117.5
    x0Cp = 7118
    slope = 0.1
    offset = 0
    expamp = 0.1
    Amp = 0.004
    
    
    """
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigB,aB,x0B, sigC,aC,x0C, offset,slope,expamp))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasoff, XEnergy, XASDiff, p0 = [sigB,aB,x0B, sigC,aC,x0C, offset,slope,expamp])
    
    Fit = xasoff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')

"""
    

    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, xasdiff(XEnergy, Amp, sigA,x0Ap, sigB,x0B,x0Bp, sigC,x0C,x0Cp))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasdiff, XEnergy, XASDiff, p0 = [Amp, sigA,x0Ap, sigB,x0B,x0Bp, sigC,x0C,x0Cp])

    print(len(params))
    
    Fit = xasdiff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, Fit)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')

    return Fit, params, 'sigA,aA,x0Ap, sigB,aB,x0B,x0Bp, sigC,aC,x0C,x0Cp'



















