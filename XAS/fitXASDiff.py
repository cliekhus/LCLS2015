# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""





def fitXASPiecewiseGauss(XEnergy, XASDiff, XASOff, XASOn, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasoff
    from fittingfunctions import lor
    from fittingfunctions import gauswslope
    import numpy as np
    

    sigAS = .3
    AS = 65.3
    x0ApS = 7111.9
    sigBS = .1
    sigBpS = .558
    BS = 125.4
    x0BS = 7113
    x0BpS = 7114.18
    sigCS = 2
    CS = 1012
    x0CS = 7115.6
    erfslopeS = 3
    offsetS = 1342
    erfampS = 849
    peakS = 7117.4
    offAS = 179181
    offBS = 331401
    slopeSA = -25.2
    slopeSB = -46.6
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
        plt.plot(XEnergy, lor(XEnergy,sigBS,x0BS,BS))
        plt.plot(XEnergy, lor(XEnergy,sigCS,x0CS,CS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasoff, XEnergy, XASOff, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
    
    
    Fit = xasoff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.plot(XEnergy, lor(XEnergy,params[0],params[2],params[1]))
        plt.plot(XEnergy, lor(XEnergy,params[3],params[5],params[4]))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
        
        
        
        
        
    xenergyAL = 7108
    xenergyAH = 7113.5
    xenergyBL = 7112.5
    xenergyBH = 7115.5
    Achoice = np.logical_and(XEnergy<xenergyAH, XEnergy >xenergyAL)
    Bchoice = np.logical_and(XEnergy > xenergyBL, XEnergy < xenergyBH)   
    
    
    
    
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy[Achoice], gauswslope(XEnergy[Achoice], sigAS,x0ApS,AS,offAS,slopeSA))
        plt.plot(XEnergy[Bchoice], gauswslope(XEnergy[Bchoice], sigBpS,x0BpS,BS,offBS,slopeSB))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        


    paramsa,cova = curve_fit(gauswslope, XEnergy[Achoice], XASDiff[Achoice], p0 = [sigAS,x0ApS,AS,offAS,slopeSA])
    
    FitA = gauswslope(XEnergy, paramsa[0], paramsa[1], paramsa[2], paramsa[3], paramsa[4])

    paramsb,covb = curve_fit(gauswslope, XEnergy[Bchoice], XASDiff[Bchoice], p0 = [sigBpS,x0BpS,BS,offBS,slopeSB])

    FitB = gauswslope(XEnergy, paramsb[0], paramsb[1], paramsb[2], paramsb[3], paramsb[4])
    

    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, FitA)
        plt.plot(XEnergy, FitB)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
    

    return Fit, params, paramsa, paramsb, cova, covb























###############################################################################
    #Old fit functions no need to look further :P

















def fitXASDiff(XEnergy, XASDiff, XASOff, XASOn, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasdiff
    from fittingfunctions import xasoff
    from fittingfunctions import lor
    from fittingfunctions import gauss
    from fittingfunctions import gauswslope
    import numpy as np
    
    if False:
        sigAS = 10
        AS = 0.001
        x0ApS = 7112.3
        sigBS = 1.7
        sigBpS = 1.6
        BS = 0.017
        BpS = 0.016
        x0BS = 7114.22
        x0BpS = 7114.22
        sigCS = 3
        sigCpS = 3
        CS = 0.04
        CpS = 0.04
        x0CS = 7116
        x0CpS = 7116.02
        erfslopeS = 2.5
        offsetS = 0.07
        erfampS = 0.04
        peakS = 7118.3
        EFS = 0.25
    
    else:
        sigAS = .2
        AS = 30
        x0ApS = 7112
        sigBS = .5
        sigBpS = .6
        BS = 389
        BpS = 300
        x0BS = 7113
        x0BpS = 7114.1
        sigCS = 2
        sigCpS = 2
        CS = 1012
        CpS = 750
        x0CS = 7115.6
        x0CpS = 7118.2
        erfslopeS = 3
        offsetS = 1342
        erfampS = 849
        peakS = 7117.4
        EFS = 4
        #slopeS = -12
        #offS = 85316
        offS = -33
        slopeS = 0
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
        plt.plot(XEnergy, gauss(XEnergy,sigBS,x0BS,BS))
        plt.plot(XEnergy, gauss(XEnergy,sigCS,x0CS,CS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasoff, XEnergy, XASOff, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
    
    Fit = xasoff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.plot(XEnergy, gauss(XEnergy,params[0],params[2],params[1]))
        plt.plot(XEnergy, gauss(XEnergy,params[3],params[5],params[4]))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
        
        
        
        
        
        
        
    linparams = np.polyfit(XEnergy[np.logical_and(XEnergy < 7114.8, XEnergy > 7110.2)], XASDiff[np.logical_and(XEnergy < 7114.8, XEnergy > 7110.2)], 1)

        
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        #plt.plot(XEnergy, xasdiff(XEnergy, AS,sigAS,x0ApS, params[1],BpS,params[0],sigBpS,params[2],x0BpS, params[4],CpS,params[3],sigCpS,params[5],x0CpS, EFS,linparams[1],linparams[0]))
        plt.plot(XEnergy, xasdiff(XEnergy, params[1],BpS,params[0],sigBpS,params[2],x0BpS, EFS,offS, slopeS))
        plt.plot(XEnergy, gauss(XEnergy, sigAS, x0ApS, AS))
        plt.plot(XEnergy, gauss(XEnergy, params[0], params[2], params[1]))
        plt.plot(XEnergy, gauss(XEnergy, sigBpS, x0BpS, BpS))
        #plt.plot(XEnergy, gauss(XEnergy, params[3], params[5], params[4]))
        #plt.plot(XEnergy, gauss(XEnergy, sigCpS, x0CpS, CpS))
        #plt.plot(XEnergy, linparams[1]+linparams[0]*XEnergy)
        plt.title('start parameters')
        plt.xlabel('energy (eV)')


    paramsA,cov = curve_fit(gauswslope, XEnergy[np.logical_and(XEnergy < 7113.3, XEnergy > 7110.2)], \
                                XASDiff[np.logical_and(XEnergy < 7113.3, XEnergy > 7110.2)], p0 = [AS,sigAS,x0ApS, offS,slopeS])
    
    paramsB,cov = curve_fit(gauswslope, XEnergy[np.logical_and(XEnergy < 7115, XEnergy > 7113)], \
                                XASDiff[np.logical_and(XEnergy < 7115, XEnergy > 7113)], p0 = [BpS,sigBpS,x0BpS, offS,slopeS])


    paramsdiff,cov = curve_fit(lambda XEnergy, EF, off: \
                               xasdiff(XEnergy[np.logical_and(XEnergy < 7115, XEnergy > 7112.3)], params[1],paramsB[0],params[0],paramsB[1],params[2],paramsB[2], EF,off,0), \
                               XEnergy[np.logical_and(XEnergy < 7115, XEnergy > 7112.3)], XASDiff[np.logical_and(XEnergy < 7115, XEnergy > 7112.3)], \
                           p0 = [EFS,offS])

    
    #paramsA,cov = curve_fit(gauss, XEnergy[XEnergy < 7113.3], XASDiff[XEnergy < 7113.3], p0 = [sigAS,x0ApS,AS])
    """
    paramsA,cov = curve_fit(lambda XEnergy, A,sigA,x0A: \
                               gauswslope(XEnergy[np.logical_and(XEnergy < 7113.3, XEnergy > 7110.2)], sigA, x0A, A, linparams[1],linparams[0]), \
                               XEnergy[np.logical_and(XEnergy < 7113.3, XEnergy > 7110.2)], XASDiff[np.logical_and(XEnergy < 7113.3, XEnergy > 7110.2)], \
                           p0 = [AS,sigAS,x0ApS])

    paramsdiff,cov = curve_fit(lambda XEnergy, Bp,sigBp,x0Bp, EF: \
                               xasdiff(XEnergy[np.logical_and(XEnergy < 7114.8, XEnergy > 7112)], paramsA[0],paramsA[1],paramsA[2], params[1],Bp,params[0],sigBp,params[2],x0Bp, EF,linparams[1],linparams[0]), \
                               XEnergy[np.logical_and(XEnergy < 7114.8, XEnergy > 7112)], XASDiff[np.logical_and(XEnergy < 7114.8, XEnergy > 7112)], \
                           p0 = [BpS,sigBpS,x0BpS, EFS])
    """
    print('params')
    print(paramsA)
    print(paramsB)
    print('endparams')
    #Fit = xasdiff(XEnergy, paramsA[0],paramsA[1],paramsA[2], params[1],paramsdiff[0],params[0],paramsdiff[1],params[2],paramsdiff[2], \
    #              paramsdiff[3], linparams[1],linparams[0])
    Fit = xasdiff(XEnergy, params[1],paramsB[0],params[0],paramsB[1],params[2],paramsB[2], \
                  paramsdiff[0], paramsdiff[1],0)

    """
    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp, EF: \
                               xasdiff(XEnergy, paramsA[0],paramsA[1],paramsA[2], params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp, EF,linparams[1],linparams[0]), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS, EFS])

    
    Fit = xasdiff(XEnergy, paramsA[0],paramsA[1],paramsA[2], params[1],paramsdiff[0],params[0],paramsdiff[1],params[2],paramsdiff[2], \
                  params[4],paramsdiff[3],params[3],paramsdiff[4],params[5],paramsdiff[5], paramsdiff[9], linparams[1],linparams[0])

    """
    """
    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp, EF: \
                               xasdiff(XEnergy, A,sigA,x0Ap, params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp, EF,linparams[1],linparams[0]), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS, EFS])

    
    Fit = xasdiff(XEnergy, paramsdiff[0],paramsdiff[1],paramsdiff[2], params[1],paramsdiff[3],params[0],paramsdiff[4],params[2],paramsdiff[5], \
                  params[4],paramsdiff[6],params[3],paramsdiff[7],params[5],paramsdiff[8], paramsdiff[9], linparams[1],linparams[0])
    """
    """
    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp: \
                               xasdiff(XEnergy, A,sigA,x0Ap, params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS])

    
    Fit = xasdiff(XEnergy, paramsdiff[0],paramsdiff[1],paramsdiff[2], params[1],paramsdiff[3],params[0],paramsdiff[4],params[2],paramsdiff[5], \
                  params[4],paramsdiff[6],params[3],paramsdiff[7],params[5],paramsdiff[8])
    """
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, Fit)
        #plt.plot(XEnergy, gauswslope(XEnergy, paramsA[0], paramsA[1], paramsA[2], paramsA[3],paramsA[4]))
        plt.plot(XEnergy, gauss(XEnergy, paramsA[1], paramsA[2], paramsA[0]))
        #plt.plot(XEnergy, gauss(XEnergy, params[0], params[2], params[1]))
        #plt.plot(XEnergy, gauswslope(XEnergy,paramsB[0],paramsB[1],paramsB[2],paramsB[3],paramsB[4]))
        plt.plot(XEnergy, gauss(XEnergy, paramsB[1], paramsB[2], paramsB[0]))
        #plt.plot(XEnergy, gauss(XEnergy,paramsdiff[4],paramsdiff[5],abs(paramsdiff[3])))
        #plt.plot(XEnergy, lor(XEnergy,paramsdiff[7],paramsdiff[8],abs(paramsdiff[6])))
        #plt.plot(XEnergy, linparams[1]+linparams[0]*XEnergy)
        #plt.plot(XEnergy, paramsdiff[4]+paramsdiff[5]*XEnergy)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
    

    return Fit, params, paramsdiff, cov, 'sigA,aA,x0Ap, sigB,aB,x0B,x0Bp, sigC,aC,x0C,x0Cp'







def fitXASPiecewiseDiff(XEnergy, XASDiff, XASOff, XASOn, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasdiff
    from fittingfunctions import xasoff
    from fittingfunctions import lor
    from fittingfunctions import lorwoff
    from fittingfunctions import xas2diff
    import numpy as np
    
    if False:
        sigAS = 10
        AS = 0.001
        x0ApS = 7112.3
        sigBS = 1.7
        sigBpS = 1.6
        BS = 0.017
        BpS = 0.016
        x0BS = 7114.22
        x0BpS = 7114.22
        sigCS = 3
        sigCpS = 3
        CS = 0.04
        CpS = 0.04
        x0CS = 7116
        x0CpS = 7116.02
        erfslopeS = 2.5
        offsetS = 0.07
        erfampS = 0.04
        peakS = 7118.3
    
    else:
        sigAS = .2
        AS = 100
        x0ApS = 7111.8
        sigBS = .1
        sigBpS = .12
        BS = 389
        BpS = 389
        x0BS = 7113
        x0BpS = 7114
        sigCS = 2
        sigCpS = 2
        CS = 1012
        CpS = 1012
        x0CS = 7115.6
        x0CpS = 7115.7
        erfslopeS = 3
        offsetS = 1342
        erfampS = 849
        peakS = 7117.4
        offAS = 0
        offBS = -37
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
        plt.plot(XEnergy, lor(XEnergy,sigBS,x0BS,BS))
        plt.plot(XEnergy, lor(XEnergy,sigCS,x0CS,CS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasoff, XEnergy, XASOff, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
    
    
    Fit = xasoff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.plot(XEnergy, lor(XEnergy,params[0],params[2],params[1]))
        plt.plot(XEnergy, lor(XEnergy,params[3],params[5],params[4]))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
        
        
        
        
        
        
    xenergyA = 7113
    xenergyBL = 7112.5
    xenergyBH = 7115
        
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy[XEnergy<xenergyA], lorwoff(XEnergy[XEnergy<xenergyA], sigAS,x0ApS,AS, offAS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        


    paramsa,cov = curve_fit(lorwoff, XEnergy[XEnergy<xenergyA], XASDiff[XEnergy<xenergyA], p0 = [sigAS,x0ApS,AS,offAS])
    
    FitA = lorwoff(XEnergy, paramsa[0], paramsa[1], paramsa[2], paramsa[3])
    
    Bchoice = np.logical_and(XEnergy > xenergyBL, XEnergy < xenergyBH)   
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy[Bchoice], xas2diff(XEnergy[Bchoice], params[1],BpS,params[0],sigBpS,params[2],x0BpS,offBS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        


    paramsdiff,cov = curve_fit(lambda XEnergy, Bp,sigBp,x0Bp,offB: \
                               xas2diff(XEnergy, params[1],Bp,params[0],sigBp,params[2],x0Bp,offB), XEnergy[Bchoice], XASDiff[Bchoice], \
                           p0 = [BpS,sigBpS,x0BpS,offBS])

    
    FitB = xas2diff(XEnergy, params[1],paramsdiff[0],params[0],paramsdiff[1],params[2],paramsdiff[2],paramsdiff[3])
    
    """
    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp: \
                               xasdiff(XEnergy, A,sigA,x0Ap, params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS])

    
    Fit = xasdiff(XEnergy, paramsdiff[0],paramsdiff[1],paramsdiff[2], params[1],paramsdiff[3],params[0],paramsdiff[4],params[2],paramsdiff[5], \
                  params[4],paramsdiff[6],params[3],paramsdiff[7],params[5],paramsdiff[8])
    """
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, FitA)
        plt.plot(XEnergy, FitB)
        plt.plot(XEnergy, lor(XEnergy,paramsdiff[1],paramsdiff[2],abs(paramsdiff[0])))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
    

    return Fit, params, paramsa, paramsdiff, cov, 'sigA,aA,x0Ap, sigB,aB,x0B,x0Bp, sigC,aC,x0C,x0Cp'









def fitXASPiecewiseLor(XEnergy, XASDiff, XASOff, XASOn, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasdiff
    from fittingfunctions import xasoff
    from fittingfunctions import lor
    from fittingfunctions import lorwoff
    from fittingfunctions import lorwslope
    from fittingfunctions import gauswslope
    from fittingfunctions import xas2diff
    import numpy as np
    
    if False:
        sigAS = .2
        AS = 0.1
        x0ApS = 7111.8
        sigBS = .1
        sigBpS = .3
        BS = 389
        BpS = 0.1
        x0BS = 7113
        x0BpS = 7114
        sigCS = 2
        sigCpS = 2
        CS = 1012
        CpS = 0.1
        x0CS = 7115.6
        x0CpS = 7115.7
        erfslopeS = 3
        offsetS = 1342
        erfampS = 849
        peakS = 7117.4
        offAS = -0.02
        offBS = -0.06
    
    else:
        sigAS = 2
        AS = 50
        x0ApS = 7111.8
        sigBS = .1
        sigBpS = .3
        BS = 389
        BpS = 60
        x0BS = 7113
        x0BpS = 7114
        sigCS = 2
        sigCpS = 2
        CS = 1012
        CpS = 1012
        x0CS = 7115.6
        x0CpS = 7115.7
        erfslopeS = 3
        offsetS = 1342
        erfampS = 849
        peakS = 7117.4
        offAS = 177750
        offBS = -60
        slopeS = -25
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
        plt.plot(XEnergy, lor(XEnergy,sigBS,x0BS,BS))
        plt.plot(XEnergy, lor(XEnergy,sigCS,x0CS,CS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    

    params,cov = curve_fit(xasoff, XEnergy, XASOff, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
    
    
    Fit = xasoff(XEnergy, params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], params[8], params[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.plot(XEnergy, lor(XEnergy,params[0],params[2],params[1]))
        plt.plot(XEnergy, lor(XEnergy,params[3],params[5],params[4]))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
        
        
        
        
        
    xenergyAL = 7108
    xenergyAH = 7113.5
    xenergyBL = 7113
    xenergyBH = 7115.5
    Achoice = np.logical_and(XEnergy<xenergyAH, XEnergy >xenergyAL)
    Bchoice = np.logical_and(XEnergy > xenergyBL, XEnergy < xenergyBH)   
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy[Achoice], lorwslope(XEnergy[Achoice], sigAS,x0ApS,AS, offAS,slopeS))
        plt.plot(XEnergy[Bchoice], lorwoff(XEnergy[Bchoice], sigBpS,x0BpS,BpS, offBS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        


    paramsa,cov = curve_fit(gauswslope, XEnergy[Achoice], XASDiff[Achoice], p0 = [sigAS,x0ApS,AS,offAS,slopeS])
    
    FitA = lorwslope(XEnergy, paramsa[0], paramsa[1], paramsa[2], paramsa[3], paramsa[4])
    print('Adone')

    paramsb,cov = curve_fit(lorwoff, XEnergy[Bchoice], XASDiff[Bchoice], p0 = [sigBpS,x0BpS,BS,offBS])

    print('Bdone')
    FitB = lorwoff(XEnergy, paramsb[0],paramsb[1],paramsb[2],paramsb[3])
    
    """
    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp: \
                               xasdiff(XEnergy, A,sigA,x0Ap, params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS])

    
    Fit = xasdiff(XEnergy, paramsdiff[0],paramsdiff[1],paramsdiff[2], params[1],paramsdiff[3],params[0],paramsdiff[4],params[2],paramsdiff[5], \
                  params[4],paramsdiff[6],params[3],paramsdiff[7],params[5],paramsdiff[8])
    """
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, FitA)
        plt.plot(XEnergy, FitB)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
    

    return Fit, params, paramsa, paramsb, cov, 'sigA,aA,x0Ap, sigB,aB,x0B,x0Bp, sigC,aC,x0C,x0Cp'





















