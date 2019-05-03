"""
XES time scan

"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from itertools import compress
import math

fileNums = list(range(373,395+1))

NumTTSteps_ES = 50
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
        Ipm2Sum = Ipm2Sum + [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these

TTDelay = [x*1000 for x in TimeTool]

TTSteps = np.linspace(-2e3,2e3,NumTTSteps_ES+1)

XES = []
NumCounts = []
Intensity = []
DelayTime = []
Peak1 = []
Peak2 = []

nancheck = [not a and not b for a,b in zip([math.isnan(sum(x)) for x in RowlandY], [math.isnan(x) for x in Ipm2Sum])]

pickenergy = [x > 0 for x in XEnergy]

for ii in range(len(TTSteps)-1):
    
    ttfilter = [a and b and c and d and e and f for a,b,c,d,e,f in zip(TTDelay > TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn, nancheck, pickenergy)]
    #ttfilter = [a and b and c and d for a,b,c,d in zip(TTDelay > TTSteps[ii], TTDelay < TTSteps[ii+1], XOn, LOn)]
    numshots = sum([int(a) for a in ttfilter])
    
    print(numshots)
    
    if numshots > 0:
        xes = [sum(list(compress(RowlandY, ttfilter)))]
        XES = XES + xes
        NumCounts = NumCounts + [sum([int(x) for x in ttfilter])]
        intensity = [sum(list(compress(Ipm2Sum, ttfilter)))]
        Intensity = Intensity + intensity
        DelayTime = DelayTime + [(TTSteps[ii]+TTSteps[ii+1])/2]
        xesp = xes[0]
        Peak1 = Peak1 + [xesp[71]]
        Peak2 = Peak2 + [xesp[36]]
    
XESNorm = [x/y for x,y in zip(XES, Intensity)]

ttfilteroff = [a and not b and c and d for a,b,c,d in zip(XOn, LOn, nancheck, pickenergy)]

plt.figure()
plt.plot(sum(list(compress(RowlandY, ttfilteroff))))

plt.figure()
plt.plot(DelayTime, Peak1, marker='.')

plt.figure()
plt.plot(DelayTime, Peak2, marker='.')