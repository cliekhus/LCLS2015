def gauswslope(x,sig,x0,a,off,slope):
    import numpy as np
    return abs(a)*np.exp(-((x-abs(x0))/sig)**2)+off-abs(slope)*x




def xasoff(x, sigB,aB,x0B, sigC,aC,x0C, offset, erfamp, erfslope, peak):
    import numpy as np
    import math
    
    return np.array([abs(aB)*math.exp(-(xx-x0B)**2/sigB) + abs(aC)*math.exp(-(xx-x0C)**2/sigC) for xx in x]) + offset + erfamp*np.array([math.erf((xx-peak)/erfslope) for xx in x])



def xason(x, sigA,aA,x0A, sigB,aB,x0B, sigC,aC,x0C, offset, erfamp, erfslope, peak):
    import numpy as np
    import math
    
    return np.array([abs(aA)*math.exp(-(xx-x0A)**2/sigA) + abs(aB)*math.exp(-(xx-x0B)**2/sigB) + abs(aC)*math.exp(-(xx-x0C)**2/sigC) for xx in x]) + offset + erfamp*np.array([math.erf((xx-peak)/erfslope) for xx in x])



def diffxas(x, x0A, x0B, x0C, amp, y0, a, b, aA):
    import numpy as np
    import pickle
    
    folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"
    
    with open(folder + "Fe_fits.pkl", "rb") as f:
        Fe_fits = pickle.load(f)
    
    
    
    params_II = Fe_fits["params_II"]
    params_III = Fe_fits["params_III"]
    params_XAS = Fe_fits["params_XAS"]
    
    params_XAS[2] = params_XAS[2]-Fe_fits["energy_shift"]
    params_XAS[5] = params_XAS[5]-Fe_fits["energy_shift"]
    params_XAS[9] = params_XAS[9]-Fe_fits["energy_shift"]
    
    out = (xason(x, params_III[0],aA,x0A, params_III[3],params_III[4],x0B, \
            params_III[6],params_III[7],x0C, 0,0,0,0))*amp \
            - xasoff(x,  params_II[0],params_II[1],params_II[2], params_II[3],params_II[4],params_II[5],\
                     0,0,0,0) + y0+a*x+b*x**2
    
    return out


def lor(x,sig,x0,a):
    
    return a/(1+(2*(x-x0)/sig)**2)







###############################################################################
# Functions I don't use below #################################################
###############################################################################
    

















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






def lorwoff(x,sig,x0,a,off):
    
    return abs(a)/(1+(2*(x-x0)/sig)**2)+off





def lorwslope(x,sig,x0,a,off,slope):
    
    return abs(a)/(1+(2*(x-x0)/sig)**2)+off+slope*x





def xasdiff_old(x, A,sigA,x0Ap, B,Bp,sigB,sigBp,x0B,x0Bp, C,Cp,sigC,sigCp,x0C,x0Cp, EF, off,slope):
    import numpy as np
    import math
    
    return np.array([EF*(A*math.exp(-(xx-x0Ap)**2/sigA) + Bp*math.exp(-(xx-x0Bp)**2/sigBp) - B*math.exp(-(xx-x0B)**2/sigB) + Cp*math.exp(-(xx-x0Cp)**2/sigCp) - C*math.exp(-(xx-x0C)**2/sigC)) +off+xx*slope for xx in x])
    #return (abs(A)/(1+(2*(x-x0Ap)/sigA)**2) + abs(Bp)/(1+(2*(x-x0Bp)/sigBp)**2) - abs(B)/(1+(2*(x-x0B)/sigB)**2) + abs(Cp)/(1+(2*(x-x0Cp)/sigCp)**2) - abs(C)/(1+(2*(x-x0C)/sigC)**2))





def xasdiff(x, B,Bp,sigB,sigBp,x0B,x0Bp, EF, off,slope):
    import numpy as np
    import math
    
    return np.array([EF*Bp*math.exp(-(xx-x0Bp)**2/sigBp) - B*math.exp(-(xx-x0B)**2/sigB) +off+xx*slope for xx in x])





def xasdiff_old2(x, A,sigA,x0Ap, B,Bp,sigB,sigBp,x0B,x0Bp, EF, off,slope):
    import numpy as np
    import math
    
    return np.array([A*math.exp(-(xx-x0Ap)**2/sigA) + EF*(Bp*math.exp(-(xx-x0Bp)**2/sigBp) - B*math.exp(-(xx-x0B)**2/sigB)) +off+xx*slope for xx in x])
 





def xas2diff(x,B,Bp,sigB,sigBp,x0B,x0Bp,off):
    
    return (abs(Bp)/(1+(2*(x-x0Bp)/sigBp)**2) - abs(B)/(1+(2*(x-x0B)/sigB)**2) + off)
























