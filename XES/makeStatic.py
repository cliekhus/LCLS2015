# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:11:08 2019

@author: chelsea
"""
def makeStaticXES(xesRawData, xesProData, MaxTime, MinTime, ploton):
    
    
    
    from makeMedianFilter import makeMedFilter
    from makeTimeFilter import makeTimeFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    numAngle = len(xesProData.UniAngle)
    SpectraOn = np.empty(numAngle)
    SpectraOff = np.empty(numAngle)
    ErrorOn = np.empty(numAngle)
    ErrorOff = np.empty(numAngle)
        
    TTFilter = makeTimeFilter(xesRawData, ploton)
    TimeFilter = np.logical_and.reduce((xesProData.TTDelay<MaxTime, xesProData.TTDelay>MinTime, TTFilter))
    
    indices2delete = []
    
    for ii in range(numAngle):

        selectAngle = xesRawData.Angle == xesProData.UniAngle[ii]
        filteron = np.logical_and.reduce((TimeFilter, selectAngle, xesRawData.LOn, xesRawData.XOn))
        filteroff = np.logical_and.reduce((selectAngle, np.logical_not(xesRawData.LOn), xesRawData.XOn))
        MedianFilterOn = makeMedFilter(xesRawData, filteron, ploton)
        MedianFilterOff = makeMedFilter(xesRawData, filteroff, ploton)
        SlopeFilterOn, ROffsetOn = makeLineFilter(xesRawData.RowlandY, xesRawData.Diode2, filteron, ploton)
        SlopeFilterOff, ROffsetOff = makeLineFilter(xesRawData.RowlandY, xesRawData.Diode2, filteroff, ploton)
        FilterOn = np.logical_and(SlopeFilterOn, MedianFilterOn, filteron)
        FilterOff = np.logical_and(SlopeFilterOff, MedianFilterOff, filteroff)


        if np.sum(FilterOn.astype('int')) > 0 and np.sum(FilterOff.astype('int')) > 0:
    
            SpectraOn[ii] = np.nansum(xesProData.RowWOffset[FilterOn])/np.nansum(xesRawData.Diode2[FilterOn])
            SpectraOff[ii] = np.nansum(xesProData.RowWOffset[FilterOff])/np.nansum(xesRawData.Diode2[FilterOff])
            ErrorOn[ii] = sem(xesProData.RowWOffset[FilterOn]/xesRawData.Diode2[FilterOn])
            ErrorOff[ii] = sem(xesProData.RowWOffset[FilterOff]/xesRawData.Diode2[FilterOff])
            
            

        else:
            
            indices2delete = indices2delete + [ii]

    
    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)
    UniAngle = np.delete(xesProData.UniAngle, indices2delete)
    
            
    return SpectraOn, SpectraOff, ErrorOn, ErrorOff, UniAngle
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def makeLaserXES(xesRawData, xesProData, MaxTime, MinTime, ploton):
    
    
    
    from makeMedianFilter import makeMedFilter
    from makeTimeFilter import makeTimeFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    numAngle = len(xesProData.UniAngle)
    SpectraOn = np.empty(numAngle)
    SpectraOff = np.empty(numAngle)
    ErrorOn = np.empty(numAngle)
    ErrorOff = np.empty(numAngle)
        
    TTFilter = makeTimeFilter(xesRawData, ploton)
    TimeFilter = np.logical_and.reduce((xesProData.TTDelay<MaxTime, xesProData.TTDelay>MinTime, TTFilter))
    
    indices2delete = []
    
    for ii in range(numAngle):

        selectAngle = xesRawData.Angle == xesProData.UniAngle[ii]
        filteron = np.logical_and.reduce((TimeFilter, selectAngle, xesRawData.LOn, xesRawData.XOn))
        filteroff = np.logical_and.reduce((selectAngle, np.logical_not(xesRawData.LOn), xesRawData.XOn))
        MedianFilterOn = makeMedFilter(xesRawData, filteron, ploton)
        MedianFilterOff = makeMedFilter(xesRawData, filteroff, ploton)
        SlopeFilterOn, ROffsetOn = makeLineFilter(xesRawData.RowlandY, xesRawData.Diode2, filteron, ploton)
        SlopeFilterOff, ROffsetOff = makeLineFilter(xesRawData.RowlandY, xesRawData.Diode2, filteroff, ploton)
        FilterOn = np.logical_and(SlopeFilterOn, MedianFilterOn, filteron)
        FilterOff = np.logical_and(SlopeFilterOff, MedianFilterOff, filteroff)


        if np.sum(FilterOn.astype('int')) > 0 and np.sum(FilterOff.astype('int')) > 0:
    
            
            SpectraOn[ii] = np.nansum(xesProData.RowWOffset[FilterOn])/np.nansum(xesRawData.Diode2[FilterOn])
            SpectraOff[ii] = np.nansum(xesProData.RowWOffset[FilterOff])/np.nansum(xesRawData.Diode2[FilterOff])
            ErrorOn[ii] = sem(xesProData.RowWOffset[FilterOn]/xesRawData.Diode2[FilterOn])
            ErrorOff[ii] = sem(xesProData.RowWOffset[FilterOff]/xesRawData.Diode2[FilterOff])
            """
            SpectraOn[ii] = np.nansum(xesRawData.Diode2[FilterOn])/np.nansum(xesRawData.Ipm2Sum[FilterOn])
            SpectraOff[ii] = np.nansum(xesRawData.Diode2[FilterOff])/np.nansum(xesRawData.Ipm2Sum[FilterOff])
            ErrorOn[ii] = sem(xesRawData.Diode2[FilterOn]/xesRawData.Ipm2Sum[FilterOn])
            ErrorOff[ii] = sem(xesRawData.Diode2[FilterOff]/xesRawData.Ipm2Sum[FilterOff])
            """
            """
            SpectraOn[ii] = np.nansum(xesRawData.CspadSum[FilterOn])/np.nansum(xesRawData.Diode2[FilterOn])
            SpectraOff[ii] = np.nansum(xesRawData.CspadSum[FilterOff])/np.nansum(xesRawData.Diode2[FilterOff])
            ErrorOn[ii] = sem(xesRawData.CspadSum[FilterOn]/xesRawData.Ipm2Sum[FilterOn])
            ErrorOff[ii] = sem(xesRawData.CspadSum[FilterOff]/xesRawData.Ipm2Sum[FilterOff])
            """
            

        else:
            
            indices2delete = indices2delete + [ii]

    
    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)
    UniAngle = np.delete(xesProData.UniAngle, indices2delete)
    
            
    return SpectraOn, SpectraOff, ErrorOn, ErrorOff, UniAngle
    
    
    
    
    
    
    
    
    
"""    
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


"""