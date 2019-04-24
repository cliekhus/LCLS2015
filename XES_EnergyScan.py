"""
XES energy scan - k beta

"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from itertools import compress
from matplotlib.widgets import Cursor

fileNums = list(range(371,395+1))
#+list(range(376,377+1))

NumTTSteps_ES = 1
NumTTStepsPlots_ES = NumTTSteps_ES

XOn = []
LOn = []
XEnergy = []
TimeTool = []
RowlandY_sum = []
RowlandX_sum = []

for fileNum in fileNums:
    
    ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(fileNum) + '.h5')
    
    XOn = XOn + list(map(bool, ScanName['/lightStatus/xray']))
    LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
    RowlandY_sum = RowlandY_sum + [sum(y) for y in list(ScanName['/Rowland/ROI_proj_ythres'])]
    XEnergy = XEnergy + [round(x,4) for x in list(ScanName['/scan/var0'])]
    TimeTool = TimeTool + list(ScanName['/ttCorr/tt'])

TTDelay_ES = [x*1000 for x in TimeTool]

TTSteps = np.linspace(min(TTDelay_ES),max(TTDelay_ES),NumTTSteps_ES+1)

UniXEnergy = np.unique(XEnergy)

XESOn = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
XESOff = [0 for x in range(len(UniXEnergy))]

On_NumScan = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
Off_NumScan = [0 for x in range(len(UniXEnergy))]

for jj in range(len(UniXEnergy)):
    
    SelectedRuns = list(a and b for a,b in zip(XOn, (XEnergy == UniXEnergy[jj])))
    
    Off = list(not a and b for a,b in zip(LOn, SelectedRuns))
    XESOff[jj] = sum(list(compress(RowlandY_sum, Off)))
    
    Off_NumScan[jj] = sum([int(x) for x in Off])
    
    for ii in range(len(TTSteps)-1):
        
        On = list(a and b and c and d for a,b,c,d in zip(LOn, SelectedRuns, (TTDelay_ES >= TTSteps[ii]), (TTDelay_ES < TTSteps[ii+1])))
        XESOn[ii][jj] = sum(list(compress(RowlandY_sum, On)))
        
        On_NumScan[ii][jj] = sum([int(x) for x in On])

fig = plt.figure()
ax = fig.add_subplot(111)

XESOn_Norm = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]

for ii in range(NumTTStepsPlots_ES):

    XESOn_Norm[ii] = [a/b for a,b in zip(XESOn[ii], On_NumScan[ii])]
    plt.plot(UniXEnergy, XESOn_Norm[ii])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('summed k alpha radiation intensity')
plt.title('Laser On')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

XESOff_Norm = [a/b for a,b in zip(XESOff, Off_NumScan)]

plt.figure()
ax = fig.add_subplot(111)
plt.plot(UniXEnergy, XESOff_Norm)
plt.xlabel('x-ray energy (keV)')
plt.ylabel('summed k alpha radiation intensity')
plt.title('Laser Off')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

plt.figure()
ax = fig.add_subplot(111)

for ii in range(NumTTStepsPlots_ES):
    
    plt.plot(UniXEnergy, [a - b for a,b, in zip(XESOn_Norm[ii], XESOff_Norm)])
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in k alpha radiation (on-off)')
plt.title('raw data')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

plt.figure()
ax = fig.add_subplot(111)

for ii in range(NumTTStepsPlots_ES):
    
    plt.plot(UniXEnergy, [a/sum(XESOn_Norm[ii]) - b/sum(XESOff_Norm) for a,b, in zip(XESOn_Norm[ii], XESOff_Norm)])
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in k alpha radiation (on-off), extra norm')
plt.title('raw data')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)
