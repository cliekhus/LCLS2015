# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from makeOneFilter import makeOneFilter
from loadData import loadData
from makeXES import makeXES
from fitXES import fitXES
from fittingfunctions import convolved
from scipy.signal import savgol_filter
from APSXESCalibration import convertAngle2Energy
import pickle

ReEnterData = True
FPlots = False

NumTTSteps = 100
NumTTStepsPlots = 50

TTSteps = np.linspace(-2000,0,NumTTSteps+1)






#plus data

if ReEnterData:

    #FileNums = [159]
    #FileNums = list(range(155, 158+1)) + list(range(160, 164+1))
    FileNums = list(range(155, 164+1))
    #FileNums = list(range(122,130+1))
    #FileNums = list(range(155, 155+1))
    XOnp, LOnp, StageDelayp, Diode2p, Ipm2Sump, TimeToolp, TTAmpp, TTFWHMp, ScanNump, RowlandYp, RowOffsetp, L3Ep, CspadSump = loadData(FileNums, "XES", 1)

RowlandWOffsetp = [x-y for x,y in zip(RowlandYp, RowOffsetp)]

#RowlandWOffsetp = RowOffsetp

#FilterpOn, FilterpOff, DiodeOffsetp = makeFilter(Diode2p, Ipm2Sump, RowlandWOffsetp, XOnp, LOnp, DiodeIpmSlopep, TimeToolp, TTAmpp, TTFWHMp, False, ScanNump, 2)
Filterp, DiodeOffsetp = makeOneFilter(Diode2p, Ipm2Sump, RowlandWOffsetp, XOnp, LOnp, TimeToolp, TTAmpp, TTFWHMp, L3Ep, CspadSump, False, 2)

#FilterpOn = [x and y for x,y in zip(XOnp, LOnp)]
#FilterpOff = [x and not y for x,y in zip(XOnp, LOnp)]

DiodeWOffsetp = [x-DiodeOffsetp for x in Diode2p]

#DiodeWOffsetp = Diode2p

TTDelayp = [(x*1e-12 + y)*1e15 for x,y in zip(TimeToolp,StageDelayp)]

XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTSteps, CspadSump, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelayp, TTSteps, FPlots)
#XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTSteps, DiodeWOffsetp, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelayp, TTSteps, FPlots)

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii+1])/2]
    
XESDiffplus = [(x-XESOff_Normp)*1000/XESOff_Normp for x in XESOn_Normp]

Energyplus = str(round(convertAngle2Energy(ScanNump[0])*1000,1))







#minus data

if ReEnterData:

    FileNums = list(range(180,188+1))
    #FileNums = list(range(180,180+1))
    #FileNums = list(range(165, 178+1))
    
    #FileNums = list(range(155, 158+1)) + list(range(160, 164+1))
    XOnm, LOnm, StageDelaym, Diode2m, Ipm2Summ, TimeToolm, TTAmpm, TTFWHMm, ScanNumm, RowlandYm, RowOffsetm, L3Em, CspadSumm = loadData(FileNums, False, 1)

RowlandWOffsetm = [x-y for x,y in zip(RowlandYm, RowOffsetm)]

#FiltermOn, FiltermOff, DiodeOffsetm = makeFilter(Diode2m, Ipm2Summ, RowlandWOffsetm, XOnm, LOnm, DiodeIpmSlopem, TimeToolm, TTAmpm, TTFWHMm, False, ScanNumm, 2)
Filterm, DiodeOffsetm = makeOneFilter(Diode2m, Ipm2Summ, RowlandWOffsetm, XOnm, LOnm, TimeToolm, TTAmpm, TTFWHMm, L3Em, CspadSumm, False, 2)

#FilterpOn = [x and y for x,y in zip(XOnp, LOnp)]
#FilterpOff = [x and not y for x,y in zip(XOnp, LOnp)]

DiodeWOffsetm = [x-DiodeOffsetm for x in Diode2m]

#DiodeWOffsetm = Diode2m

TTDelaym = [(x*1e-12 + y)*1e15 for x,y in zip(TimeToolm,StageDelaym)]

XESOn_Normm, XESOff_Normm, Num_Onm, Num_Offm, NormFactor_Offm, NormFactor_Onm = makeXES(NumTTSteps, DiodeWOffsetm, RowlandWOffsetm, Filterm, LOnm, XOnm, TTDelaym, TTSteps, FPlots)

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii+1])/2]
    
XESDiffminus = [(x-XESOff_Normm)*1000/XESOff_Normm for x in XESOn_Normm]

Energyminus = str(round(convertAngle2Energy(ScanNumm[0])*1000,1))






Fit1, Fit2, params, info = fitXES(TCenters, XESDiffplus, XESDiffminus, -1534, FPlots)

t0 = params[6]

folder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
with open(folder + "t0.pkl", "wb") as f:
        pickle.dump(t0, f)


TTDelaypp = [x-t0 for x in TTDelayp]
TTDelaymp = [x-t0 for x in TTDelaym]



TTSteps = np.linspace(-250, 1400, NumTTStepsPlots+1)

XESOn_Normp, XESOff_Normp, Num_Onp, Num_Offp, NormFactor_Offp, NormFactor_Onp = makeXES(NumTTStepsPlots, DiodeWOffsetp, RowlandWOffsetp, Filterp, LOnp, XOnp, TTDelaypp, TTSteps, FPlots)
XESDiffplus = [(x-XESOff_Normp)*1000/XESOff_Normp for x in XESOn_Normp]

