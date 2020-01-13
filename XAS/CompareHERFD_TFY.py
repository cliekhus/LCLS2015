# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:15:21 2020

@author: chelsea
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\EnergyShift.pkl", "rb") as f:
    Shift = pickle.load(f)

with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\TFY.pkl", "rb") as f:
    TFY = pickle.load(f)
    
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\TFY_E.pkl", "rb") as f:
    TFY_E = pickle.load(f)
    
TFY_E = TFY_E+Shift
    
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\HERFD.pkl", "rb") as f:
    HERFD = pickle.load(f)
    
HERFD = np.delete(HERFD,-4)
    
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\HERFD_E.pkl", "rb") as f:
    HERFD_E = pickle.load(f)

HERFD_E = np.delete(HERFD_E,-4)
    
HERFD_E = HERFD_E+Shift




TFY_tck = interpolate.splrep(TFY_E, TFY, s=0)
HERFD_tck = interpolate.splrep(HERFD_E, HERFD, s=0)
Energy = np.linspace(min(TFY_E), max(TFY_E), 1000)
TFY_sp = interpolate.splev(Energy, TFY_tck, der=0)
HERFD_sp = interpolate.splev(Energy, HERFD_tck, der=0)



TFY_tck_base = interpolate.splrep(TFY_E[np.logical_or(TFY_E<7112+Shift, TFY_E>7118+Shift)], TFY[np.logical_or(TFY_E<7112+Shift, TFY_E>7118+Shift)], s=0)
HERFD_tck_base = interpolate.splrep(HERFD_E[np.logical_or(HERFD_E<7112+Shift, HERFD_E>7118+Shift)], HERFD[np.logical_or(HERFD_E<7112+Shift, HERFD_E>7118+Shift)], s=0)
TFY_sp_base = interpolate.splev(Energy, TFY_tck_base, der=0)
HERFD_sp_base = interpolate.splev(Energy, HERFD_tck_base, der=0)


Cindex = np.argmax(HERFD_sp[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)]-HERFD_sp_base[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)])
Cregion = Energy[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)]
HC = Cregion[Cindex]

Cindex = np.argmax(TFY_sp[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)]-TFY_sp_base[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)])
Cregion = Energy[np.logical_and(Energy<7118+Shift, Energy > 7115+Shift)]
TC = Cregion[Cindex]


Bindex = np.argmax(HERFD_sp[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)]-HERFD_sp_base[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)])
Bregion = Energy[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)]
HB = Bregion[Bindex]

Bindex = np.argmax(TFY_sp[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)]-TFY_sp_base[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)])
Bregion = Energy[np.logical_and(Energy<7114+Shift, Energy > 7112.5+Shift)]
TB = Bregion[Bindex]


Mindex = np.argmin(HERFD_sp[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)]-HERFD_sp_base[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)])
Mregion = Energy[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)]
HM = Mregion[Mindex]

Mindex = np.argmin(TFY_sp[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)]-TFY_sp_base[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)])
Mregion = Energy[np.logical_and(Energy<7115+Shift, Energy > 7114+Shift)]
TM = Mregion[Mindex]


plt.figure()
plt.plot(TFY_E, TFY, label = 'TFY')
plt.plot(Energy, TFY_sp-TFY_sp_base, label = 'TFY_sp')
plt.plot(HERFD_E, HERFD, label = 'HERFD')
plt.plot(Energy, HERFD_sp-HERFD_sp_base, label = 'HERFD_sp')
plt.plot(Energy, TFY_sp_base)
plt.plot(Energy, HERFD_sp_base)
plt.plot([HC, HC], [0,4])
plt.plot([TC, TC], [0,4])
plt.plot([HB, HB], [0,4])
plt.plot([TB, TB], [0,4])
plt.plot([HM, HM], [0,4])
plt.plot([TM, TM], [0,4])
plt.xlabel('Incident energy (eV)')
plt.ylabel('absorption arb. units.')
plt.legend()



TFY_tck_base = interpolate.splrep(TFY_E[np.logical_or.reduce((TFY_E<7112.3+Shift, TFY_E>7118+Shift, TFY_E==7114.3+Shift))], TFY[np.logical_or.reduce((TFY_E<7112.3+Shift, TFY_E>7118+Shift, TFY_E==7114.3+Shift))], s=0)
HERFD_tck_base = interpolate.splrep(HERFD_E[np.logical_or.reduce((HERFD_E<7112.3+Shift, HERFD_E>7118+Shift, HERFD_E==7114.3+Shift))], HERFD[np.logical_or.reduce((HERFD_E<7112.3+Shift, HERFD_E>7118+Shift, HERFD_E==7114.3+Shift))], s=0)
#TFY_tck_base = interpolate.splrep(TFY_E[np.logical_or(TFY_E<7112.3, TFY_E>7118)], TFY[np.logical_or(TFY_E<7112.3, TFY_E>7118)], s=0)
#HERFD_tck_base = interpolate.splrep(HERFD_E[np.logical_or(HERFD_E<7112.3, HERFD_E>7118)], HERFD[np.logical_or(HERFD_E<7112.3, HERFD_E>7118)], s=0)
TFY_sp_base = interpolate.splev(TFY_E, TFY_tck_base, der=0)
HERFD_sp_base = interpolate.splev(HERFD_E, HERFD_tck_base, der=0)


fig, axs = plt.subplots(2, 1)
axs[0].plot(TFY_E, TFY, label = 'TFY', linestyle='-')
axs[0].plot(HERFD_E, HERFD, label = 'HERFD', linestyle = '-.')
axs[0].plot(TFY_E, TFY_sp_base, label = 'TFY background fit', linestyle = ':')
axs[0].plot(HERFD_E, HERFD_sp_base, label = 'HERFD background fit', linestyle = '--')
axs[1].plot(TFY_E, (TFY-TFY_sp_base)/sum(TFY-TFY_sp_base), label = 'TFY', linestyle = '-')
axs[1].plot(HERFD_E, (HERFD-HERFD_sp_base)/sum(HERFD-HERFD_sp_base), label = 'HERFD', linestyle = '--')
axs[1].set_xlabel('incident energy (eV)')
axs[0].set_ylabel('absorption')
axs[1].set_ylabel('background subtracted')
axs[0].legend()
axs[1].legend()
fig.tight_layout()

