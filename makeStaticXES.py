# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:11:08 2019

@author: chelsea
"""
def makeStaticXES(Angle, UniqueAngle, RowlandWOffset, Diode2, Ipm2Sum, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, MaxTime, MinTime, ploton):
    
    from itertools import compress
    from makeFilter import makeFilter

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
    
    
        Filter, Offset = makeFilter(diode2, list(compress(Ipm2Sum, selectAngle)), rowlandwoffset, \
                                    list(compress(XOn, selectAngle)), list(compress(LOn, selectAngle)), list(compress(DiodeIpmSlope, selectAngle)), \
                                    timetool, list(compress(TTAmp, selectAngle)), list(compress(TTFWHM, selectAngle)), \
                                    FPlots, list(compress(ScanNum, selectAngle)), 2)
        
        diode2 = [x-Offset for x in diode2]
        
        Filteroff = [x and y and not z for x,y,z in zip(Filter, XOn, LOn)]
        Filteron = [(w < MaxTime) and (w > MinTime) and x and y and z for w,x,y,z in zip(timetool, Filter, XOn, LOn)]
        
        if sum(list(compress(diode2, Filteroff))) > 0 and sum(list(compress(diode2, Filteron))) > 0:
            SpectraOn = SpectraOn + [sum(list(compress(rowlandwoffset, Filteroff)))/sum(list(compress(diode2, Filteroff)))]
            SpectraOff = SpectraOff + [sum(list(compress(rowlandwoffset, Filteron)))/sum(list(compress(diode2, Filteron)))]
            UniqueAnglep = UniqueAnglep + [uangle]
    
        if ii%6 == 1:
            FPlots = False
            
    return SpectraOn, SpectraOff, UniqueAnglep