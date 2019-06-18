def gauss(t,sig,t0,a):
    
    import math
    
    return [a*math.exp(-(tt-t0)**2/2/sig**2) for tt in t]


def lor(t,sig,t0,a):
    
    return [a/(1+(2*(tt-t0)/sig)**2) for tt in t]


def expdecay(a,t,t0,rate):
    
    import math
    
    out = []
    
    for ii in range(len(t)):
        if t[ii] < t0:
            out = out + [0]
        else:
            out = out + [a*math.exp(-(t[ii]-t0)/rate)]
        
    return out


def convolved(t,a,rate,t0,sig):
    
    import math
   
    out = [a*(1-math.erf(1/math.sqrt(2)*(sig/rate-(tt-t0)/sig)))*math.exp(-(tt-t0)/rate) for tt in t]
    
    return out


def combinedconvolved(t, a1, rate1, a2, rate2, t0, sig):
    
    tfirst = t[0:int(len(t)/2)]
    out1 = convolved(tfirst, a1,rate1,t0,sig)
    
    tsecond = t[int(len(t)/2):]
    out2 = convolved(tsecond, a2, rate2, t0, sig)
    
    return out1+out2


def lorwoffset(t, sig, t0, a, x0, slope):
    
    return [a/(1+(2*(tt-t0)/sig)**2)+x0+tt*slope for tt in t]

