# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:39:27 2019

@author: chelsea
"""
def makeSpectralPlot(Residual, TCP, noverlap, nperseg, calc):
    
    calcXmax = 2000
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import spectrogram
    import matplotlib.gridspec as gridspec
    
    f,t,Zxx = spectrogram(np.array(Residual), fs = 1/(TCP[1]-TCP[0]), noverlap = noverlap, nperseg = nperseg)
    plt.figure()
    gridspec.GridSpec(5,5)
    
    tmesh = np.concatenate((t, np.array([t[-1]+t[1]-t[0]])))+TCP[0]
    tmesh = tmesh - (tmesh[1]-tmesh[0])/2
    fmesh = np.concatenate((f, np.array([f[-1]+f[1]-f[0]])))*33.356*1000
    fmesh = fmesh - (fmesh[1]-fmesh[0])/2
    
    ax = plt.subplot2grid((5,5), (4,0), colspan = 4, rowspan = 1)
    plt.plot(t+TCP[0], np.sum(np.abs(Zxx),0))
    if calc:
        plt.xlim([0,calcXmax])
    else:
        plt.xlim([tmesh[0],tmesh[-1]])
    plt.xlabel('time (fs)')
    
    ax = plt.subplot2grid((5,5), (0,0), colspan = 4, rowspan = 4)
    plt.pcolormesh(tmesh,fmesh,np.abs(np.pad(Zxx, (0,1), 'constant', constant_values = (0))))
    ax.set_xticklabels([])
    if calc:
        plt.ylim([0,2500])
    else:
        plt.ylim([-(fmesh[1]-fmesh[0])/2,fmesh[-1]])
    if calc:
        plt.xlim([0,calcXmax])
        plt.clim([0, np.max(Zxx[:,t<=calcXmax])])
    else:
        plt.xlim([tmesh[0],tmesh[-1]])
    plt.ylabel('cm$^{-1}$')
    
    ax = plt.subplot2grid((5,5), (0,4), colspan = 1, rowspan = 4)
    plt.plot(np.sum(np.abs(Zxx),1), f*33.356*1000)
    ax.set_yticklabels([])
    if calc:
        plt.ylim([0,2500])
    else:
        plt.ylim([-(fmesh[1]-fmesh[0])/2,fmesh[-1]])
    
