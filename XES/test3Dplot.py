# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 16:15:20 2019

@author: chelsea
"""



from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import numpy.matlib as npm

#style.use('fivethirtyeight')

color = ['b', 'r', 'g', 'k', 'y', 'm']

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
#ax1.view_init(elev=90,azim=-100)

for jj in range(len(Freq)):
        
    
    Z = np.ndarray.flatten(npm.repmat(Energy[jj],len(Freq[jj]),1))
    ax1.plot(Freq[jj], Z, FTBootF[jj], color=color[jj])
    
    for ii in range(len(Freq[jj])):
        ax1.plot([Freq[jj][ii],Freq[jj][ii]], [Z[ii], Z[ii]], [FTBootF[jj][ii]+FTBootE[jj][ii], FTBootF[jj][ii]-FTBootE[jj][ii]], color=color[jj])
    

ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')
ax1.set_zlim(0,.015)
ax1.set_ylim(6.4012, 6.4041)

plt.show()





fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
#ax1.view_init(elev=90,azim=-100)

for jj in range(len(TCenters)):
        
    
    Z = np.ndarray.flatten(npm.repmat(Energy[jj],len(TCenters[jj]),1))
    ax1.plot(TCenters[jj], Z, PeaksBootF[jj], color=color[jj])
    
    for ii in range(len(TCenters[jj])):
        ax1.plot([TCenters[jj][ii],TCenters[jj][ii]], [Z[ii], Z[ii]], [PeaksBootF[jj][ii]+PeaksBootE[jj][ii], PeaksBootF[jj][ii]-PeaksBootE[jj][ii]], color=color[jj])
    

ax1.set_xlabel('x axis')
ax1.set_ylabel('y axis')
ax1.set_zlabel('z axis')
ax1.set_zlim(0,.015)
ax1.set_ylim(6.4012, 6.4041)

plt.show()