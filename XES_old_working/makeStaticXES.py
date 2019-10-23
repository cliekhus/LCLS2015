# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:11:08 2019

@author: chelsea
"""
def makeStaticXES(Angle, UniqueAngle, RowlandWOffset, Diode2, Ipm2Sum, XOn, LOn, TimeTool, TTAmp, TTFWHM, ScanNum, L3E, CspadSum, MaxTime, MinTime, ploton):
    
    from itertools import compress
    from makeOneFilter import makeOneFilter
    from scipy.stats import sem

    SpectraOn = []
    SpectraOff = []
    UniqueAnglep = []
    ErrorOn = []
    ErrorOff = []
    
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


        Filter, Offset = makeOneFilter(diode2, list(compress(Ipm2Sum, selectAngle)), rowlandwoffset, xon, lon, \
                                    timetool, list(compress(TTAmp, selectAngle)), list(compress(TTFWHM, selectAngle)), \
                                    list(compress(L3E, selectAngle)), list(compress(CspadSum, selectAngle)), FPlots, 2)
        
        #print(Offset)
        
        
        
        #FilterOn = [x and y for x,y in zip(xon, lon)]
        #FilterOff = [x and not y for x,y in zip(xon, lon)]

        diode2 = [x-Offset for x in diode2]

        FilterOn = [(w < MaxTime) and (w > MinTime) and x and y for w,x,y in zip(timetool, Filter, LOn)]
        FilterOff = [x and not y for x,y in zip(Filter, LOn)]
        
        
        #print(sum([int(x) for x in Filteron]))
        #print(sum([int(x) for x in FilterOff]))
        
        if sum(list(compress(diode2, FilterOff))) > 0 and sum(list(compress(diode2, FilterOn))) > 0:
            SpectraOn = SpectraOn + [sum(list(compress(rowlandwoffset, FilterOn)))/sum(list(compress(diode2, FilterOn)))]
            SpectraOff = SpectraOff + [sum(list(compress(rowlandwoffset, FilterOff)))/sum(list(compress(diode2, FilterOff)))]
            UniqueAnglep = UniqueAnglep + [uangle]
            ErrorOn = ErrorOn + [sem(list(compress(rowlandwoffset, FilterOn)))]
            ErrorOff = ErrorOff + [sem(list(compress(rowlandwoffset, FilterOff)))]
    
        if ii%6 == 1:
            FPlots = False
            
            #plt.figure()
            #plt.plot(list(compress(diode2, FilterOn)))
            #plt.plot(list(compress(diode2, FilterOff)))
            
    return SpectraOn, SpectraOff, UniqueAnglep, ErrorOn, ErrorOff