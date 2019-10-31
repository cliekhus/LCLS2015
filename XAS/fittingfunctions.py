def lor(x,sig,x0,a):
    
    return a/(1+(2*(x-x0)/sig)**2)


def xasdiff(x, Amp, sigA,x0Ap, sigB,x0B,x0Bp, sigC,x0C,x0Cp):
    
    return Amp*.1/(1+(2*(x-x0Ap)/sigA)**2) + Amp*.49/(1+(2*(x-x0Bp)/sigB)**2) - Amp*.49/(1+(2*(x-x0B)/sigB)**2) + Amp*1.4/(1+(2*(x-x0Cp)/sigC)**2) - Amp*1.4/(1+(2*(x-x0C)/sigC)**2)


def xasoff(x, sigB,aB,x0B, sigC,aC,x0C, offset, slope, expamp):
    import numpy as np
    
    return aB/(1+(2*(x-x0B)/sigB)**2) + aC/(1+(2*(x-x0C)/sigC)**2) + offset + expamp*np.exp((x-7110)*slope)