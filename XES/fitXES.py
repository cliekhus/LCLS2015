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





def fitXESthreeExtra(TCentersplus, TCentersplus2, TCentersminus, XESDiffplus, XESDiffplus2, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import convolved
    from fittingfunctions import combinedzerothreeexp
    from fittingfunctions import combinedconvolvedzerothree
    import numpy as np

    starta = .02
    startrate = 50
    startsig = 30
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
        plt.plot(TCentersminus, convolved(TCentersminus, -starta*.5, startrate*2, startoffsetm, startt0, startsig))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    #params,cov = curve_fit(combinedconvolvedzerothree, np.concatenate((TCentersplus,TCentersminus,TCentersplus2)), np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2)), p0 = [starta, -starta, startrate, startt0, startsig, starta])
    params,cov = curve_fit(combinedzerothreeexp, np.concatenate((TCentersplus,TCentersminus,TCentersplus2)), np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2)), p0 = [starta, -starta, startrate, startt0, startsig, starta, startrate*2, -starta*.5])
    
    Fitp = convolved(TCentersplus, params[0], params[2], 0, params[3], params[4])
    Fitm = convolved(TCentersminus, params[1], params[2], 0, params[3], params[4])
    Fitp2 = convolved(TCentersplus2, params[5], params[2], 0, params[3], params[4])
    Fitm2 = convolved(TCentersminus, params[7], params[6], 0, params[3], params[4])
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersminus, Fitp)
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitm)
        plt.plot(TCentersminus, Fitm2)
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










def fitXEScos2(TCenters, Residual, sigma, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import offsetcos2
    import numpy as np


    startoscamp = 0.01
    startonset = 150
    startperiod1 = 300
    startperiod2 = 133
    startbase = 0
    
    if ploton:

        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, offsetcos2(TCenters, startoscamp, startoscamp, startperiod1, startperiod2, startonset, startbase, sigma))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(lambda t,oscamp1,oscamp2,period1,period2,onset,base: \
                           offsetcos2(t,oscamp1,oscamp2,period1,period2,onset,base,sigma), TCenters, Residual, \
                           p0 = [startoscamp, startoscamp, startperiod1, startperiod2, startonset, startbase])
    cov = np.sqrt(np.diag(cov))
    
    time = np.linspace(min(TCenters), max(TCenters), 1000)
    
    params = np.append(params, sigma)
    Fit = offsetcos2(TCenters, *params)
    
    RR = Residual - Fit
    
    Fit = offsetcos2(time, *params)
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, Fit)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fit, time, params, cov, RR












def fitXESsine2(TCenters, Residual, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import offsetsine2
    import numpy as np


    startoscamp = 0.01
    startonset = 150
    startperiod1 = 300
    startperiod2 = 133
    startbase = 0
    
    if ploton:

        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, offsetsine2(TCenters, startoscamp, startoscamp, startperiod1, startperiod2, startonset, startbase))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(offsetsine2, TCenters, Residual, p0 = [startoscamp, startoscamp, startperiod1, startperiod2, startonset, startbase])
    cov = np.sqrt(np.diag(cov))
    
    time = np.linspace(min(TCenters), max(TCenters), 1000)
    
    Fit = offsetsine2(TCenters, *params)
    
    RR = Residual - Fit
    
    Fit = offsetsine2(time, *params)
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, Fit)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fit, time, params, cov, RR










def fitXESsine(TCenters, Residual, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import offsetsine
    import numpy as np


    startoscamp = 0.01
    startonset = 150
    startperiod = 300
    startbase = 0
    
    if ploton:

        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, offsetsine(TCenters, startoscamp, startperiod, startonset, startbase))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    

    params,cov = curve_fit(offsetsine, TCenters, Residual, p0 = [startoscamp, startperiod, startonset, startbase])
    cov = np.sqrt(np.diag(cov))
    
    time = np.linspace(min(TCenters), max(TCenters), 1000)
    
    Fit = offsetsine(TCenters, *params)
    
    RR = Residual - Fit
    
    Fit = offsetsine(time, *params)
    
    if ploton:
            
        plt.figure()
        plt.plot(TCenters, Residual, 'o')
        plt.plot(TCenters, Fit)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return Fit, time, params, cov, RR






def fitXESGlobal_setBET(TCentersplus, TCentersplus2, TCentersminus, XESDiffplus, XESDiffplus2, XESDiffminus, startt0, BET, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import globalconvolved
    from fittingfunctions import globalfit
    from fittingfunctions import globalfitsimple
    from fittingfunctions import halffit
    import numpy as np
    import math

    starta = .02
    startrate = 50
    startsig = 30
    startoffsetp = 0
    startoffsetm = 0
    ampfactor = 0.5
    ratefactor = 2
    
    if ploton:

        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(TCentersplus, globalconvolved(TCentersplus, startt0, startsig, starta, startrate, startoffsetp))
        plt.plot(TCentersplus, globalconvolved(TCentersplus, startt0, startsig, starta*ampfactor, startrate*ratefactor, startoffsetp))
        plt.plot(TCentersminus, globalconvolved(TCentersminus, startt0, startsig, -starta, startrate, startoffsetm))
        plt.plot(TCentersminus, globalconvolved(TCentersminus, startt0, startsig, -starta*ampfactor, startrate*ratefactor, startoffsetm))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    
    times = np.concatenate((TCentersplus,TCentersminus,TCentersplus2))
    ys = np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2))
    tt = np.linspace(min(times), max(times), 1000)


    params,cov = curve_fit(lambda t, t0, sig, a11, a21, a31, a12, a22, a32, rate2: \
                           globalfit(t, t0, sig, a11, a21, a31, BET, a12, a22, a32, rate2), times, ys, \
                           p0 = [startt0, startsig, starta, -starta, starta, starta*ampfactor, -starta*ampfactor, starta*ampfactor, startrate*ratefactor])
    cov = np.sqrt(np.diag(cov))
    
