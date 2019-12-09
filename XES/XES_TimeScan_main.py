# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""


from loadData import loadData
#from fitXES import fitXES
from fitXES import fitXESthree
from APSXESCalibration import convertAngle2Energy
import pickle
import ProcessedDataClass as PDC
from makeTimePlot import makeTimePlot
from makeTimePlot import makeTimePlotThree
from makeTimePlot import makeTimePlotThreeError
from makeTimePlot import makeBootFT
from makeTimePlot import makeOneBootFT
import numpy as np
import random
import matplotlib.pyplot as plt
import math
from MakeRawBoot import MakeRawBoot


folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
Boot = True
numBoot = 100

NumTTSteps = 100
NumTTStepsPlots = 50

MinTime = -2000 
MaxTime = 0                                                                                                                                                                           

MinTimePlots = -250
MaxTimePlots = 1400

removenum = 9

#plus data

if ReEnterData:

    #FileNumsP = list(range(144, 154+1))
    #FileNumsP = list(range(131, 140+1))
    #FileNumsP = list(range(165, 178+1))
    FileNumsP = list(range(123, 130+1))
    #FileNumsP = list(range(155,164+1))
    #FileNumsP = [103,105,115,121]
    #FileNumsP.remove(FileNumsP[removenum])
    peaksRawDataP = loadData(FileNumsP, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataP.pkl", "rb") as f:
        peaksRawDataP = pickle.load(f)
        
    with open(folder + "FileNumsP.pkl", "rb") as f:
        FileNumsP = pickle.load(f)

peaksProDataP = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP.TimeTool + peaksRawDataP.StageDelay*1e15, RowWOffset = peaksRawDataP.RowlandY - peaksRawDataP.Offset)
peaksProDataP.makeProPeaks(peaksRawDataP, NumTTSteps, MinTime, MaxTime, FPlots)




#plus2 data

if ReEnterData:

    #FileNumsP2 = list(range(123, 130+1))
    #FileNumsP2 = [105,103]
    FileNumsP2 = list(range(155,164+1))
    #FileNumsP2.remove(FileNumsP2[removenum])
    peaksRawDataP2 = loadData(FileNumsP2, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataP2.pkl", "rb") as f:
        peaksRawDataP2 = pickle.load(f)
        
    with open(folder + "FileNumsP2.pkl", "rb") as f:
        FileNumsP2 = pickle.load(f)

peaksProDataP2 = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP2.TimeTool + peaksRawDataP2.StageDelay*1e15, RowWOffset = peaksRawDataP2.RowlandY - peaksRawDataP2.Offset)
peaksProDataP2.makeProPeaks(peaksRawDataP2, NumTTSteps, MinTime, MaxTime, FPlots)



#minus data


if ReEnterData:

    FileNumsM = list(range(180,188+1))
    #FileNumsM = list(range(131, 140+1))
    #FileNumsM.remove(FileNumsM[removenum])
    peaksRawDataM = loadData(FileNumsM, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataM.pkl", "rb") as f:
        peaksRawDataM = pickle.load(f)
    
    with open(folder + "FileNumsM.pkl", "rb") as f:
        FileNumsM = pickle.load(f)

peaksProDataM = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15, RowWOffset = peaksRawDataM.RowlandY - peaksRawDataM.Offset)
peaksProDataM.makeProPeaks(peaksRawDataM, NumTTSteps, MinTime, MaxTime, FPlots)





TCentersP = (peaksProDataP.TimeSteps[:-1]+peaksProDataP.TimeSteps[1:])/2
TCentersP2 = (peaksProDataP2.TimeSteps[:-1]+peaksProDataP2.TimeSteps[1:])/2
TCentersM = (peaksProDataM.TimeSteps[:-1]+peaksProDataM.TimeSteps[1:])/2
#Fit1, Fit2, params, info = fitXES(TCentersP, TCentersM, peaksProDataP.XESDiff, peaksProDataM.XESDiff, -1534, True)
Fit1, Fit2, params, info = fitXESthree(TCentersP, TCentersM, TCentersP2, peaksProDataP.XESDiff, peaksProDataM.XESDiff, peaksProDataP2.XESDiff, -1534, FPlots)

t0 = params[3]

folder_con = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
with open(folder_con + "t0.pkl", "wb") as f:
        pickle.dump(t0, f)





peaksProDataPF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP.TimeTool + peaksRawDataP.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP.RowlandY - peaksRawDataP.Offset)
#peaksProDataPF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP.TimeTool + peaksRawDataP.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP.RowlandY)
peaksProDataPF.makeProPeaks(peaksRawDataP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataPF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsP2[0], True)*1000,1))
TCentersPF = (peaksProDataPF.TimeSteps[:-1]+peaksProDataPF.TimeSteps[1:])/2



