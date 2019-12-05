def gauss(t,sig,t0,a):
    
    import math
    
    return [a*math.exp(-(tt-t0)**2/2/sig**2) for tt in t]


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


def convolvedzero(t,a,rate,t0,sig):
    
    import math
    
    out = [a*(1-math.erf(1/math.sqrt(2)*(sig/rate-(tt-t0)/sig)))*math.exp(-(tt-t0)/rate) for tt in t]
    
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


def combinedconvolvedzerothree(t, a1, a2, rate, t0, sig, a3):
    
    tfirst = t[0:int(len(t)/3)]
    out1 = convolved(tfirst, a1, rate, 0, t0, sig)
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    out2 = convolved(tsecond, a2, rate, 0, t0, sig)
    
    tthird = t[int(2*len(t)/3):]
    out3 = convolved(tthird, a3, rate, 0, t0, sig)
    
    return out1+out2+out3


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
    hsfirst = np.heaviside(tfirst - onset, 0)
    out1 = [x+y*z for x,y,z in zip(convolved(tfirst, a1, rate, 0, t0, sig),oscamp1*np.sin(tfirst*2*math.pi/period),hsfirst)]
    
    tsecond = t[int(len(t)/2):]
    hssecond = np.heaviside(tsecond - onset, 0)
    out2 = [x+y*z for x,y,z in zip(convolved(tsecond, a2, rate, 0, t0, sig),oscamp2*np.sin(tsecond*2*math.pi/period),hssecond)]
    
    return out1+out2


def combinedconvolvedsinethree(t, a1, a2, rate, t0, sig, oscamp1, oscamp2, oscamp3, period, onset, a3):
    import numpy as np
    import math
    
    tfirst = t[0:int(len(t)/3)]
    hsfirst = np.heaviside(tfirst - onset, 0)
    out1 = [x+y*z for x,y,z in zip(convolved(tfirst, a1, rate, 0, t0, sig),oscamp1*np.sin(tfirst*2*math.pi/period),hsfirst)]
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    hssecond = np.heaviside(tsecond - onset, 0)
    out2 = [x+y*z for x,y,z in zip(convolved(tsecond, a2, rate, 0, t0, sig),oscamp2*np.sin(tsecond*2*math.pi/period),hssecond)]
    
    tthird = t[int(2*len(t)/3):]
    hsthird = np.heaviside(tthird - onset, 0)
    out3 = [x+y*z for x,y,z in zip(convolved(tthird, a2, rate, 0, t0, sig),oscamp3*np.sin(tthird*2*math.pi/period),hsthird)]
    
    return out1+out2+out3


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



def offsetsine(t,oscamp,period,onset):
    import numpy as np
    import math
   
    hs = np.heaviside((t-onset), 0)
    out = oscamp*np.sin(t*2*math.pi/period)*hs

    return out



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