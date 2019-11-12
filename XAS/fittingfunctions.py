def lor(x,sig,x0,a):
    
    return a/(1+(2*(x-x0)/sig)**2)


def lorwoff(x,sig,x0,a,off):
    
    return abs(a)/(1+(2*(x-x0)/sig)**2)+off

def lorwslope(x,sig,x0,a,off,slope):
    
    return abs(a)/(1+(2*(x-x0)/sig)**2)+off+slope*x

def gauswslope(x,sig,x0,a,off,slope):
    import numpy as np
    return abs(a)*np.exp(-((x-x0)/sig)**2)+off+slope*x

def xasdiff(x, A,sigA,x0Ap, B,Bp,sigB,sigBp,x0B,x0Bp, C,Cp,sigC,sigCp,x0C,x0Cp):
    
    return (abs(A)/(1+(2*(x-x0Ap)/sigA)**2) + abs(Bp)/(1+(2*(x-x0Bp)/sigBp)**2) - abs(B)/(1+(2*(x-x0B)/sigB)**2) + abs(Cp)/(1+(2*(x-x0Cp)/sigCp)**2) - abs(C)/(1+(2*(x-x0C)/sigC)**2))

def xas2diff(x,B,Bp,sigB,sigBp,x0B,x0Bp,off):
    
    return (abs(Bp)/(1+(2*(x-x0Bp)/sigBp)**2) - abs(B)/(1+(2*(x-x0B)/sigB)**2) + off)


def xasoff(x, sigB,aB,x0B, sigC,aC,x0C, offset, erfamp, erfslope, peak):
    import numpy as np
    import math
    
    return aB/(1+(2*(x-x0B)/sigB)**2) + aC/(1+(2*(x-x0C)/sigC)**2) + offset + erfamp*np.array([math.erf((xx-peak)/erfslope) for xx in x])