peaksProDataP2F = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP2.TimeTool + peaksRawDataP2.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP2.RowlandY - peaksRawDataP2.Offset)
#peaksProDataP2F = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP2.TimeTool + peaksRawDataP2.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP2.RowlandY)
peaksProDataP2F.makeProPeaks(peaksRawDataP2, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataP2F.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsP[0], True)*1000,1))
TCentersP2F = (peaksProDataP2F.TimeSteps[:-1]+peaksProDataP2F.TimeSteps[1:])/2



peaksProDataMF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15 - t0, RowWOffset = peaksRawDataM.RowlandY - peaksRawDataM.Offset)
#peaksProDataMF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15 - t0, RowWOffset = peaksRawDataM.RowlandY)
peaksProDataMF.makeProPeaks(peaksRawDataM, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataMF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsM[0], True)*1000,1))
TCentersMF = (peaksProDataMF.TimeSteps[:-1]+peaksProDataMF.TimeSteps[1:])/2







#makeTimePlot(TCentersPF, TCentersMF, peaksProDataPF, peaksProDataMF, MinTimePlots, MaxTimePlots, FPlots)
params, cov, Freq, FTp, FTm, FTp2 = makeTimePlotThree(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF, peaksProDataP2F, peaksProDataMF, MinTimePlots, MaxTimePlots, 0, FPlots, True)


FT, Freq, params = makeOneBootFT(TCentersPF, peaksProDataPF, MinTimePlots, MaxTimePlots, 0.02, 60, 30, True, FPlots)

FT, Freq, params = makeOneBootFT(TCentersP2F, peaksProDataP2F, MinTimePlots, MaxTimePlots, 0.02, 60, 30, True, FPlots)

FT, Freq, params = makeOneBootFT(TCentersMF, peaksProDataMF, MinTimePlots, MaxTimePlots, 0.02, 60, 30, False, FPlots)




