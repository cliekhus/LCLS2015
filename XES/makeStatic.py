# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:11:08 2019

@author: chelsea
"""
def makeStaticXES(xesRawData, xesProData, MaxTime, MinTime, ploton):
    
    from makeOneFilter import makeOneFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    SpectraOn = np.empty(len(xesProData.UniAngle))
    SpectraOff = np.empty(len(xesProData.UniAngle))
    ErrorOn = np.empty(len(xesProData.UniAngle))
    ErrorOff = np.empty(len(xesProData.UniAngle))
    
    
    Filter, TTFilter = makeOneFilter(xesRawData, ploton)
    SlopeFilter, Offset = makeLineFilter(xesRawData.CspadSum, xesRawData.Diode2, np.logical_and(Filter, TTFilter), ploton)
    AllFilter = np.logical_and.reduce((Filter, TTFilter, SlopeFilter))
    
    indices2delete = []
    
    for ii in range(len(xesProData.UniAngle)):

        selectAngle = xesRawData.Angle == xesProData.UniAngle[ii]
        selectTime = np.logical_and(xesProData.TTDelay <= MaxTime, xesProData.TTDelay >= MinTime)
        
        filteron = np.logical_and.reduce((AllFilter, selectAngle, selectTime, xesRawData.LOn, xesRawData.XOn))
        filteroff = np.logical_and.reduce((SlopeFilter, selectAngle, np.logical_not(xesRawData.LOn), xesRawData.XOn))

        if np.sum(filteron.astype('int')) > 0 and np.sum(filteroff.astype('int')) > 0:
    
            SpectraOn[ii] = np.sum(xesProData.RowWOffset[filteron])/np.sum(xesRawData.CspadSum[filteron])
            SpectraOff[ii] = np.sum(xesProData.RowWOffset[filteroff])/np.sum(xesRawData.CspadSum[filteroff])
            ErrorOn[ii] = sem(xesProData.RowWOffset[filteron]/xesRawData.CspadSum[filteron])
            ErrorOff[ii] = sem(xesProData.RowWOffset[filteroff]/xesRawData.CspadSum[filteroff])
            
        else:
            
            indices2delete = indices2delete + [ii]

    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)

    return SpectraOn, SpectraOff, ErrorOn, ErrorOff




def makeStaticXAS(xasRawData, xasProData, MaxTime, MinTime, DorH, ploton):
    
    from makeOneFilter import makeOneFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    SpectraOn = np.empty(len(xasProData.UniXEnergy))
    SpectraOff = np.empty(len(xasProData.UniXEnergy))
    ErrorOn = np.empty(len(xasProData.UniXEnergy))
    ErrorOff = np.empty(len(xasProData.UniXEnergy))
    
    
    Filter, TTFilter = makeOneFilter(xasRawData, ploton)
    SlopeFilter, Offset = makeLineFilter(xasRawData.CspadSum, xasRawData.Diode2, np.logical_and(Filter, TTFilter), ploton)
    AllFilter = np.logical_and.reduce((Filter, TTFilter, SlopeFilter))
    
    indices2delete = []
    
    for ii in range(len(xasProData.UniXEnergy)):

        selectAngle = xasProData.XEnergy == xasProData.UniXEnergy[ii]
        selectTime = np.logical_and(xasProData.TTDelay <= MaxTime, xasProData.TTDelay >= MinTime)
        
        filteron = np.logical_and.reduce((AllFilter, selectAngle, selectTime, xasRawData.LOn, xasRawData.XOn))
        filteroff = np.logical_and.reduce((SlopeFilter, selectAngle, np.logical_not(xasRawData.LOn), xasRawData.XOn))

        if np.sum(filteron.astype('int')) > 0 and np.sum(filteroff.astype('int')) > 0:
    
            if DorH:
                
                SpectraOn[ii] = np.sum(xasRawData.Diode2[filteron])/np.sum(xasRawData.CspadSum[filteron])
                SpectraOff[ii] = np.sum(xasRawData.Diode2[filteroff])/np.sum(xasRawData.CspadSum[filteroff])
                ErrorOn[ii] = sem(xasRawData.Diode2[filteron]/xasRawData.CspadSum[filteron])
                ErrorOff[ii] = sem(xasRawData.Diode2[filteroff]/xasRawData.CspadSum[filteroff])
                
            else:
                    
                SpectraOn[ii] = np.sum(xasProData.RowWOffset[filteron])/np.sum(xasRawData.CspadSum[filteron])
                SpectraOff[ii] = np.sum(xasProData.RowWOffset[filteroff])/np.sum(xasRawData.CspadSum[filteroff])
                ErrorOn[ii] = sem(xasProData.RowWOffset[filteron]/xasRawData.CspadSum[filteron])
                ErrorOff[ii] = sem(xasProData.RowWOffset[filteroff]/xasRawData.CspadSum[filteroff])
            
        else:
            
            indices2delete = indices2delete + [ii]

    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)

    return SpectraOn, SpectraOff, ErrorOn, ErrorOff