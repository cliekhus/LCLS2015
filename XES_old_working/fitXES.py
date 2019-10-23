# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""

def fitXES(TCenters, XESDiffplus, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolved
    from fittingfunctions import combinedconvolved
    
    starta = 7
    startrate = 60
    startsig = 7
    startoffsetp = 2
    startoffsetm = -2
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiffplus, 'o')
        plt.plot(TCenters, convolved(TCenters, starta, startrate, startoffsetp, startt0, startsig))
        plt.plot(TCenters, XESDiffminus, 'o')
        plt.plot(TCenters, convolved(TCenters, -starta, startrate, startoffsetm, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(combinedconvolved, TCenters+TCenters, XESDiffplus+XESDiffminus, p0 = [starta, startrate, startoffsetp, -starta, startrate, startoffsetm, startt0, startsig])
    
    Fitp = convolved(TCenters, params[0], params[1], params[2], params[6], params[7])
    Fitm = convolved(TCenters, params[3], params[4], params[5], params[6], params[7])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiffplus, 'o')
        plt.plot(TCenters, Fitp)
        plt.plot(TCenters, XESDiffminus, 'x')
        plt.plot(TCenters, Fitm)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitp, Fitm, params, 'amplitude1, rate1, amplitude2, rate2, t0, instrument response'



















