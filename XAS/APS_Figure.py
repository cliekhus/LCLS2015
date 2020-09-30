# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 13:24:18 2020

@author: chelsea
"""

        
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pickle


pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'
darkred = '#8c0028'
darkerred = '#64001c'

Eoff = 143.6
shift = 1.14
file = 'C:/Users/chelsea/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/simulation/feru-series-2-10'

calc = np.loadtxt(file+'.dat')
roots = np.loadtxt(file+'.roots')

APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

FeIII = np.array(APSName['/FeIII_ref_RIXS'])
FeII = np.array(APSName['/FeII_ref_RIXS'])
FeRu = np.array(APSName['/FeRu_RIXS'])

incident_axis = 1000*np.array(APSName['/Fe_RIXS_incident_axis'])
emitted_axis = 1000*np.array(APSName['/Fe_RIXS_emitted_axis'])
xp,yp = np.meshgrid(emitted_axis,incident_axis)

incident_axis = incident_axis[:,0]

plt.figure()
plt.pcolor(xp, yp, FeIII)

plt.figure()
plt.plot(emitted_axis[0], np.sum(FeIII, axis=0), marker='.')

plt.xlabel('emitted energy (keV)')
plt.ylabel('emittance')

APSXASNorm = np.sum(FeRu, axis = 1)
APSXASNorm = (APSXASNorm-min(APSXASNorm))/np.sum(APSXASNorm)*100


kalpha_index = np.argmax(np.sum(FeII, axis=0))
HERFD_II = FeII[:,kalpha_index]/np.sum(FeII)*100
HERFD_III = FeIII[:,kalpha_index]/np.sum(FeIII)*100
kalpha_index = np.argmax(np.sum(FeIII, axis=0))
HERFD_III_p = FeIII[:,kalpha_index]/np.sum(FeIII)*100
kalpha_index = np.argmax(np.sum(FeRu, axis=0))
HERFD_FeRu = FeRu[:,kalpha_index]/np.sum(FeRu)*100

scale = APSXASNorm[50-np.argmax(APSXASNorm[range(50,100)])]/calc[np.argmax(calc[range(1000),1]),1]


plt.figure(figsize=(3.3,4))

ax=plt.subplot(2,1,1)
plt.plot(incident_axis, APSXASNorm, marker='', label='experiment', color = minuscolor, linewidth = 2, linestyle = '--')
plt.xlim([7107,7125])
plt.ylim([0,1])
plt.xlabel('incident x-ray energy (keV)')
plt.ylabel('XANES (arb. units)')
plt.legend()

ax=plt.subplot(2,1,2)
plt.plot(calc[:,0]+Eoff+shift, calc[:,1]*scale, color = red, label = 'calculated', linewidth = 2)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]*scale/30, markerfmt = 'none', basefmt='none', linefmt=red)
plt.xlim([round(7107),round(7125)])
plt.ylim([0,1])
plt.xlabel('incident x-ray energy (keV)')
plt.ylabel('XANES (arb. units)')
plt.legend()

plt.tight_layout()

scale = HERFD_FeRu[50-np.argmax(HERFD_FeRu[range(50,100)])]/calc[np.argmax(calc[range(1000),1]),1]

fig, ax = plt.subplots(figsize = (3.3,4))
plt.plot(incident_axis[incident_axis < 7124], HERFD_II[incident_axis < 7124], marker = '', label = r'Fe$^{\mathrm{II}}$(CN)$_6$', color = pluscolor, linestyle = '--', linewidth = 2)
plt.plot(incident_axis, HERFD_III, marker = '', label = r'Fe$^{\mathrm{III}}$(CN)$_6$, v1', color = minuscolor, linewidth = 2, linestyle = ':')
plt.plot(incident_axis, HERFD_III_p, marker = '', label = r'Fe$^{\mathrm{III}}$(CN)$_6$, v2', color = minuscolor, linewidth = 2)
plt.plot(incident_axis, HERFD_FeRu, marker = '', label = r'FeRu', color = pluscolor2, linewidth = 2, linestyle = '-.')
plt.plot(calc[:,0]+Eoff+shift, calc[:,1]*scale, color = red, label = 'calculated', zorder = -100)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]*scale/30, markerfmt = 'none', basefmt='none', linefmt=red)
plt.xlim([7107,7125])
plt.xlabel('incident x-ray energy (keV)')
plt.ylabel('HERFD-XANES (arb. units)')
plt.legend()
plt.tight_layout()



with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_HERFD_II.pkl", "wb") as f:
    pickle.dump(HERFD_II, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_HERFD_III.pkl", "wb") as f:
    pickle.dump(HERFD_III, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_FeRu.pkl", "wb") as f:
    pickle.dump(HERFD_FeRu, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_incident.pkl", "wb") as f:
    pickle.dump(incident_axis, f)
        
    
    