#    Rsquared = 1-(np.sum((ys - globalfit(times, *params))**2) / np.sum((ys - np.mean(globalfit(times, *params)))**2))
#    print('Rsquared for global with fixed BET ' + str(Rsquared))
    print('global fit with fixed BET')
    print('BET = ' + str(BET) + ' fs')
    print('IRF = ' + str(int(params[1]*2*math.sqrt(2*math.log(2)))) + ' $\pm$ ' + str(int(cov[1]*2*math.sqrt(2*math.log(2)))) + ' fs')
    print('LD = ' + str(int(params[8])) + ' $\pm$ ' + str(int(cov[8])) + ' fs')
    print('Ap1 = ' + str(params[2]) + ' $\pm$ ' + str(cov[2]) + ' fs')
    print('Ap2 = ' + str(params[3]) + ' $\pm$ ' + str(cov[3]) + ' fs')
    print('Ap3 = ' + str(params[4]) + ' $\pm$ ' + str(cov[4]) + ' fs')
    print('Bp1 = ' + str(params[5]) + ' $\pm$ ' + str(cov[5]) + ' fs')
    print('Bp2 = ' + str(params[6]) + ' $\pm$ ' + str(cov[6]) + ' fs')
    print('Bp3 = ' + str(params[7]) + ' $\pm$ ' + str(cov[7]) + ' fs')
    
    if ploton:
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[2], BET, 0)) + np.array(globalconvolved(tt, params[0], params[1], params[5], params[8], 0)), label = '2')
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[3], BET, 0)) + np.array(globalconvolved(tt, params[0], params[1], params[6], params[8], 0)), label = '3')
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[4], BET, 0)) + np.array(globalconvolved(tt, params[0], params[1], params[7], params[8], 0)), label = '4')
        plt.title('two exponentials')
        plt.legend()



    return params, cov








