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
from makeTimePlot import makeBootFT
import numpy as np
import random


folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = False
Boot = True
numBoot = 1

NumTTSteps = 100
NumTTStepsPlots = 65

MinTime = -2000 
MaxTime = 0

MinTimePlots = -500
MaxTimePlots = 1500

removenum = 9

#plus data

if ReEnterData:

    #FileNumsP = list(range(144, 154+1))
    #FileNumsP = list(range(131, 140+1))
    FileNumsP = list(range(165, 178+1))
    #FileNumsP = list(range(123, 130+1))
    #FileNumsP = list(range(155,164+1))
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

    FileNumsP2 = list(range(123, 130+1))
    #FileNumsP2.remove(FileNumsP2[removenum])
    peaksRawDataP2 = loadData(FileNumsP2, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataP.pkl", "rb") as f:
        peaksRawDataP2 = pickle.load(f)
        
    with open(folder + "FileNumsP.pkl", "rb") as f:
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
peaksProDataPF.makeProPeaks(peaksRawDataP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataPF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsP2[0], True)*1000,1))
TCentersPF = (peaksProDataPF.TimeSteps[:-1]+peaksProDataPF.TimeSteps[1:])/2



peaksProDataP2F = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP2.TimeTool + peaksRawDataP2.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP2.RowlandY - peaksRawDataP2.Offset)
peaksProDataP2F.makeProPeaks(peaksRawDataP2, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataP2F.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsP[0], True)*1000,1))
TCentersP2F = (peaksProDataP2F.TimeSteps[:-1]+peaksProDataP2F.TimeSteps[1:])/2



peaksProDataMF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15 - t0, RowWOffset = peaksRawDataM.RowlandY - peaksRawDataM.Offset)
peaksProDataMF.makeProPeaks(peaksRawDataM, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataMF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsM[0], True)*1000,1))
TCentersMF = (peaksProDataMF.TimeSteps[:-1]+peaksProDataMF.TimeSteps[1:])/2







makeTimePlot(TCentersPF, TCentersMF, peaksProDataPF, peaksProDataMF, MinTimePlots, MaxTimePlots, FPlots)
#makeTimePlotThree(TCentersPF, TCentersP2F, TCentersMF, peaksProDataPF, peaksProDataP2F, peaksProDataMF, MinTimePlots, MaxTimePlots, 0, FPlots)









if Boot:
    
    peaksProDataPF_boot = peaksProDataPF
    
    PeaksBoot = np.empty((np.shape(TCentersPF)[0],numBoot))
    
    TT = np.matlib.repmat(True,1,int((np.shape(peaksRawDataP.XOn)[0])/2))
    FF = np.matlib.repmat(False,1,int((np.shape(peaksRawDataP.XOn)[0])/2))
    TF = np.concatenate((TT,FF))

    TF = TF.flatten()    
    
    FTp, FTm, Freq = makeBootFT(TCentersPF, TCentersMF, peaksProDataPF_boot.XESDiff, peaksProDataMF.XESDiff, MinTimePlots, MaxTimePlots, FPlots)
    FTBoot = np.empty((np.shape(Freq)[0],numBoot))
    
    for ii in range(numBoot):

        random.shuffle(TF)  
        
        peaksProDataPF_boot.makeBootPeaks(peaksRawDataP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, TF, FPlots)
        
        PeaksBoot[:,ii] = peaksProDataPF_boot.XESDiff
        
        FTp, FTm, Freq = makeBootFT(TCentersPF, TCentersMF, peaksProDataPF_boot.XESDiff, peaksProDataMF.XESDiff, MinTimePlots, MaxTimePlots, FPlots)
        
        FTBoot[:,ii] = abs(FTp)
    
    PeaksBootF = np.mean(PeaksBoot,1)
    PeaksBootE = np.std(PeaksBoot,1)
    FTBootF = np.mean(FTBoot,1)
    FTBootE = np.std(FTBoot,1)
"""        
    if True:
        
        plt.figure()
        plt.plot(xasProData_one.EnergyPlot, XASDiffBoot)
        
    plt.figure()
    plt.errorbar(xasProData_one.EnergyPlot, XASDiffBootF, XASDiffBootE)
    
    Fit,Params,ParamsA,ParamsB,cov,info = \
        fitXASPiecewiseLor(xasProData_one.EnergyPlot, XASDiffBootF, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)

    with open(folder + "XASDiffBootF.pkl", "wb") as f:
        pickle.dump(XASDiffBootF, f)
        
    with open(folder + "XASDiffBootE.pkl", "wb") as f:
        pickle.dump(XASDiffBootE, f)

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









