# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:24:58 2019

@author: chelsea
"""



import h5py
import numpy as np
import matplotlib.pyplot as plt


APSName = h5py.File('Data/APS/APS_Aug_2015_Fesamples.mat')

FeRuRIXS = np.array(APSName['/FeRu_RIXS'])

incident_axis = np.array(APSName['/Fe_RIXS_incident_axis'])
emitted_axis = np.array(APSName['/Fe_RIXS_emitted_axis'])
xp,yp = np.meshgrid(emitted_axis,incident_axis)

plt.figure(), plt.plot(emitted_axis[0], np.sum(FeRuRIXS, axis=0), marker='.')
plt.figure(), plt.plot(incident_axis, np.sum(FeRuRIXS, axis=1), marker='.')
plt.figure(), plt.pcolor(xp, yp, FeRuRIXS)