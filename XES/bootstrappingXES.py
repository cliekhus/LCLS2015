# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:02:24 2019

@author: chelsea
"""

def bootstrappingXES(NumTTStepsPlots, DiodeWOffsetp, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelaypp, TTSteps, DiodeWOffsetm, RowlandWOffsetm, Filterm, LOnm, XOnm, TTDelaymp):
    
    from makeXES import makeXES
    import random
    
    NumSamples = 10

    
    for ii in range(NumSamples):
        
        randomFilter = [bool(random.getrandbits(1)) for x in Filterp]
        
        randomFilterp = [a and b for a,b in zip(randomFilter, Filterp)]
        
        randomFilterm = [a and b for a,b in zip(randomFilter, Filterm)]
        
        XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTStepsPlots, DiodeWOffsetp, \
                                                                                                RowlandWOffsetp, randomFilterp, LOnp, XOnp, TTDelaypp, TTSteps, False)
        xesDiffplus = [(x-XESOff_Normp)*1000/XESOff_Normp for x in XESOn_Normp]
        
        if ii == 0:
            XESDiffplus = [xesDiffplus]
        else:
            XESDiffplus.append(xesDiffplus)
        
        XESOn_Normm, XESOff_Normm, Num_Onm, Num_Offm, NormFactor_Offm, NormFactor_Onm = makeXES(NumTTStepsPlots, DiodeWOffsetm, RowlandWOffsetm, \
                                                                                                randomFilterm, LOnm, XOnm, TTDelaymp, TTSteps, False)
        xesDiffminus = [(x-XESOff_Normm)*1000/XESOff_Normm for x in XESOn_Normm]
        
        if ii == 0:
            XESDiffminus = [xesDiffminus]
        else:
            XESDiffminus.append(xesDiffminus)
            
        ii = ii+1
        
    return XESDiffplus, XESDiffminus