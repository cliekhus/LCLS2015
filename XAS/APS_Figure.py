# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 13:24:18 2020

@author: chelsea
"""

        
import h5py
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib.cbook import get_sample_data
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage, AnnotationBbox)


pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'
red = '#c70039'
darkred = '#8c0028'
darkerred = '#64001c'

Eoff = 143.6
shift = 1.12
file = 'simulation/feru-series-2-10'

calc = np.loadtxt(file+'.dat')
roots = np.loadtxt(file+'.roots')

APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')

FeIII = np.array(APSName['/FeIII_ref_RIXS'])
FeII = np.array(APSName['/FeII_ref_RIXS'])
FeRu = np.array(APSName['/FeRu_RIXS'])

incident_axis = 1000*np.array(APSName['/Fe_RIXS_incident_axis'])
emitted_axis = 1000*np.array(APSName['/Fe_RIXS_emitted_axis'])
xp,yp = np.meshgrid(incident_axis,emitted_axis)

incident_axis = incident_axis[:,0]


kalpha_index = np.argmax(np.sum(FeIII, axis=0))
plt.figure()
ax=plt.subplot(2,2,1)
plt.pcolor(xp, yp, np.log(np.transpose(FeIII)))
plt.arrow(7110, emitted_axis[:,kalpha_index][0], 14, 0, head_width = 3, head_length=1, color = 'w')
plt.text(7107.5, 6403, r'k$\alpha_1$', color = 'w')
plt.text(7107.5, 6390, r'k$\alpha_2$', color = 'w')
plt.xlim([7107,7125])
plt.ylim([6380,6415])
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('emitted energy (eV)')

ax=plt.subplot(2,2,3)
FeIII_XANES = np.sum(FeIII, axis = 1)
plt.plot(incident_axis, (FeIII_XANES-min(FeIII_XANES))/np.sum(FeIII_XANES)*100)
plt.xlim([7107,7125])
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('XANES')

ax=plt.subplot(2,2,2)
HERFD_III = FeIII[:,kalpha_index]/np.sum(FeIII)*100
plt.plot(incident_axis, HERFD_III)
plt.xlim([7107,7125])
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('HERFD-XANES')

FeIII_XANES = np.sum(FeIII, axis = 1)/np.sum(np.sum(FeIII))
FeII_XANES = np.sum(FeII, axis = 1)/np.sum(np.sum(FeII))
FeRu_XANES = np.sum(FeRu, axis = 1)/np.sum(np.sum(FeRu))
# =============================================================================
# 
# ax=plt.subplot(2,2,4)
# with get_sample_data("C:/Users/chelsea/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/Figures/FeMOs.pdf") as file:
#     arr_img = plt.imread(file, format='pdf')
# 
# imagebox = OffsetImage(arr_img, zoom=.25)
# imagebox.image.axes = ax
# 
# ab = AnnotationBbox(imagebox, [0.5,0.5],
#                     xybox=(0, 0),
#                     xycoords='data',
#                     boxcoords="offset points",
#                     pad=0.5,
#                     arrowprops=dict(
#                         arrowstyle="->",
#                         connectionstyle="angle,angleA=0,angleB=90,rad=3")
#                     )
# 
# ax.add_artist(ab)
# =============================================================================

plt.tight_layout()


plt.figure()
plt.plot(emitted_axis[0], np.sum(FeIII, axis=0), marker='.')

plt.xlabel('emitted energy (eV)')
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
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('XANES (arb. units)')
plt.legend()

ax=plt.subplot(2,1,2)
plt.plot(calc[:,0]+Eoff+shift, calc[:,1]*scale, color = red, label = 'calculated', linewidth = 2)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]*scale/30, markerfmt = 'none', basefmt='none', linefmt=red)
plt.xlim([round(7107),round(7125)])
plt.ylim([0,1])
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('XANES (arb. units)')
plt.legend()

plt.tight_layout()

scale = HERFD_FeRu[50-np.argmax(HERFD_FeRu[range(50,100)])]/calc[np.argmax(calc[range(1000),1]),1]

fig, ax = plt.subplots(figsize = (3.3,4))
plt.plot(incident_axis[incident_axis < 7124] - energy_shift, HERFD_II[incident_axis < 7124], marker = '', label = r'Fe$^{\mathrm{II}}$(CN)$_6$', color = pluscolor, linestyle = '--', linewidth = 2)
plt.plot(incident_axis - energy_shift, HERFD_III, marker = '', label = r'Fe$^{\mathrm{III}}$(CN)$_6$, v1', color = minuscolor, linewidth = 2, linestyle = ':')
plt.plot(incident_axis - energy_shift, HERFD_III_p, marker = '', label = r'Fe$^{\mathrm{III}}$(CN)$_6$, v2', color = minuscolor, linewidth = 2)
plt.plot(incident_axis - energy_shift, HERFD_FeRu, marker = '', label = r'FeRu', color = pluscolor2, linewidth = 2, linestyle = '-.')
plt.plot(calc[:,0]+Eoff+shift, calc[:,1]*scale, color = red, label = 'calculated', zorder = -100)
plt.stem(roots[:,0]+Eoff+shift, roots[:,1]*scale/30, markerfmt = 'none', basefmt='none', linefmt=red)
plt.xlim([7107,7125])
plt.xlabel('incident x-ray energy (eV)')
plt.ylabel('HERFD-XANES (arb. units)')
plt.legend()
plt.tight_layout()




plt.figure()
plt.plot(energies, np.delete(xasProData_one.XASOff_Norm,-4), label = 'LCLS ground state', linestyle = '--')
plt.plot(incident_axis - energy_shift, xasoff(incident_axis, *params_XAS), label='LCLS ground state fit')
plt.plot(incident_axis - energy_shift, HERFD_FeRu*scale_factor, marker = '', label = 'APS ground state', linestyle = '--')
plt.plot(incident_axis - energy_shift, xasoff(incident_axis, *params_II)*scale_factor, label='APS ground state fit')
plt.plot(XX+shift, Ampforplotting1*320, label = 'calculated ground state', linestyle = '-.')
plt.plot(incident_axis - energy_shift, xason(incident_axis, params_FeRu[0], params_FeRu[1], params_FeRu[2], params_FeRu[3], params_FeRu[4], params_FeRu[5], 
                                params_FeRu[6], params_FeRu[7], params_FeRu[8], 0,0,0,0)/.25, label = 'extracted excited state')
plt.plot(XX+shift, Ampforplotting*320, label='calculated excited state', linestyle = '-.')
plt.xlim([7110,7122])
plt.xlabel('incident energy (eV)')
plt.ylabel('HERFD-XANES (arb. units)')
plt.legend()
plt.tight_layout()


plt.figure(figsize = (3,5))
plt.subplot(211)
plt.plot(incident_axis, FeII_XANES, label = r'Fe$^{\mathrm{II}}$(CN)$_6$', color = pluscolor, linestyle = '--', linewidth = 2)
plt.plot(incident_axis, FeIII_XANES, label = r'Fe$^{\mathrm{III}}$(CN)$_6$', color = pluscolor2, linestyle = ':', linewidth = 2)
plt.plot(incident_axis, FeRu_XANES, label = r'FeRu', color = minuscolor, linewidth = 2)
#plt.xlabel('incident energy (eV)')
plt.ylabel('XANES (arb. units)')
#plt.xticks(np.arange(7110, 7123, 4.0))
plt.xlim([7110,7122])
plt.ylim([0, 0.025])
plt.legend(loc = 'upper left')

plt.subplot(212)
plt.plot(incident_axis, HERFD_II, label = r'Fe$^{\mathrm{II}}$(CN)$_6$', color = pluscolor, linestyle = '--', linewidth = 2)
plt.plot(incident_axis, HERFD_III, label = r'Fe$^{\mathrm{III}}$(CN)$_6$', color = pluscolor2, linestyle = ':', linewidth = 2)
plt.plot(incident_axis, HERFD_FeRu, label = r'FeRu', color = minuscolor, linewidth = 2)
plt.xlabel('incident energy (eV)')
plt.ylabel('HERFD-XANES (arb. units)')
#plt.xticks(np.arange(7110, 7123, 4.0))
plt.xlim([7110,7122])
plt.ylim([0, 0.05])
#plt.legend(loc = 'upper left')
plt.tight_layout()

#plt.rcParams.update({'font.size': 14})
#fig, ax = plt.subplots(figsize = (6.5,4))
#plt.subplot(1,2,1)
#plt.plot(incident_axis[incident_axis < 7124], HERFD_II[incident_axis < 7124], marker = '', color = pluscolor, linestyle = '-', linewidth = 2)
#plt.xlim([7107,7124])
#plt.xticks(np.arange(7107, 7124, 5))
#plt.ylabel('HERFD-XANES (arb. units)')
#plt.title(r'$[$Fe$^{\mathrm{II}}$(CN)$_6]^{4-}$')
#plt.subplot(1,2,2)
#plt.plot(incident_axis, HERFD_III, marker = '', color = minuscolor, linewidth = 2, linestyle = '-')
#plt.title(r'$[$Fe$^{\mathrm{III}}$(CN)$_6]^{3-}$')
#plt.xlim([7107, 7124])
#plt.xticks(np.arange(7107, 7124, 5))
#fig.add_subplot(111, frameon=False)
## hide tick and tick label of the big axis
#plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
#plt.xlabel('incident x-ray energy (eV)')
#plt.tight_layout()



with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_HERFD_II.pkl", "wb") as f:
    pickle.dump(HERFD_II, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_HERFD_III.pkl", "wb") as f:
    pickle.dump(HERFD_III, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_FeRu.pkl", "wb") as f:
    pickle.dump(HERFD_FeRu, f)
with open("D:\LCLS_Data\LCLS_python_data\XAS_Spectra\APS_incident.pkl", "wb") as f:
    pickle.dump(incident_axis, f)
        
    
    
