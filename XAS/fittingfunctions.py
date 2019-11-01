def lor(x,sig,x0,a):
    
    return a/(1+(2*(x-x0)/sig)**2)


def xasdiff(x, A,sigA,x0Ap, B,Bp,sigB,sigBp,x0B,x0Bp, C,Cp,sigC,sigCp,x0C,x0Cp):
    
    return (abs(A)/(1+(2*(x-x0Ap)/sigA)**2) + Bp/(1+(2*(x-x0Bp)/sigBp)**2) - B/(1+(2*(x-x0B)/sigB)**2) + Cp/(1+(2*(x-x0Cp)/sigCp)**2) - C/(1+(2*(x-x0C)/sigC)**2))/(B/(1+(2*(x-x0B)/sigB)**2)+C/(1+(2*(x-x0C)/sigC)**2))


def xasoff(x, sigB,aB,x0B, sigC,aC,x0C, offset, erfamp, erfslope, peak):
    import numpy as np
    import math
    
    return aB/(1+(2*(x-x0B)/sigB)**2) + aC/(1+(2*(x-x0C)/sigC)**2) + offset + erfamp*np.array([math.erf((xx-peak)/erfslope) for xx in x])