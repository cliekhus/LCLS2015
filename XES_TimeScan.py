# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from makeFilter import makeFilter
from loadData import loadData
from makeXES import makeXES
from fitXES import fitXES
from fittingfunctions import convolved
from scipy.signal import savgol_filter

ReEnterData = False
FPlots = False

NumTTSteps = 200
NumTTStepsPlots = 50

TTSteps = np.linspace(-2000,0,NumTTSteps+1)






#plus data

if ReEnterData:

    #FileNums = [180]+ list(range(182,188+1))
    FileNums = list(range(155, 158+1)) + list(range(160, 164+1))
    XOnp, LOnp, StageDelayp, Diode2p, Ipm2Sump, DiodeIpmSlopep, TimeToolp, TTAmpp, TTFWHMp, ScanNump, RowlandYp, RowOffsetp = loadData(FileNums, False)

RowlandWOffsetp = [x-y for x,y in zip(RowlandYp, RowOffsetp)]

Filterp, IpmOffsetp = makeFilter(Diode2p, Ipm2Sump, RowlandWOffsetp, XOnp, LOnp, DiodeIpmSlopep, TimeToolp, TTAmpp, TTFWHMp, FPlots, ScanNump, 2)

IpmWOffsetp = [x-IpmOffsetp for x in Diode2p]

TTDelayp = [(x*1e-12 + y)*1e15 for x,y in zip(TimeToolp,StageDelayp)]

XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTSteps, IpmWOffsetp, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelayp, TTSteps, FPlots)

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii+1])/2]
    
XESDiffplus = [(x-XESOff_Normp)*1000/XESOff_Normp for x in XESOn_Normp]









#minus data

if ReEnterData:

    FileNums = [180]+ list(range(182,188+1))
    #FileNums = list(range(155, 158+1)) + list(range(160, 164+1))
    XOnm, LOnm, StageDelaym, Diode2m, Ipm2Summ, DiodeIpmSlopem, TimeToolm, TTAmpm, TTFWHMm, ScanNumm, RowlandYm, RowOffsetm = loadData(FileNums, False)

RowlandWOffsetm = [x-y for x,y in zip(RowlandYm, RowOffsetm)]

Filterm, IpmOffsetm = makeFilter(Diode2m, Ipm2Summ, RowlandWOffsetm, XOnm, LOnm, DiodeIpmSlopem, TimeToolm, TTAmpm, TTFWHMm, FPlots, ScanNumm, 2)

IpmWOffsetm = [x-IpmOffsetm for x in Diode2m]

TTDelaym = [(x*1e-12 + y)*1e15 for x,y in zip(TimeToolm,StageDelaym)]

XESOn_Normm, XESOff_Normm, Num_Onm, Num_Offm, NormFactor_Offm, NormFactor_Onm = makeXES(NumTTSteps, IpmWOffsetm, RowlandWOffsetm, Filterm, LOnm, XOnm, TTDelaym, TTSteps, FPlots)

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii+1])/2]
    
XESDiffminus = [(x-XESOff_Normm)*1000/XESOff_Normm for x in XESOn_Normm]








Fit1, Fit2, params, info = fitXES(TCenters, XESDiffplus, XESDiffminus, -1534, FPlots)

t0 = params[4]


TTDelaypp = [x-t0 for x in TTDelayp]
TTDelaymp = [x-t0 for x in TTDelaym]



TTSteps = np.linspace(-150, 1500, NumTTStepsPlots+1)

XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTStepsPlots, IpmWOffsetp, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelaypp, TTSteps, FPlots)
XESDiffplus = [(x-XESOff_Normp)*1000/XESOff_Normp for x in XESOn_Normp]

XESOn_Normm, XESOff_Normm, Num_Onm, Num_Offm, NormFactor_Offm, NormFactor_Onm = makeXES(NumTTStepsPlots, IpmWOffsetm, RowlandWOffsetm, Filterm, LOnm, XOnm, TTDelaymp, TTSteps, FPlots)
XESDiffminus = [(x-XESOff_Normm)*1000/XESOff_Normm for x in XESOn_Normm]









TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii])/2]


Fitp, Fitm, params, info = fitXES(TCenters, XESDiffplus, XESDiffminus, 0, FPlots)

tt = np.linspace(-150,800,1000)

plt.figure()
plt.plot(TCenters, XESDiffplus, 'o')
plt.plot(tt, convolved(tt, params[0], params[1], params[4], params[5]))
plt.plot(TCenters, XESDiffminus, 'x')
plt.plot(tt, convolved(tt, params[2], params[3], params[4], params[5]))

plt.ylabel('$\Delta$ T x 10$^3$')
plt.xlabel('time delay (fs)')

plt.figure()
plt.plot(TCenters, savgol_filter(XESDiffplus,7,2), 'o')
plt.plot(tt, convolved(tt, params[0], params[1], params[4], params[5]))
plt.plot(TCenters, savgol_filter(XESDiffminus,7,2), 'x')
plt.plot(tt, convolved(tt, params[2], params[3], params[4], params[5]))
plt.title('smoothed')


Residualp = [x-y for x,y,z in zip(XESDiffplus,Fitp,TCenters) if z>200]
Residualm = [x-y for x,y,z in zip(XESDiffminus,Fitm,TCenters) if z>200]

#Residualp = [x-y for x,y,z in zip(savgol_filter(XESDiffplus,7,2),Fitp,TCenters) if z>200]
#Residualm = [x-y for x,y,z in zip(savgol_filter(XESDiffminus,7,2),Fitm,TCenters) if z>200]

TCP = [x for x in TCenters if x>200]

plt.figure()
plt.plot(TCP, Residualp, 'o')
plt.plot(TCP, Residualm, 'x')

FTp = np.fft.rfft(Residualp)
FTm = np.fft.rfft(Residualm)

Freq = np.fft.rfftfreq(len(Residualp), d=(TCenters[0]-TCenters[1])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
plt.plot(Freq, abs(FTp))
plt.plot(Freq, abs(FTm))