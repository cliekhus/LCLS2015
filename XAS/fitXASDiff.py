# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:45:19 2019

@author: chelsea
"""

def fitXASDiff(XEnergy, XASDiff, XASOff, XASOn, ploton):
    
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from fittingfunctions import xasdiff
    from fittingfunctions import xasoff
    from fittingfunctions import lor
    
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
        sigAS = .5
        AS = 100
        x0ApS = 7111.2
        sigBS = .5
        sigBpS = .5
        BS = 389
        BpS = 389
        x0BS = 7113
        x0BpS = 7114.5
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
        
        
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, xasoff(XEnergy, sigBpS,BpS,x0BpS, sigCpS,CpS,x0CpS, offsetS,erfampS,erfslopeS,peakS))
        plt.plot(XEnergy, lor(XEnergy,sigBS,x0BS,BS))
        plt.plot(XEnergy, lor(XEnergy,sigCS,x0CS,CS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        
    paramsp,cov = curve_fit(xasoff, XEnergy, XASOff, p0 = [sigBpS,BpS,x0BpS, sigCpS,CpS,x0CpS, offsetS,erfampS,erfslopeS,peakS])
    
    Fit = xasoff(XEnergy, paramsp[0], paramsp[1], paramsp[2], paramsp[3], paramsp[4], paramsp[5], paramsp[6], paramsp[7], paramsp[8], paramsp[9])
    
    if ploton:
            
        plt.figure()
        plt.plot(XEnergy, XASOff, 'o')
        plt.plot(XEnergy, Fit)
        plt.title('end parameters')
        plt.xlabel('energy (eV)')


    
    
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy, xasdiff(XEnergy, AS,sigAS,x0ApS, params[1],BpS,params[0],sigBpS,params[2],x0BpS, params[4],CpS,params[3],sigCpS,params[5],x0CpS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        

    paramsdiff,cov = curve_fit(lambda XEnergy, A,sigA,x0Ap, Bp,sigBp,x0Bp, Cp,sigCp,x0Cp: \
                               xasdiff(XEnergy, A,sigA,x0Ap, params[1],Bp,params[0],sigBp,params[2],x0Bp, params[4],Cp,params[3],sigCp,params[5],x0Cp), XEnergy, XASDiff, \
                           p0 = [AS,sigAS,x0ApS, BpS,sigBpS,x0BpS, CpS,sigCpS,x0CpS])

    
    Fit = xasdiff(XEnergy, paramsdiff[0],paramsdiff[1],paramsdiff[2], params[1],paramsdiff[3],params[0],paramsdiff[4],params[2],paramsdiff[5], \
                  params[4],paramsdiff[6],params[3],paramsdiff[7],params[5],paramsdiff[8])
    
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
        plt.plot(XEnergy, lor(XEnergy,paramsdiff[1],paramsdiff[2],abs(paramsdiff[0])))
        plt.plot(XEnergy, lor(XEnergy,paramsdiff[4],paramsdiff[5],abs(paramsdiff[3])))
        plt.plot(XEnergy, lor(XEnergy,paramsdiff[7],paramsdiff[8],abs(paramsdiff[6])))
        plt.title('end parameters')
        plt.xlabel('energy (eV)')
    

    return Fit, params, paramsp, paramsdiff, cov, 'sigA,aA,x0Ap, sigB,aB,x0B,x0Bp, sigC,aC,x0C,x0Cp'







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
    from fittingfunctions import xas2diff
    import numpy as np
    
    if True:
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
        sigAS = .2
        AS = 100
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
        offAS = -30
        offBS = -60
    
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
    xenergyBL = 7113
    xenergyBH = 7115.5
    Bchoice = np.logical_and(XEnergy > xenergyBL, XEnergy < xenergyBH)   
    if ploton:

        plt.figure()
        plt.plot(XEnergy, XASDiff, 'o')
        plt.plot(XEnergy[XEnergy<xenergyA], lorwoff(XEnergy[XEnergy<xenergyA], sigAS,x0ApS,AS, offAS))
        plt.plot(XEnergy[Bchoice], lorwoff(XEnergy[Bchoice], sigBpS,x0BpS,BpS, offBS))
        plt.title('start parameters')
        plt.xlabel('energy (eV)')
        


    paramsa,cov = curve_fit(lorwoff, XEnergy[XEnergy<xenergyA], XASDiff[XEnergy<xenergyA], p0 = [sigAS,x0ApS,AS,offAS])
    
    FitA = lorwoff(XEnergy, paramsa[0], paramsa[1], paramsa[2], paramsa[3])
    print('hi')

    paramsb,cov = curve_fit(lorwoff, XEnergy[Bchoice], XASDiff[Bchoice], p0 = [sigBpS,x0BpS,BS,offBS])

    
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









