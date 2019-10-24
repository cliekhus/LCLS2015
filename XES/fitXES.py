# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""

def fitXES(TCentersplus, TCentersminus, XESDiffplus, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolved
    from fittingfunctions import combinedconvolvedzero
    import numpy as np
    
    starta = .02
    startrate = 60
    startsig = 7
    startoffsetp = 0
    startoffsetm = 0
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus, convolved(TCentersplus, starta, startrate, startoffsetp, startt0, startsig))
        plt.plot(TCentersminus, XESDiffminus, 'o')
        plt.plot(TCentersminus, convolved(TCentersminus, -starta, startrate, startoffsetm, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(combinedconvolvedzero, np.concatenate((TCentersplus,TCentersminus)), np.concatenate((XESDiffplus,XESDiffminus)), p0 = [starta, -starta, startrate, startt0, startsig])
    
    Fitp = convolved(TCentersplus, params[0], params[2], 0, params[3], params[4])
    Fitm = convolved(TCentersminus, params[1], params[2], 0, params[3], params[4])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersminus, Fitp)
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitm)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitp, Fitm, params, 'amplitude1, rate1, amplitude2, rate2, t0, instrument response'



















