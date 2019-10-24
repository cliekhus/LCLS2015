# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:39:27 2019

@author: chelsea
"""
def makeStaticPlot(xesProData):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    
    pluscolor = '#0070DF'
    minuscolor = '#54A60C'
    
    xlimspan = 0.004
    xlimL = xesProData.KaEnergy[xesProData.XESOff_Norm.argmax()]-xlimspan
    xlimH = xesProData.KaEnergy[xesProData.XESOff_Norm.argmax()]+xlimspan
    
    plt.figure(figsize = (4,5))
    
    gridspec.GridSpec(10,1)

    ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
    plt.errorbar(xesProData.KaEnergy, xesProData.XESOff_Norm, xesProData.Error_Off, color = 'k')
    plt.xlim([xlimL, xlimH])
    ax.set_xticklabels([])
    plt.tight_layout()
    
    ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
    plt.errorbar(xesProData.KaEnergy, (xesProData.XESOn_Norm - xesProData.XESOff_Norm)/xesProData.XESOff_Norm, np.sqrt(xesProData.Error_On**2+xesProData.Error_On**2)/xesProData.XESOff_Norm, color = 'k')
    ax.annotate('', xy=(6.4029,0.004), xytext=(6.4029,-0.015), arrowprops={'arrowstyle': '->', 'ec': pluscolor, 'lw': 3})
    ax.annotate('', xy=(6.4050,-0.004), xytext=(6.4050,0.015), arrowprops={'arrowstyle': '->', 'ec': minuscolor, 'lw': 3})
    plt.xlabel('energy (keV)')
    plt.ylim([-0.04, 0.04])
    plt.xlim([xlimL, xlimH])
    plt.tight_layout()