# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""


def XES_Time_Scan_fn(FileNums, PorM, ReEnterData, SaveData, ReLoadData, FPlots):
    
    from loadData import loadData
    #from fitXES import fitXES
    from fitXES import fitXESthree
    from APSXESCalibration import convertAngle2Energy
    import pickle
    import ProcessedDataClass as PDC
    from makeTimePlot import makeTimePlot
    from makeTimePlot import makeTimePlotThree
    from makeTimePlot import makeOneBootFT
    import numpy as np
    import random
    import matplotlib.pyplot as plt
    
    
    folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
    numBoot = 100
    
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
    

        
    peaksProDataF_boot = peaksProDataF
    
    PeaksBoot = np.empty((np.shape(TCenters)[0],numBoot))
    
    TT = np.matlib.repmat(True,1,int((np.shape(peaksRawData.XOn)[0])/2))
    FF = np.matlib.repmat(False,1,int((np.shape(peaksRawData.XOn)[0])/2))
    TF = np.concatenate((TT,FF))

    TF = TF.flatten()
    
    FT, Freq, params = makeOneBootFT(TCenters, peaksProDataF.XESDiff, MinTimePlots, MaxTimePlots, FPlots)
    FTBoot = np.empty((np.shape(Freq)[0],numBoot))
    
    for ii in range(numBoot):

        random.shuffle(TF)  
        
        peaksProDataF_boot.makeBootPeaks(peaksRawData, NumTTStepsPlots, MinTimePlots, MaxTimePlots, TF, FPlots)
        
        PeaksBoot[:,ii] = peaksProDataF_boot.XESDiff
        TCenters, XESDiff, minTime, maxTime, starta, startrate, startsig, PM, ploton
        FTp, FTm, Freq = makeOneBootFT(TCenters, peaksProDataF.XESDiff, MinTimePlots, MaxTimePlots, FPlots)
        
        FTBoot[:,ii] = abs(FTm)
    
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
    
    
    
    return PeaksBootF, PeaksBootE, FTBootF, FTBootE