def fitXESGlobal(TCentersplus, TCentersplus2, TCentersminus, XESDiffplus, XESDiffplus2, XESDiffminus, startt0, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import globalconvolved
    from fittingfunctions import globalfit
    from fittingfunctions import globalfitsimple
    from fittingfunctions import halffit
    import numpy as np
    import math

    starta = .02
    startrate = 50
    startsig = 30
    startoffsetp = 0
    startoffsetm = 0
    ampfactor = 0.5
    ratefactor = 2
    
    if ploton:

        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(TCentersplus, globalconvolved(TCentersplus, startt0, startsig, starta, startrate, startoffsetp))
        plt.plot(TCentersplus, globalconvolved(TCentersplus, startt0, startsig, starta*ampfactor, startrate*ratefactor, startoffsetp))
        plt.plot(TCentersminus, globalconvolved(TCentersminus, startt0, startsig, -starta, startrate, startoffsetm))
        plt.plot(TCentersminus, globalconvolved(TCentersminus, startt0, startsig, -starta*ampfactor, startrate*ratefactor, startoffsetm))
        plt.title('start parameters')
        plt.xlabel('time (fs)')
    
    times = np.concatenate((TCentersplus,TCentersminus,TCentersplus2))
    ys = np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2))
    tt = np.linspace(min(times), max(times), 1000)


    params,cov = curve_fit(globalfit, times, ys, \
                           p0 = [startt0, startsig, starta, -starta, starta, startrate, starta*ampfactor, -starta*ampfactor, starta*ampfactor, startrate*ratefactor])
    cov = np.sqrt(np.diag(cov))
    
    
    Rsquared = 1-(np.sum((ys - globalfit(times, *params))**2) / np.sum((ys - np.mean(globalfit(times, *params)))**2))
    print('Rsquared for global ' + str(Rsquared))
    print('BET = ' + str(int(params[5])) + ' $\pm$ ' + str(int(cov[5])) + ' fs')
    print('IRF = ' + str(int(params[1]*2*math.sqrt(2*math.log(2)))) + ' $\pm$ ' + str(int(cov[1]*2*math.sqrt(2*math.log(2)))) + ' fs')
    print('LD = ' + str(int(params[9])) + ' $\pm$ ' + str(int(cov[9])) + ' fs')
    print('Ap1 = ' + str(params[2]) + ' $\pm$ ' + str(cov[2]) + ' fs')
    print('Ap2 = ' + str(params[3]) + ' $\pm$ ' + str(cov[3]) + ' fs')
    print('Ap3 = ' + str(params[4]) + ' $\pm$ ' + str(cov[4]) + ' fs')
    print('Bp1 = ' + str(params[6]) + ' $\pm$ ' + str(cov[6]) + ' fs')
    print('Bp2 = ' + str(params[7]) + ' $\pm$ ' + str(cov[7]) + ' fs')
    print('Bp3 = ' + str(params[8]) + ' $\pm$ ' + str(cov[8]) + ' fs')
    
    if ploton:
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[2], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[6], params[9], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[3], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[7], params[9], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[4], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[8], params[9], 0)))
        plt.title('two exponentials')

    paramshalf,covhalf = curve_fit(halffit, times, ys, \
                           p0 = [startt0, startsig, starta, -starta, starta, startrate, -starta*ampfactor, startrate*ratefactor])
    covhalf = np.sqrt(np.diag(covhalf))
    
    Rsquared = 1-(np.sum((ys - halffit(times, *paramshalf))**2) / np.sum((ys - np.mean(halffit(times, *paramshalf)))**2))
    print('Rsquared for half ' + str(Rsquared))
    print('BET = ' + str(int(paramshalf[5])) + ' $\pm$ ' + str(int(covhalf[5])) + ' fs')
    print('IRF = ' + str(int(paramshalf[1]*2*math.sqrt(2*math.log(2)))) + ' $\pm$' + str(int(covhalf[1]*2*math.sqrt(2*math.log(2)))) + ' fs')
    print('LD = ' + str(int(paramshalf[7])) + ' $\pm$ ' + str(int(covhalf[7])) + ' fs')
    
    if ploton:
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(tt, np.array(globalconvolved(tt, paramshalf[0], paramshalf[1], paramshalf[2], paramshalf[5], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramshalf[0], paramshalf[1], paramshalf[3], paramshalf[5], 0)) + np.array(globalconvolved(tt, paramshalf[0], paramshalf[1], paramshalf[6], paramshalf[7], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramshalf[0], paramshalf[1], paramshalf[4], paramshalf[5], 0)))
        plt.title('half exponentials')

    paramssimple,covsimple = curve_fit(globalfitsimple, np.concatenate((TCentersplus,TCentersminus,TCentersplus2)), np.concatenate((XESDiffplus,XESDiffminus,XESDiffplus2)), \
                           p0 = [startt0, startsig, starta, -starta, starta, startrate])
    covsimple = np.sqrt(np.diag(covsimple))
    
    Rsquared = 1-(np.sum((ys - globalfitsimple(times, *paramssimple))**2) / np.sum((ys - np.mean(globalfitsimple(times, *paramssimple)))**2))
    print('Rsquared for simpleglobal ' + str(Rsquared))
    print('BET = ' + str(int(paramssimple[5])) + ' $\pm $ ' + str(int(covsimple[5])) + ' fs')
    print('IRF = ' + str(int(paramssimple[1]*2*math.sqrt(2*math.log(2)))) + ' $\pm $' + str(int(covsimple[1]*2*math.sqrt(2*math.log(2)))) + ' fs')
    
    if ploton:
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[2], paramssimple[5], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[3], paramssimple[5], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[4], paramssimple[5], 0)))
        plt.title('one exponential')

    
    if ploton:
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersminus, XESDiffminus, 'x')
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[2], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[6], params[9], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[3], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[7], params[9], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, params[0], params[1], params[4], params[5], 0)) + np.array(globalconvolved(tt, params[0], params[1], params[8], params[9], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[2], paramssimple[5], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[3], paramssimple[5], 0)))
        plt.plot(tt, np.array(globalconvolved(tt, paramssimple[0], paramssimple[1], paramssimple[4], paramssimple[5], 0)))
        
    
    Fitp1 = globalconvolved(TCentersplus, params[0], params[1], params[2], params[5], 0)
    Fitm1 = globalconvolved(TCentersminus, params[0], params[1], params[3], params[5], 0)
    Fitp21 = globalconvolved(TCentersplus2, params[0], params[1], params[4], params[5], 0)
    Fitp2 = globalconvolved(TCentersminus, params[0], params[1], params[6], params[9], 0)
    Fitm2 = globalconvolved(TCentersminus, params[0], params[1], params[7], params[9], 0)
    Fitp22 = globalconvolved(TCentersminus, params[0], params[1], params[8], params[9], 0)
    
    if ploton:
            
        plt.figure()
        plt.plot(TCentersplus, XESDiffplus, 'o')
        plt.plot(TCentersplus2, XESDiffplus2, 's')
        plt.plot(TCentersplus, XESDiffminus, 'x')
        plt.plot(TCentersminus, Fitp1)
        plt.plot(TCentersminus, Fitm1)
        plt.plot(TCentersminus, Fitp21)
        plt.plot(TCentersminus, Fitp2)
        plt.plot(TCentersminus, Fitm2)
        plt.plot(TCentersminus, Fitp22)
        plt.title('end parameters')
        plt.xlabel('time (fs)')

    return params, cov, paramshalf, covhalf, paramssimple, covsimple



