# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""


def XES_TimeScan_fn(FileNums, PorM, ReEnterData, SaveData, ReLoadData, starta, startrate, startsig, FPlots):
    
    from loadData import loadData
    import pickle
    import ProcessedDataClass as PDC
    from makeTimePlot import makeOneBootFT
    from makeTimePlot import makenofitBootFT
    import numpy as np
    from MakeRawBoot import MakeRawBoot
    
    
    folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
    numBoot = 5
    
    NumTTStepsPlots = 50
    
    MinTimePlots = -250
    MaxTimePlots = 1400

    if ReEnterData:
        peaksRawData = loadData(FileNums, "Peaks", 1)
        
    if ReLoadData:
    
        with open(folder + "peaksRawData" + str(FileNums[0]) + ".pkl", "rb") as f:
            peaksRawData = pickle.load(f)

    folder_con = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
    with open(folder_con + "t0.pkl", "rb") as f:
            t0 = pickle.load(f)
    
    peaksProDataF = PDC.PeaksProcessedData(Delay = 1000*peaksRawData.TimeTool + peaksRawData.StageDelay*1e15 - t0, RowWOffset = peaksRawData.RowlandY - peaksRawData.Offset)
    peaksProDataF.makeProPeaks(peaksRawData, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
    
    TCenters = (peaksProDataF.TimeSteps[:-1]+peaksProDataF.TimeSteps[1:])/2
    
    
    PeaksBoot = np.empty((np.shape(TCenters)[0],numBoot))
    
    try:
        FT, Freq, params = makeOneBootFT(TCenters, peaksProDataF.XESDiff, MinTimePlots, MaxTimePlots, starta, startrate, startsig, PorM, FPlots)
    except:
        FT, Freq, params = makenofitBootFT(TCenters, peaksProDataF.XESDiff, FPlots)
        
    FTBoot = np.empty((np.shape(Freq)[0],numBoot))
    
    for ii in range(numBoot):

        peaksRawBoot = MakeRawBoot(peaksRawData)
        
        peaksProDataF_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBoot.TimeTool + peaksRawBoot.StageDelay*1e15 - t0, RowWOffset = peaksRawBoot.RowlandY - peaksRawBoot.Offset)
        peaksProDataF_boot.makeProPeaks(peaksRawBoot, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
        
        PeaksBoot[:,ii] = peaksProDataF_boot.XESDiff

        try:
                
            FT, Freq, params = makeOneBootFT(TCenters, peaksProDataF_boot.XESDiff, MinTimePlots, MaxTimePlots, starta, startrate, startsig, PorM, FPlots)
            FTBoot[:,ii] = abs(FT)

        except:
            
            try:
                    
                FT, Freq, params = makeOneBootFT(TCenters, peaksProDataF_boot.XESDiff, MinTimePlots, MaxTimePlots, starta*.9, startrate*.9, startsig*.9, PorM, FPlots)
                FTBoot[:,ii] = abs(FT)
                
            except:
                
                FT, Freq, params = makenofitBootFT(TCenters, peaksProDataF_boot.XESDiff, FPlots)
                FTBoot[:,ii] = abs(FT)
            
    
    PeaksBootF = np.mean(PeaksBoot,1)
    PeaksBootE = np.std(PeaksBoot,1)
    FTBootF = np.mean(FTBoot,1)
    FTBootE = np.std(FTBoot,1)


    
    if SaveData:
            
        with open(folder + "peaksRawData" + str(FileNums[0]) + ".pkl", "wb") as f:
            pickle.dump(peaksRawData, f)

        with open(folder + "peaksProData" + str(FileNums[0]) + ".pkl", "wb") as f:
            pickle.dump(peaksProDataF, f)
            
        with open(folder + "FileNums" + str(FileNums[0]) + ".pkl", "wb") as f:
            pickle.dump(FileNums, f)
    
    
    
    return PeaksBootF, PeaksBootE, FTBootF, FTBootE, Freq, TCenters





