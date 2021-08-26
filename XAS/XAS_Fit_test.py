# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 19:08:52 2020

@author: chelsea
"""

import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from fittingfunctions import xasoff, xason, diffxas
import numpy as np

#plt.close('all')

folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"

with open(folder + "APS_HERFD_II.pkl", "rb") as f:
    HERFD_II = pickle.load(f)

with open(folder + "APS_HERFD_III.pkl", "rb") as f:
    HERFD_III = pickle.load(f)

with open(folder + "APS_FeRu.pkl", "rb") as f:
    HERFD_FeRu = pickle.load(f)

with open(folder + "APS_incident.pkl", "rb") as f:
    incident_axis = pickle.load(f)


    


sigAS = 0.3
AS = 0.01
x0AS = 7110.3
x0AdS = 7113.4

sigBS = 0.1
sigBpS = 0.1
BS = 0.01
BpS = 0.01
x0BS = 7114.3
x0BpS = 7114.5
x0BdS = 7116

sigCS = 2
sigCpS = 0.558
CS = 0.02
CpS = 0.02
x0CS = 7116.7
x0CpS = 7118.5
x0CdS = 7120

erfslopeS = 5
erfslopepS = 5
offsetS = 0.05
offsetpS = 0.05
erfampS = .05
erfamppS = .05
peakS = 7121
peakpS = 7122
peakdS = 7119



plt.figure()
plt.plot(incident_axis, HERFD_FeRu)
#plt.plot(incident_axis, xasoff(incident_axis, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
params_II, cov_II = curve_fit(xasoff, incident_axis, HERFD_FeRu, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
plt.plot(incident_axis, xasoff(incident_axis, *params_II))

plt.figure()
plt.plot(incident_axis, HERFD_II)
params_FeII, cov_FeII = curve_fit(xasoff, incident_axis, HERFD_II, p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetpS,erfamppS,erfslopepS,peakpS])
plt.plot(incident_axis, xasoff(incident_axis, *params_FeII))


plt.figure()
plt.plot(incident_axis, HERFD_III)
#plt.plot(incident_axis, xason(incident_axis, sigAS,AS,x0AS, sigBpS,BpS,x0BpS, sigCpS,CpS,x0CpS, offsetpS,erfamppS,erfslopepS,peakpS))
params_III, cov_III = curve_fit(xason, incident_axis, HERFD_III, p0 = [sigAS,AS,x0AS, sigBpS,BpS,x0BpS, sigCpS,CpS,x0CpS, offsetpS,erfamppS,erfslopepS,peakpS])
plt.plot(incident_axis, xason(incident_axis, *params_III))


plt.figure()
plt.plot(xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm/79006)
#plt.plot(xasProData_one.EnergyPlot, xasoff(xasProData_one.EnergyPlot, sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS))
params_XAS, cov_XAS = curve_fit(xasoff, xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm/79006, \
                                p0 = [sigBS,BS,x0BS, sigCS,CS,x0CS, offsetS,erfampS,erfslopeS,peakS])
plt.plot(incident_axis, xasoff(incident_axis, *params_XAS))



energy_shift = params_XAS[2]-params_II[2]
#params_XAS[2] = params_XAS[2]-energy_shift
#params_XAS[5] = params_XAS[5]-energy_shift
#params_XAS[9] = params_XAS[9]-energy_shift

energy = np.delete(xasProData_one.EnergyPlot,-4) - energy_shift
diff = np.delete(XASDiffBootF,-4)

plt.figure()
plt.plot(energy, diff/15801, label = 'data')
#plt.plot(energy, diffxas(energy, x0AdS, x0BdS, x0CdS, peakdS))

params_FeRu, cov_FeRu = curve_fit(diffxas, energy, diff/15801, p0 = [x0AdS, x0BdS, x0CdS, 1, 0, 0])


Fe_Fits = {"params_II": params_II, "params_III": params_III, "params_XAS": params_XAS, "params_FeRu": params_FeRu, "cov_FeRu": np.sqrt(np.diag(cov_FeRu)), 'energy_shift': energy_shift}

with open(folder + "Fe_fits.pkl", "wb") as f:
    pickle.dump(Fe_Fits, f)


plt.plot(incident_axis, diffxas(incident_axis, *params_FeRu), label = 'fit')
plt.plot(incident_axis, (xason(incident_axis, params_III[0],params_III[1],params_FeRu[0], params_III[3],params_III[4],params_FeRu[1], \
            params_III[6],params_III[7],params_FeRu[2], 0,0,0,0))*params_FeRu[3], label = 'excited state')
plt.xlabel('incident energy (eV)')
plt.ylabel('difference HERFD')
plt.legend()
plt.tight_layout()


print('aprox exfrac')
exfrac = (params_III[7]*params_FeRu[3]/params_II[4])*.2
print(exfrac)