if Boot:
    
    peaksRawBootP = MakeRawBoot(peaksRawDataP)
    peaksRawBootP2 = MakeRawBoot(peaksRawDataP2)
    peaksRawBootM = MakeRawBoot(peaksRawDataM)
        
    peaksProDataPF_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootP.TimeTool + peaksRawBootP.StageDelay*1e15 - t0, RowWOffset = peaksRawBootP.RowlandY - peaksRawBootP.Offset)
    peaksProDataPF_boot.makeProPeaks(peaksRawBootP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
    
    peaksProDataP2F_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootP2.TimeTool + peaksRawBootP2.StageDelay*1e15 - t0, RowWOffset = peaksRawBootP2.RowlandY - peaksRawBootP2.Offset)
    peaksProDataP2F_boot.makeProPeaks(peaksRawBootP2, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
    
    peaksProDataMF_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootM.TimeTool + peaksRawBootM.StageDelay*1e15 - t0, RowWOffset = peaksRawBootM.RowlandY - peaksRawBootM.Offset)
    peaksProDataMF_boot.makeProPeaks(peaksRawBootM, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
    
    PeaksBootP = np.empty((np.shape(TCentersPF)[0],numBoot))
    PeaksBootP2 = np.empty((np.shape(TCentersP2F)[0],numBoot))
    PeaksBootM = np.empty((np.shape(TCentersMF)[0],numBoot))
    
    BET = np.empty(numBoot)
    IRF = np.empty(numBoot)
    
    
    params, cov, Freq, FTp, FTm, FTp2 = makeTimePlotThree(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, False)
    
    
    FTBootP = np.empty((np.shape(Freq)[0],numBoot))
    FTBootP2 = np.empty((np.shape(Freq)[0],numBoot))
    FTBootM = np.empty((np.shape(Freq)[0],numBoot))
    
    for ii in range(numBoot):

        peaksRawBootP = MakeRawBoot(peaksRawDataP)
        peaksRawBootP2 = MakeRawBoot(peaksRawDataP2)
        peaksRawBootM = MakeRawBoot(peaksRawDataM)
            
        peaksProDataPF_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootP.TimeTool + peaksRawBootP.StageDelay*1e15 - t0, RowWOffset = peaksRawBootP.RowlandY - peaksRawBootP.Offset)
        peaksProDataPF_boot.makeProPeaks(peaksRawBootP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
        
        peaksProDataP2F_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootP2.TimeTool + peaksRawBootP2.StageDelay*1e15 - t0, RowWOffset = peaksRawBootP2.RowlandY - peaksRawBootP2.Offset)
        peaksProDataP2F_boot.makeProPeaks(peaksRawBootP2, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
        
        peaksProDataMF_boot = PDC.PeaksProcessedData(Delay = 1000*peaksRawBootM.TimeTool + peaksRawBootM.StageDelay*1e15 - t0, RowWOffset = peaksRawBootM.RowlandY - peaksRawBootM.Offset)
        peaksProDataMF_boot.makeProPeaks(peaksRawBootM, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)

        
        PeaksBootP[:,ii] = peaksProDataPF_boot.XESDiff
        PeaksBootP2[:,ii] = peaksProDataP2F_boot.XESDiff
        PeaksBootM[:,ii] = peaksProDataMF_boot.XESDiff
        
        
        params, cov, Freq, FTp, FTm, FTp2 = makeTimePlotThree(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, False)
        
        BET[ii] = params[2]*math.log(2)
        IRF[ii] = params[4]
        
        
        FTBootP[:,ii] = abs(FTp)
        FTBootP2[:,ii] = abs(FTp2)
        FTBootM[:,ii] = abs(FTm)
    
    PeaksBootPF = np.mean(PeaksBootP,1)
    PeaksBootPE = np.std(PeaksBootP,1)
    FTBootPF = np.mean(FTBootP,1)
    FTBootPE = np.std(FTBootP,1)
    
    
    PeaksBootP2F = np.mean(PeaksBootP2,1)
    PeaksBootP2E = np.std(PeaksBootP2,1)
    FTBootP2F = np.mean(FTBootP2,1)
    FTBootP2E = np.std(FTBootP2,1)
    
    
    PeaksBootMF = np.mean(PeaksBootM,1)
    PeaksBootME = np.std(PeaksBootM,1)
    FTBootMF = np.mean(FTBootM,1)
    FTBootME = np.std(FTBootM,1)
    
    BETF = np.mean(BET)
    BETE = np.std(BET)
    
    IRFF = np.mean(IRF)
    IRFE = np.std(IRF)
    
    peaksProDataPF_boot.changeValue(XESDiff = PeaksBootPF, XESDiffE = PeaksBootPE, FT = FTBootPF, FTE = FTBootPE, Freq = Freq, EnergyLabel = peaksProDataPF.EnergyLabel)
    peaksProDataP2F_boot.changeValue(XESDiff = PeaksBootP2F, XESDiffE = PeaksBootP2E, FT = FTBootP2F, FTE = FTBootP2E, Freq = Freq, EnergyLabel = peaksProDataP2F.EnergyLabel)
    peaksProDataMF_boot.changeValue(XESDiff = PeaksBootMF, XESDiffE = PeaksBootME, FT = FTBootMF, FTE = FTBootME, Freq = Freq, EnergyLabel = peaksProDataMF.EnergyLabel)
    
    makeTimePlotThreeError(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 0, FPlots, True)
    makeTimePlotThree(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF_boot, peaksProDataP2F_boot, peaksProDataMF_boot, MinTimePlots, MaxTimePlots, 300, FPlots, True)
    
"""        
    if True:
        
        plt.figure()
        plt.plot(xasProData_one.EnergyPlot, XASDiffBoot)
        
    plt.figure()
    plt.errorbar(xasProData_one.EnergyPlot, XASDiffBootF, XASDiffBootE)
    
    Fit,Params,ParamsA,ParamsB,cov,info = \
        fitXASPiecewiseLor(xasProData_one.EnergyPlot, XASDiffBootF, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)

    with open(folder + "PeaksBootF.pkl", "wb") as f:
        pickle.dump(PeaksBootF, f)
        
    with open(folder + "PeaksBootE.pkl", "wb") as f:
        pickle.dump(PeaksBootE, f)
        
    with open(folder + "FTBootF.pkl", "wb") as f:
        pickle.dump(FTBootF, f)
        
    with open(folder + "FTBootE.pkl", "wb") as f:
        pickle.dump(FTBootE, f)

else:
    
    with open(folder + "XASDiffBootF.pkl", "rb") as f:
        XASDiffBootF = pickle.load(f)
        
    with open(folder + "XASDiffBootE.pkl", "rb") as f:
        XASDiffBootE = pickle.load(f)
        
    Fit,Params,ParamsA,ParamsB,covA,covB = \
        fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBootF, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)

"""





if SaveData:
        
    with open(folder + "peaksRawDataP.pkl", "wb") as f:
        pickle.dump(peaksRawDataP, f)
        
    with open(folder + "peaksRawDataM.pkl", "wb") as f:
        pickle.dump(peaksRawDataM, f)
            
    with open(folder + "peaksProDataPF.pkl", "wb") as f:
        pickle.dump(peaksProDataPF, f)
        
    with open(folder + "peaksProDataMF.pkl", "wb") as f:
        pickle.dump(peaksProDataMF, f)
        
    with open(folder + "FileNumsM.pkl", "wb") as f:
        pickle.dump(FileNumsM, f)
        
    with open(folder + "FileNumsP.pkl", "wb") as f:
        pickle.dump(FileNumsP, f)
        
    with open(folder + "peaksRawDataP2.pkl", "wb") as f:
        pickle.dump(peaksRawDataP2, f)
            
    with open(folder + "peaksProDataP2F.pkl", "wb") as f:
        pickle.dump(peaksProDataP2F, f)

    with open(folder + "FileNumsP2.pkl", "wb") as f:
        pickle.dump(FileNumsP, f)









