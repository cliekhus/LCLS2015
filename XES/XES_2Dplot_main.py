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
from makeTimePlot import makeOneBootFT
from fitXES import fitOneXES
import numpy as np
import random
import matplotlib.pyplot as plt


folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = False
Boot = True
numBoot = 100

NumTTSteps = 100
NumTTStepsPlots = 65

MinTime = -2000 
MaxTime = 0

MinTimePlots = -500
MaxTimePlots = 1500

removenum = 9

#plus data


FileNums = [list(range(123, 130+1))]
FileNums.append(list(range(144, 154+1)))
FileNums.append(list(range(180,188+1)))
FileNums.append(list(range(131,140+1)))
#FileNums.append(list(range(165,178+1)))
FileNums.append(list(range(155,164+1)))

starta = [0.02, 0.009, -0.02, -0.02, 0.02]
startrate = [59, 60, 60, 60, 60]
startsig = [6, 6, 8, 6, 6]

for ii in range(len(FileNums)):
        
    if ReEnterData:
    
        peaksRawData = loadData(FileNums[ii], "Peaks", 1)
        
    if ReLoadData:
    
        with open(folder + "peaksRawDataP.pkl", "rb") as f:
            peaksRawData = pickle.load(f)
            
        with open(folder + "FileNumsP.pkl", "rb") as f:
            FileNumsP = pickle.load(f)
    
    
    
    
           
    if ii == 0:

        peaksProData = PDC.PeaksProcessedData(Delay = 1000*peaksRawData.TimeTool + peaksRawData.StageDelay*1e15, RowWOffset = peaksRawData.RowlandY - peaksRawData.Offset)
        peaksProData.makeProPeaks(peaksRawData, NumTTSteps, MinTime, MaxTime, FPlots)
        TCenters = (peaksProData.TimeSteps[:-1]+peaksProData.TimeSteps[1:])/2
        Fit, params, info = fitOneXES(TCenters, peaksProData.XESDiff, -1534, starta[0], startrate[0], startsig[0], True)
        t0 = params[2]
        
    peaksProData = PDC.PeaksProcessedData(Delay = 1000*peaksRawData.TimeTool + peaksRawData.StageDelay*1e15 - t0, RowWOffset = peaksRawData.RowlandY - peaksRawData.Offset)
    peaksProData.makeProPeaks(peaksRawData, NumTTStepsPlots, MinTimePlots, MaxTimePlots,  FPlots)
    TCenters = (peaksProData.TimeSteps[:-1]+peaksProData.TimeSteps[1:])/2
    peaksProData.changeValue(EnergyLabel = round(convertAngle2Energy(FileNums[ii][0], True)*1000,1))
        
    
    
    
    
    

    
    if Boot:
        
        peaksProData_boot = peaksProData
        
        PeaksBoot = np.empty((np.shape(TCenters)[0],numBoot))
        
        TT = np.matlib.repmat(True,1,int((np.shape(peaksRawData.XOn)[0])/2))
        FF = np.matlib.repmat(False,1,int((np.shape(peaksRawData.XOn)[0])/2))
        TF = np.concatenate((TT,FF))
    
        TF = TF.flatten()    
        
        try:
            FT, Freq = makeOneBootFT(TCenters, peaksProData_boot.XESDiff, MinTimePlots, MaxTimePlots, starta[ii], startrate[ii], startsig[ii], True)
        except:
            FT, Freq = makeOneBootFT(TCenters, peaksProData_boot.XESDiff, MinTimePlots, MaxTimePlots, starta[ii]*.9, startrate[ii]*.9, startsig[ii]*.9, True)
            
        FTBoot = np.empty((np.shape(Freq)[0],numBoot))
        
        for jj in range(numBoot):
    
            random.shuffle(TF)  
            
            peaksProData_boot.makeBootPeaks(peaksRawData, NumTTStepsPlots, MinTimePlots, MaxTimePlots, TF, FPlots)
            
            PeaksBoot[:,jj] = peaksProData_boot.XESDiff
            
            try:
                FT, Freq = makeOneBootFT(TCenters, peaksProData_boot.XESDiff, MinTimePlots, MaxTimePlots, starta[ii], startrate[ii], startsig[ii], FPlots)
            except:
                FT, Freq = makeOneBootFT(TCenters, peaksProData_boot.XESDiff, MinTimePlots, MaxTimePlots, starta[ii]*.9, startrate[ii]*.9, startsig[ii]*.9, True)
            
            FTBoot[:,jj] = abs(FT)
        
        PeaksBootF = np.mean(PeaksBoot,1)
        PeaksBootE = np.std(PeaksBoot,1)
        FTBootF = np.mean(FTBoot,1)
        FTBootE = np.std(FTBoot,1)
        
        if ii == 0:
            
            XESMat = np.empty((np.shape(PeaksBootF)[0],len(FileNums)))
            XESEMat = np.empty((np.shape(PeaksBootE)[0],len(FileNums)))
            FTMat = np.empty((np.shape(FTBootF)[0],len(FileNums)))
            FTEMat = np.empty((np.shape(FTBootE)[0],len(FileNums)))
            EnergyMat = np.empty(len(FileNums))
            
            FreqMat = Freq
            
        XESMat[:,ii] = PeaksBootF
        XESEMat[:,ii] = PeaksBootE
        FTMat[:,ii] = FTBootF
        FTEMat[:,ii] = FTBootE
        EnergyMat[ii] = peaksProData.EnergyLabel
        
        
index = np.argsort(EnergyMat)
EnergyMat = EnergyMat[index]
XESMat = XESMat[:,index]
XESEMat = XESEMat[:,index]
FTMat = FTMat[:,index]
FTEMat = FTEMat[:,index]




with open(folder + "EnergyMat.pkl", "wb") as f:
    pickle.dump(EnergyMat, f)
    
with open(folder + "XESMat.pkl", "wb") as f:
    pickle.dump(XESMat, f)
    
with open(folder + "XESEMat.pkl", "wb") as f:
    pickle.dump(XESEMat, f)
    
with open(folder + "FTMat.pkl", "wb") as f:
    pickle.dump(FTMat, f)
    
with open(folder + "FTEMat.pkl", "wb") as f:
    pickle.dump(FTEMat, f)


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

"""







