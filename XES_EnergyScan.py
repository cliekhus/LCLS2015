"""
XES time scan

"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from itertools import compress

fileNums = list(range(371,395+1))

NumTTSteps_ES = 100
NumTTStepsPlots_ES = NumTTSteps_ES

if False:
    
    XOn = []
    LOn = []
    XEnergy = []
    TimeTool = []
    RowlandY = []
    Ipm2Sum = []
    
    for fileNum in fileNums:
        
        ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(fileNum) + '.h5')
        
        XOn = XOn + list(map(bool, ScanName['/lightStatus/xray']))
        LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
        RowlandY = RowlandY + list(ScanName['/Rowland/ROI_proj_ythres'])
        XEnergy = XEnergy + [round(x,4) for x in list(ScanName['/scan/var0'])]
        TimeTool = TimeTool + list(ScanName['/ttCorr/tt'])
        Ipm2Sum = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these

TTDelay = [x*1000 for x in TimeTool]

TTSteps = np.linspace(min(TTDelay),max(TTDelay),NumTTSteps_ES+1)

XES = []
NumCounts = []
Intensity = []
DelayTime = []
Peak = []

for ii in range(len(TTSteps)-1):
    
    ttfilter = [a and b and c and d for a,b,c,d in zip(TTDelay > TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn)]
    numshots = sum([int(a) for a in ttfilter])
    
    if numshots > 100:
        xes = [sum(list(compress(RowlandY, ttfilter)))]
        XES = XES + xes
        NumCounts = NumCounts + [sum([int(x) for x in ttfilter])]
        intensity = [sum(list(compress(Ipm2Sum, ttfilter)))]
        Intensity = Intensity + intensity
        DelayTime = DelayTime + [(TTSteps[ii]+TTSteps[ii+1])/2]
        xesp = xes[0]
        Peak = Peak + [xesp[71]/intensity[0]]
    
XESNorm = [x/y for x,y in zip(XES, Intensity)]

plt.figure()
plt.contour(XESNorm[:20])

plt.figure()
plt.plot(DelayTime, Peak, marker='.')