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


def convolved(t,a,rate,offset,t0,sig):
    
    import math
   
    out = [a*(1-math.erf(1/math.sqrt(2)*(sig/rate-(tt-t0)/sig)))*math.exp(-(tt-t0)/rate) + offset for tt in t]
    
    return out



def combinedconvolved(t, a1, rate1, offset1, a2, rate2, offset2, t0, sig):
    
    tfirst = t[0:int(len(t)/2)]
    out1 = convolved(tfirst, a1,rate1, offset1, t0, sig)
    
    tsecond = t[int(len(t)/2):]
    out2 = convolved(tsecond, a2, rate2, offset2, t0, sig)
    
    return out1+out2


def combinedconvolvedzero(t, a1, a2, rate, t0, sig):
    
    tfirst = t[0:int(len(t)/2)]
    out1 = convolved(tfirst, a1, rate, 0, t0, sig)
    
    tsecond = t[int(len(t)/2):]
    out2 = convolved(tsecond, a2, rate, 0, t0, sig)
    
    return out1+out2


def combinedconvolvedoff(t, a1, a2, rate, offset1, offset2, t0, sig):
    
    tfirst = t[0:int(len(t)/2)]
    out1 = convolved(tfirst, a1, rate, offset1, t0, sig)
    
    tsecond = t[int(len(t)/2):]
    out2 = convolved(tsecond, a2, rate, offset2, t0, sig)
    
    return out1+out2


def combinedconvolvedsine(t, a1, a2, rate, t0, sig, oscamp1, oscamp2, period, onset):
    import numpy as np
    import math
    
    tfirst = t[0:int(len(t)/2)]
    
    hs = np.heaviside(t, onset)
    
    out1 = [x+y*z for x,y,z in zip(convolved(tfirst, a1, rate, 0, t0, sig),oscamp1*np.sin(tfirst*2*math.pi/period),hs)]
    
    tsecond = t[int(len(t)/2):]
    out2 = [x+y*z for x,y,z in zip(convolved(tsecond, a2, rate, 0, t0, sig),oscamp2*np.sin(tsecond*2*math.pi/period),hs)]
  
    return out1+out2


def convolvedsine(t,a,rate,offset,t0,sig,oscamp,period,onset):
    import numpy as np
    import math
   
    hs = np.heaviside(t, onset)
        
    out1 = [a*(1-math.erf(1/math.sqrt(2)*(sig/rate-(tt-t0)/sig)))*math.exp(-(tt-t0)/rate) + offset for tt in t]
    out2 = oscamp*np.sin(t*2*math.pi/period)*hs
    out = [x+y for x,y in zip(out1,out2)]
    
    return out


def combinedconvolvedtwo(t, a1, a2, rate1, t0, sig1, rate2, sig2):
    
    tfirst = t[0:int(len(t)/2)]
    out1 = convolved(tfirst, a1, rate1, 0, t0, sig1)
    
    tsecond = t[int(len(t)/2):]
    out2 = convolved(tsecond, a2, rate2, 0, t0, sig2)
    
    return out1+out2


def lorwoffset(t, sig, t0, a, x0, slope):
    
    return [a/(1+(2*(tt-t0)/sig)**2)+x0+tt*slope for tt in t]

