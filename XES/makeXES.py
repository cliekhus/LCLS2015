# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeXES(peaksProData, peaksRawData, NumTTSteps, MinTime, MaxTime, ploton):
    
    from makeOneFilter import makeOneFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    SpectraOn = np.empty(NumTTSteps-1)
    SpectraOff = np.empty(NumTTSteps-1)
    ErrorOn = np.empty(NumTTSteps-1)
    ErrorOff = np.empty(NumTTSteps-1)
    TimeSteps = np.linspace(MinTime, MaxTime, NumTTSteps)
    
    
    Filter, TTFilter = makeOneFilter(peaksRawData, ploton)
    SlopeFilter, ROffset = makeLineFilter(peaksRawData.RowlandY, peaksRawData.Diode2, np.logical_and(Filter, TTFilter), ploton)
    AllFilter = np.logical_and.reduce((Filter, TTFilter, SlopeFilter))
    
    filteroff = np.logical_and.reduce((SlopeFilter, np.logical_not(peaksRawData.LOn), peaksRawData.XOn, Filter))
    SpectraOff = np.sum(peaksProData.RowWOffset[filteroff]-ROffset)/np.sum(peaksRawData.Diode2[filteroff])
    #SpectraOff = np.sum(peaksProData.RowWOffset[filteroff])/np.sum(peaksRawData.Ipm2Sum[filteroff])
    ErrorOff = sem(peaksProData.RowWOffset[filteroff]/peaksRawData.Diode2[filteroff])
            
    indices2delete = []
    
    for ii in range(len(TimeSteps)-1):

        selectTime = np.logical_and(peaksProData.Delay < TimeSteps[ii+1], peaksProData.Delay >= TimeSteps[ii])
        filteron = np.logical_and.reduce((AllFilter, selectTime, peaksRawData.LOn, peaksRawData.XOn))

        if np.sum(filteron.astype('int')) > 0 and np.sum(filteroff.astype('int')) > 0:
    
            SpectraOn[ii] = np.sum(peaksProData.RowWOffset[filteron]-ROffset)/np.sum(peaksRawData.Diode2[filteron])
            #SpectraOn[ii] = np.sum(peaksProData.RowWOffset[filteron])/np.sum(peaksRawData.Ipm2Sum[filteron])
            ErrorOn[ii] = sem(peaksProData.RowWOffset[filteron]/peaksRawData.Diode2[filteron])

        else:
            
            indices2delete = indices2delete + [ii]

    
    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)
    TimeSteps = np.delete(TimeSteps, indices2delete)
    
            
    return SpectraOn, SpectraOff, ErrorOn, ErrorOff, TimeSteps




def makeBootXES(peaksProData, peaksRawData, NumTTSteps, MinTime, MaxTime, TF, ploton):
    
    from makeOneFilter import makeOneFilter
    from scipy.stats import sem
    from makeIntensityFilter import makeLineFilter
    import numpy as np


    SpectraOn = np.empty(NumTTSteps-1)
    SpectraOff = np.empty(NumTTSteps-1)
    ErrorOn = np.empty(NumTTSteps-1)
    ErrorOff = np.empty(NumTTSteps-1)
    TimeSteps = np.linspace(MinTime, MaxTime, NumTTSteps)
    
    
    Filter, TTFilter = makeOneFilter(peaksRawData, ploton)
    Filter = np.logical_and(Filter, TF)
    SlopeFilter, ROffset = makeLineFilter(peaksRawData.RowlandY, peaksRawData.Diode2, np.logical_and(Filter, TTFilter), ploton)
    AllFilter = np.logical_and.reduce((Filter, TTFilter, SlopeFilter))
    
    filteroff = np.logical_and.reduce((SlopeFilter, np.logical_not(peaksRawData.LOn), peaksRawData.XOn, Filter))
    SpectraOff = np.sum(peaksProData.RowWOffset[filteroff]-ROffset)/np.sum(peaksRawData.Diode2[filteroff])
    #SpectraOff = np.sum(peaksProData.RowWOffset[filteroff])/np.sum(peaksRawData.Ipm2Sum[filteroff])
    ErrorOff = sem(peaksProData.RowWOffset[filteroff]/peaksRawData.Diode2[filteroff])

            
    indices2delete = []
    
    for ii in range(len(TimeSteps)-1):

        selectTime = np.logical_and(peaksProData.Delay < TimeSteps[ii+1], peaksProData.Delay >= TimeSteps[ii])
        filteron = np.logical_and.reduce((AllFilter, selectTime, peaksRawData.LOn, peaksRawData.XOn))

        if np.sum(filteron.astype('int')) > 0 and np.sum(filteroff.astype('int')) > 0:
    
            SpectraOn[ii] = np.sum(peaksProData.RowWOffset[filteron]-ROffset)/np.sum(peaksRawData.Diode2[filteron])
            #SpectraOn[ii] = np.sum(peaksProData.RowWOffset[filteron])/np.sum(peaksRawData.Ipm2Sum[filteron])
            ErrorOn[ii] = sem(peaksProData.RowWOffset[filteron]/peaksRawData.Diode2[filteron])

        else:
            
            indices2delete = indices2delete + [ii]

    
    SpectraOn = np.delete(SpectraOn, indices2delete)
    SpectraOff = np.delete(SpectraOff, indices2delete)
    ErrorOn = np.delete(ErrorOn, indices2delete)
    ErrorOff = np.delete(ErrorOff, indices2delete)
    TimeSteps = np.delete(TimeSteps, indices2delete)
    
            
    return SpectraOn, SpectraOff, ErrorOn, ErrorOff, TimeSteps