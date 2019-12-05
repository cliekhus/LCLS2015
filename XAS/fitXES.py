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

    return Fitp, Fitm, params, cov





def fitOneXES(TCenters, XESDiff, startt0, starta, startrate, startsig, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolved
    from fittingfunctions import convolvedzero
    import numpy as np
    
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiff, 'o')
        plt.plot(TCenters, convolvedzero(TCenters, starta, startrate, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(convolvedzero, TCenters, XESDiff, p0 = [starta, startrate, startt0, startsig])
    
    Fit = convolvedzero(TCenters, params[0], params[1], params[2], params[3])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, XESDiff, 'o')
        plt.plot(TCenters, Fit)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fit, params, cov




def fitXESwsine(TCentersplus, TCentersminus, XESDiffplus, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolvedsine
    from fittingfunctions import combinedconvolvedsine
    import numpy as np
    
    starta = .02
    startrate = 60
    startsig = 7
    startoffsetp = 0
    startoffsetm = 0
    startoscampp = 0.002
    startoscampm = -0.004
    startonset = 200
    startperiod = 240
    
    if ploton:

        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus, convolvedsine(TCentersplus, starta, startrate, startoffsetp, startt0, startsig, startoscampp, startperiod, startonset))
        plt.plot(TCentersminus, XESDiffminus, 'o')
        plt.plot(TCentersminus, convolvedsine(TCentersminus, -starta, startrate, startoffsetm, startt0, startsig, startoscampm, startperiod, startonset))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    
    params,cov = curve_fit(combinedconvolvedsine, np.concatenate((TCentersplus,TCentersminus)), np.concatenate((XESDiffplus,XESDiffminus)), \
                           p0 = [starta, -starta, startrate, startt0, startsig, startoscampp, startoscampm, startperiod, startonset])

    Fitp = convolvedsine(TCentersplus, params[0], params[2], 0, params[3], params[4], params[5], params[7], params[8])
    
    Fitm = convolvedsine(TCentersminus, params[1], params[2], 0, params[3], params[4], params[6], params[7], params[8])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersminus, Fitp)
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitm)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitp, Fitm, params, cov



def fitXESthree(TCentersplus, TCentersplus2, TCentersminus, XESDiffplus, XESDiffplus2, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolved
    from fittingfunctions import combinedconvolvedzerothree
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
        plt.plot(TCentersplus2, XESDiffplus2, 'o')
        plt.plot(TCentersplus2, convolved(TCentersplus2, starta, startrate, startoffsetp, startt0, startsig))
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(TCentersminus, convolved(TCentersminus, -starta, startrate, startoffsetm, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(combinedconvolvedzerothree, np.concatenate((TCentersplus,TCentersminus,TCentersplus2)), np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2)), p0 = [starta, -starta, startrate, startt0, startsig, starta])

    
    Fitp = convolved(TCentersplus, params[0], params[2], 0, params[3], params[4])
    Fitm = convolved(TCentersminus, params[1], params[2], 0, params[3], params[4])
    Fitp2 = convolved(TCentersplus2, params[5], params[2], 0, params[3], params[4])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersminus, Fitp)
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitm)
        plt.plot(TCentersplus2, XESDiffplus2, 'o')
        plt.plot(TCentersminus, Fitp2)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitp, Fitm, params, cov



def fitXESsinethree(TCentersplus, TCentersplus2, TCentersminus, XESDiffplus, XESDiffplus2, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolvedsine
    from fittingfunctions import combinedconvolvedsinethree
    import numpy as np

    starta = .02
    startrate = 80
    startsig = 30
    startoffsetp = 0
    startoffsetm = 0
    startoscampp = 0.002
    startoscampm = -0.00001
    startoscampp2 = 0.002
    startonset = 50
    startperiod = 300
    
    if ploton:

        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus, convolvedsine(TCentersplus, starta, startrate, startoffsetp, startt0, startsig, startoscampp, startperiod, startonset))
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(TCentersminus, convolvedsine(TCentersminus, -starta, startrate, startoffsetm, startt0, startsig, startoscampm, startperiod, startonset))
        plt.plot(TCentersplus2, XESDiffplus2, 'o')
        plt.plot(TCentersplus2, convolvedsine(TCentersplus2, starta, startrate, startoffsetp, startt0, startsig, startoscampp2, startperiod, startonset))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(combinedconvolvedsinethree, np.concatenate((TCentersplus,TCentersminus,TCentersplus2)), np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2)), \
                           p0 = [starta, -starta, startrate, startt0, startsig, startoscampp, startoscampm, startoscampp2, startperiod, startonset, starta])
    
    Fitp = convolvedsine(TCentersplus, params[0], params[2], 0, params[3], params[4], params[5], params[8], params[9])
    Fitm = convolvedsine(TCentersminus, params[1], params[2], 0, params[3], params[4], params[6], params[8], params[9])
    Fitp2 = convolvedsine(TCentersplus2, params[10], params[2], 0, params[3], params[4], params[7], params[8], params[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersminus, Fitp)
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitm, linestyle = '--')
        plt.plot(TCentersplus2, XESDiffplus2, 'o')
        plt.plot(TCentersminus, Fitp2, linestyle = ':')
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fitp, Fitm, params, cov






def fitXESsine(TCenters, Residual, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import offsetsine


    startoscamp = -0.01
    startonset = 500
    startperiod = 300
    
    if ploton:

        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, offsetsine(TCenters, startoscamp, startperiod, startonset))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(offsetsine, TCenters, Residual, p0 = [startoscamp, startperiod, startonset])
    
    Fit = offsetsine(TCenters, params[0], params[1], params[2])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, Fit)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fit, params, cov












