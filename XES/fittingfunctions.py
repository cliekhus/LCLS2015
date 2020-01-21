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



def combinedzerothreeexp(t, a1, a2, rate, t0, sig, a3, rate2, a4):
    
    tfirst = t[0:int(len(t)/3)]
    out1 = convolved(tfirst, a1, rate, 0, t0, sig)
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    out2a = convolved(tsecond, a2, rate, 0, t0, sig) 
    out2b = convolved(tsecond, a4, rate2, 0, t0, sig)
    out2 = [x+y for x,y in zip(out2a,out2b)]
    
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


def lorwoffset(t, sig, t0, a, x0, slope):
    
    return [a/(1+(2*(tt-t0)/sig)**2)+x0+tt*slope for tt in t]



def offsetsine(t,oscamp,period,onset):
    import numpy as np
    import math
   
    hs = np.heaviside((t-onset), 0)
    out = oscamp*np.sin(t*2*math.pi/period)*hs

    return out






def globalfit(t, t0, sig, a11, a21, a31, rate1, a12, a22, a32, rate2):
    
    tfirst = t[0:int(len(t)/3)]
    out11 = globalconvolved(tfirst, t0, sig, a11, rate1, 0)
    out12 = globalconvolved(tfirst, t0, sig, a12, rate2, 0)
    out1 = [x+y for x,y in zip(out11, out12)]
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    out21 = globalconvolved(tsecond, t0, sig, a21, rate1, 0) 
    out22 = globalconvolved(tsecond, t0, sig, a22, rate2, 0)
    out2 = [x+y for x,y in zip(out21,out22)]
    
    tthird = t[int(2*len(t)/3):]
    out31 = globalconvolved(tthird, t0, sig, a31, rate1, 0)
    out32 = globalconvolved(tthird, t0, sig, a32, rate2, 0)
    out3 = [x+y for x,y in zip(out31, out32)]
    
    return out1+out2+out3




def globalfitsimple(t, t0, sig, a1, a2, a3, rate):
    
    tfirst = t[0:int(len(t)/3)]
    out1 = globalconvolved(tfirst, t0, sig, a1, rate, 0)
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    out2 = globalconvolved(tsecond, t0, sig, a2, rate, 0)
    
    tthird = t[int(2*len(t)/3):]
    out3 = globalconvolved(tthird, t0, sig, a3, rate, 0)
    
    return out1+out2+out3



def globalconvolved(t, t0, sig, a, rate, offset):
    
    import math
    
    out = [a*(1-math.erf(1/math.sqrt(2)*(sig/rate-(tt-t0)/sig)))*math.exp(-(tt-t0)/rate) + offset for tt in t]
    
    return out




def halffit(t, t0, sig, a11, a21, a31, rate1, a22, rate2):
    
    tfirst = t[0:int(len(t)/3)]
    out11 = globalconvolved(tfirst, t0, sig, a11, rate1, 0)
    out1 = out11
    
    tsecond = t[int(len(t)/3):int(2*len(t)/3)]
    out21 = globalconvolved(tsecond, t0, sig, a21, rate1, 0) 
    out22 = globalconvolved(tsecond, t0, sig, a22, rate2, 0)
    out2 = [x+y for x,y in zip(out21,out22)]
    
    tthird = t[int(2*len(t)/3):]
    out31 = globalconvolved(tthird, t0, sig, a31, rate1, 0)
    out3 = out31
    
    return out1+out2+out3