XESOn_Normm, XESOff_Normm, Num_Onm, Num_Offm, NormFactor_Offm, NormFactor_Onm = makeXES(NumTTStepsPlots, DiodeWOffsetm, RowlandWOffsetm, Filterm, LOnm, XOnm, TTDelaymp, TTSteps, FPlots)
XESDiffminus = [(x-XESOff_Normm)*1000/XESOff_Normm for x in XESOn_Normm]









TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii])/2]


Fitp, Fitm, params, info = fitXES(TCenters, XESDiffplus, XESDiffminus, 0, FPlots)

tt = np.linspace(-250,1400,1000)

pluscolor = '#0070DF'
minuscolor = '#54A60C'
darkpluscolor = '#004B95'
darkminuscolor = '#376E08'

plt.figure()
line0 = plt.plot(TCenters, XESDiffplus, 'o', color = pluscolor)
line1 = plt.plot(TCenters, XESDiffminus, 's', color = minuscolor)
line2 = plt.plot(tt, convolved(tt, params[0], params[1], params[2], params[6], params[7]), color = darkpluscolor)
line3 = plt.plot(tt, convolved(tt, params[3], params[4], params[5], params[6], params[7]), '--', color = darkminuscolor)
plt.ylabel('$\Delta$ T x 10$^3$')
plt.xlabel('time delay (fs)')
plt.legend((line0[0], line1[0], line2[0], line3[0]), (Energyplus +' eV', Energyminus +' eV', Energyplus +' eV fit', Energyminus +' eV fit'))

plt.figure()
line0 = plt.plot(TCenters, savgol_filter(XESDiffplus,5,2), 'o', color = pluscolor)
line1 = plt.plot(TCenters, savgol_filter(XESDiffminus,5,2), 's', color = minuscolor)
line2 = plt.plot(tt, convolved(tt, params[0], params[1], params[2], params[6], params[7]), color = darkpluscolor)
line3 = plt.plot(tt, convolved(tt, params[3], params[4], params[5], params[6], params[7]), '--', color = darkminuscolor)
plt.title('smoothed')
plt.ylabel('$\Delta$ T x 10$^3$')
plt.xlabel('time delay (fs)')
plt.legend((line0[0], line1[0], line2[0], line3[0]), (Energyplus +' eV', Energyminus +' eV', Energyplus +' eV fit', Energyminus +' eV fit'))


Residualp = [x-y for x,y,z in zip(savgol_filter(XESDiffplus,5,2),Fitp,TCenters) if z>200]
Residualm = [x-y for x,y,z in zip(savgol_filter(XESDiffminus,5,2),Fitm,TCenters) if z>200]

TCP = [x for x in TCenters if x>200]

plt.figure()
line0 = plt.plot(TCP, Residualp, marker = 'o', color = pluscolor)
line1 = plt.plot(TCP, Residualm, marker = 's', color = minuscolor)
plt.ylabel('residuals')
plt.xlabel('time delay (fs)')
plt.legend((line0[0], line1[0]), (Energyplus +' eV', Energyminus +' eV'))
plt.title('smoothed')

FTp = np.fft.rfft(Residualp)
FTm = np.fft.rfft(Residualm)

Freq = np.fft.rfftfreq(len(Residualp), d=(TCenters[0]-TCenters[1])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
line0 = plt.plot(Freq, abs(FTp), color = pluscolor)
line1 = plt.plot(Freq, abs(FTm), color = minuscolor)
plt.ylabel('fourier amplitude')
plt.xlabel('cm$^{-1}$')
plt.legend((line0[0], line1[0]), (Energyplus +' eV', Energyminus +' eV'))
plt.title('smoothed')






TCP = [x for x in TCenters if x>-2000]

Residualp = [x-y for x,y,z in zip(XESDiffplus,Fitp,TCenters) if z>-2000]
Residualm = [x-y for x,y,z in zip(XESDiffminus,Fitm,TCenters) if z>-2000]

HammingWindowp = np.hamming(len(Residualp))
HammingWindowm = np.hamming(len(Residualm))

plt.figure()
line0 = plt.plot(TCP, Residualp, marker = 'o', color = pluscolor)
line1 = plt.plot(TCP, Residualm, marker = 's', color = minuscolor)
plt.ylabel('residuals')
plt.xlabel('time delay (fs)')
plt.legend((line0[0], line1[0]), (Energyplus +' eV', Energyminus +' eV'))

FTp = np.fft.rfft([x*y for x,y in zip(Residualp, HammingWindowp)])
FTm = np.fft.rfft([x*y for x,y in zip(Residualm, HammingWindowm)])

Freq = np.fft.rfftfreq(len(Residualp), d=(TCenters[0]-TCenters[1])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
line0 = plt.plot(Freq, abs(FTp), color = pluscolor)
line1 = plt.plot(Freq, abs(FTm), color = minuscolor)
plt.ylabel('fourier amplitude')
plt.xlabel('cm$^{-1}$')
plt.legend((line0[0], line1[0]), (Energyplus +' eV', Energyminus +' eV'))
plt.title('with Hamming window')
