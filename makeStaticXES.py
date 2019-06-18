# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:11:08 2019

@author: chelsea
"""
def makeStaticXES(Angle, UniqueAngle, RowlandWOffset, Diode2, Ipm2Sum, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, MaxTime, MinTime, ploton):
    
    from itertools import compress
    from makeFilter import makeFilter
    import matplotlib.pyplot as plt

    SpectraOn = []
    SpectraOff = []
    UniqueAnglep = []
    
    ii = 0
    
    FPlots = False
    
    for uangle in UniqueAngle:
        
        selectAngle = [x == uangle for x in Angle]
        
        ii = ii+1
        if ploton:
            if ii%6 == 1:
                FPlots = True
                
                
    
        rowlandwoffset = list(compress(RowlandWOffset, selectAngle))
        diode2 = list(compress(Diode2, selectAngle))
        timetool = list(compress(TimeTool, selectAngle))
        lon = list(compress(LOn, selectAngle))
        xon = list(compress(XOn, selectAngle))
    
        FilterOn, FilterOff, Offset = makeFilter(diode2, list(compress(Ipm2Sum, selectAngle)), rowlandwoffset, \
                                    xon, lon, list(compress(DiodeIpmSlope, selectAngle)), \
                                    timetool, list(compress(TTAmp, selectAngle)), list(compress(TTFWHM, selectAngle)), \
                                    FPlots, list(compress(ScanNum, selectAngle)), 2)
        
        #print(Offset)
        
        
        
        #FilterOn = [x and y for x,y in zip(xon, lon)]
        #FilterOff = [x and not y for x,y in zip(xon, lon)]

        diode2 = [x-Offset for x in diode2]

        Filteron = [(w < MaxTime) and (w > MinTime) and x for w,x in zip(timetool, FilterOn)]
        
        if sum(list(compress(diode2, FilterOff))) > 0 and sum(list(compress(diode2, Filteron))) > 0:
            SpectraOn = SpectraOn + [sum(list(compress(rowlandwoffset, FilterOff)))/sum(list(compress(diode2, FilterOff)))]
            SpectraOff = SpectraOff + [sum(list(compress(rowlandwoffset, Filteron)))/sum(list(compress(diode2, Filteron)))]
            UniqueAnglep = UniqueAnglep + [uangle]
    
        if ii%6 == 1:
            FPlots = False
            
            #plt.figure()
            #plt.plot(list(compress(diode2, FilterOn)))
            #plt.plot(list(compress(diode2, FilterOff)))
            
    return SpectraOn, SpectraOff, UniqueAnglep