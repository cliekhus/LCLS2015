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
    indices2delete = []
    
    for ii in range(len(xesProData.UniAngle)):

        selectAngle = xesRawData.Angle == xesProData.UniAngle[ii]
        selectTime = np.logical_and(xesProData.TTDelay <= MaxTime, xesProData.TTDelay >= MinTime)

        SlopeFilter, Offset = makeLineFilter(xesRawData.Ipm2Sum, xesRawData.Diode2, np.logical_and.reduce((Filter, TTFilter, )), ploton)
        AllFilter = np.logical_and.reduce((Filter, TTFilter, SlopeFilter))
        
        filteron = np.logical_and.reduce((AllFilter, selectAngle, selectTime, xesRawData.LOn, xesRawData.XOn))
        filteroff = np.logical_and.reduce((SlopeFilter, selectAngle, np.logical_not(xesRawData.LOn), xesRawData.XOn))
        print('filters')
        print(np.sum(AllFilter.astype('int')))
        print(np.sum(selectAngle.astype('int')))
        print(np.sum(selectTime.astype('int')))
        print(np.sum(xesRawData.LOn.astype('int')))
        print(np.sum(xesRawData.LOn.astype('int')))
        print(np.sum(xesRawData.XOn.astype('int')))
        print(np.sum(SlopeFilter.astype('int')))
        print(np.sum(filteron.astype('int')))
        print(np.sum(filteroff.astype('int')))


        if np.sum(filteron.astype('int')) > 0 and np.sum(filteroff.astype('int')) > 0:
    
            SpectraOn[ii] = np.sum(xesProData.RowWOffset[filteron])/np.sum(xesRawData.Ipm2Sum[filteron])
            SpectraOff[ii] = np.sum(xesProData.RowWOffset[filteroff])/np.sum(xesRawData.Ipm2Sum[filteroff])
            ErrorOn[ii] = sem(xesProData.RowWOffset[filteron]/xesRawData.Ipm2Sum[filteron])
            ErrorOff[ii] = sem(xesProData.RowWOffset[filteroff]/xesRawData.Ipm2Sum[filteroff])
            
        else:
            
            indices2delete = indices2delete + [ii]

    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)
    UniAngle = np.delete(xesProData.UniAngle, indices2delete)

    return SpectraOn, SpectraOff, ErrorOn, ErrorOff, UniAngle


