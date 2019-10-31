# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""


from loadData import loadData
from fitXES import fitXES
from APSXESCalibration import convertAngle2Energy
import pickle
import ProcessedDataClass as PDC
from makeTimePlot import makeTimePlot


folder = "D://LCLS_Data/LCLS_python_data/XES_TimeResolved/"
ReEnterData = False
FPlots = False
ReLoadData = True
SaveData = False

NumTTSteps = 100
NumTTStepsPlots = 65

MinTime = -2000
MaxTime = 0

MinTimePlots = -500
MaxTimePlots = 1500


#plus data

if ReEnterData:

    FileNumsP = list(range(143, 154+1))
    #FileNumsP = list(range(155, 164+1))
    #FileNumsP = list(range(155, 155+1))
    #FileNumsP = list(range(122, 130+1))+list(range(143, 154+1))
    peaksRawDataP = loadData(FileNumsP, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataP.pkl", "rb") as f:
        peaksRawDataP = pickle.load(f)
        
    with open(folder + "FileNumsP.pkl", "rb") as f:
        FileNumsP = pickle.load(f)

peaksProDataP = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP.TimeTool + peaksRawDataP.StageDelay*1e15, RowWOffset = peaksRawDataP.RowlandY - peaksRawDataP.Offset)
peaksProDataP.makeProPeaks(peaksRawDataP, NumTTSteps, MinTime, MaxTime, FPlots)




#minus data


if ReEnterData:

    #FileNumsM = list(range(180,188+1))
    FileNumsM = list(range(180,180+1))
    
    peaksRawDataM = loadData(FileNumsM, "Peaks", 1)
    
if ReLoadData:

    with open(folder + "peaksRawDataM.pkl", "rb") as f:
        peaksRawDataM = pickle.load(f)
    
    with open(folder + "FileNumsM.pkl", "rb") as f:
        FileNumsM = pickle.load(f)

peaksProDataM = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15, RowWOffset = peaksRawDataM.RowlandY - peaksRawDataM.Offset)
peaksProDataM.makeProPeaks(peaksRawDataM, NumTTSteps, MinTime, MaxTime, FPlots)





TCentersP = (peaksProDataP.TimeSteps[:-1]+peaksProDataP.TimeSteps[1:])/2
TCentersM = (peaksProDataM.TimeSteps[:-1]+peaksProDataM.TimeSteps[1:])/2
Fit1, Fit2, params, info = fitXES(TCentersP, TCentersM, peaksProDataP.XESDiff, peaksProDataM.XESDiff, -1534, FPlots)

t0 = params[3]

folder_con = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
with open(folder_con + "t0.pkl", "wb") as f:
        pickle.dump(t0, f)






peaksProDataPF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataP.TimeTool + peaksRawDataP.StageDelay*1e15 - t0, RowWOffset = peaksRawDataP.RowlandY - peaksRawDataP.Offset)
peaksProDataPF.makeProPeaks(peaksRawDataP, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataPF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsP[0], True)*1000,1))
TCentersPF = (peaksProDataPF.TimeSteps[:-1]+peaksProDataPF.TimeSteps[1:])/2





peaksProDataMF = PDC.PeaksProcessedData(Delay = 1000*peaksRawDataM.TimeTool + peaksRawDataM.StageDelay*1e15 - t0, RowWOffset = peaksRawDataM.RowlandY - peaksRawDataM.Offset)
peaksProDataMF.makeProPeaks(peaksRawDataM, NumTTStepsPlots, MinTimePlots, MaxTimePlots, FPlots)
peaksProDataMF.changeValue(EnergyLabel = round(convertAngle2Energy(FileNumsM[0], True)*1000,1))
TCentersMF = (peaksProDataMF.TimeSteps[:-1]+peaksProDataMF.TimeSteps[1:])/2




makeTimePlot(TCentersPF, TCentersMF, peaksProDataPF, peaksProDataMF, MinTimePlots, MaxTimePlots, FPlots)





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









