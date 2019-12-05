# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 20:09:03 2019

@author: chelsea
"""

Fit, params, cov = fitOneXES(TimesC, XASDiffPlotC/xasPeaksDataC.XASOff_Norm, 0, -.1, 60, 30, True)

plt.figure()
plt.plot(TimesC, XASDiffPlotC/xasPeaksDataC.XASOff_Norm-Fit)

Residual = XASDiffPlotC/xasPeaksDataC.XASOff_Norm-Fit

bartlettWindow = np.bartlett(len(Residual))
FT = np.fft.rfft([x*y for x,y in zip(Residual, bartlettWindow)])

Freq = np.fft.rfftfreq(len(Residual), d=(TimesC[0]-TimesC[1])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure(figsize = (4,5))
plt.plot(Freq, np.abs(FT))