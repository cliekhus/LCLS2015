# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:55:07 2020

@author: chels
"""


import pickle
from APSXESCalibration import convertAngle2Energy
import matplotlib.pyplot as plt
import matplotlib.patches as pat


folder = "C://Users/chels/Downloads/numbered_data/"

with open(folder + "peaksProData123.pkl", "rb") as f:
    peaksProData123 = pickle.load(f)
    
Energy123 = round(convertAngle2Energy(123, True)*1000,1)

with open(folder + "peaksProData131.pkl", "rb") as f:
    peaksProData131 = pickle.load(f)

Energy131 = round(convertAngle2Energy(131, True)*1000,1)

with open(folder + "peaksProData144.pkl", "rb") as f:
    peaksProData144 = pickle.load(f)

Energy144 = round(convertAngle2Energy(144, True)*1000,1)

with open(folder + "peaksProData155.pkl", "rb") as f:
    peaksProData155 = pickle.load(f)

Energy155 = round(convertAngle2Energy(155, True)*1000,1)

with open(folder + "peaksProData165.pkl", "rb") as f:
    peaksProData165 = pickle.load(f)
    
Energy165 = round(convertAngle2Energy(165, True)*1000,1)
    
with open(folder + "peaksProData180.pkl", "rb") as f:
    peaksProData180 = pickle.load(f)
    
Energy180 = round(convertAngle2Energy(180, True)*1000,1)

with open("C://Users/chels/Downloads/LCLS_python_data/LCLS_python_data/XES_TimeResolved/TCentersPF.pkl", "rb") as f:
    TCenters = pickle.load(f)



fig = plt.figure(figsize = (5,7))
ax = plt.subplot(8,1,1)
Y155 = (peaksProData155.XESOn_Norm - peaksProData155.XESOff_Norm)/peaksProData155.XESOff_Norm*100
plt.plot(TCenters, Y155, color = 'r', label = str(Energy155) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=1)
plt.ylim([-.4,2.2])
ax.set_xticklabels([])

ax = plt.subplot(8,1,2)
Y123 = (peaksProData123.XESOn_Norm - peaksProData123.XESOff_Norm)/peaksProData123.XESOff_Norm*100
plt.plot(TCenters, Y123, color = 'darkorange', label = str(Energy123) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=1)
plt.ylim([-.4,2.2])
ax.set_xticklabels([])

ax = plt.subplot(8,1,3)
Y144 = (peaksProData144.XESOn_Norm - peaksProData144.XESOff_Norm)/peaksProData144.XESOff_Norm*100
plt.plot(TCenters, Y144, color = 'k', label = str(Energy144) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=1)
plt.ylim([-.4,2.2])
ax.set_xticklabels([])

ax = plt.subplot(8,1,4)
Y165 = (peaksProData165.XESOn_Norm - peaksProData165.XESOff_Norm)/peaksProData165.XESOff_Norm*100
plt.plot(TCenters, Y165, color = 'g', label = str(Energy165) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-2.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=4)
plt.ylim([-2.2,.4])
ax.set_xticklabels([])

ax = plt.subplot(8,1,5)
Y131 = (peaksProData131.XESOn_Norm - peaksProData131.XESOff_Norm)/peaksProData131.XESOff_Norm*100
plt.plot(TCenters, Y131, color = 'b', label = str(Energy131) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-2.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=4)
plt.ylim([-2.2,.4])
ax.set_xticklabels([])

ax = plt.subplot(8,1,6)
Y180 = (peaksProData180.XESOn_Norm - peaksProData180.XESOff_Norm)/peaksProData180.XESOff_Norm*100
plt.plot(TCenters, Y180, color = 'purple', label = str(Energy180) + " eV")
patch = pat.Rectangle(xy=(TCenters[8]-10,-2.5), width = 20, height = 3, alpha = 0.5, color = 'y')
ax.add_patch(patch)
plt.legend(loc=4)
plt.ylim([-2.2,.4])
plt.xlabel('time delay (fs)')

ax = plt.subplot(8,1,8)
plt.plot([6401.1, 6404.1], [0,0], color = 'k', zorder = 0)
plt.scatter(Energy155, Y155[8], color = 'r', zorder = 1)
plt.scatter(Energy123, Y123[8], color = 'darkorange', zorder = 2)
plt.scatter(Energy144, Y144[8], color = 'k', zorder = 3)
plt.scatter(Energy165, Y165[8], color = 'g', zorder = 4)
plt.scatter(Energy131, Y131[8], color = 'b', zorder = 5)
plt.scatter(Energy180, Y180[8], color = 'purple', zorder = 6)
plt.xlim([6401.1, 6404.1])
plt.xlabel('energy (eV)')
plt.ylabel('peak %$\Delta$')
ax.set_yticks([-2,2])
#plt.ylim([-2.2,.4])
#plt.xlabel('time delay (fs)')

fig.text(0.04, 1-.41, '%$\Delta$ emission', va='center', rotation='vertical')
plt.ylim([-2.75,2.75])
#plt.tight_layout()






