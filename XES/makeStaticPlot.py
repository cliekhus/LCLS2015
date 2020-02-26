# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 10:39:27 2019

@author: chelsea
"""
def makeStaticPlot(xesProData):
    
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    import pickle
    
    with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataPF.pkl", "rb") as f:
        peaksProDataP = pickle.load(f)

    
    with open("D:\LCLS_Data\LCLS_python_data\XES_TimeResolved\peaksProDataMF.pkl", "rb") as f:
        peaksProDataM = pickle.load(f)
    
    pluscolor = '#0070DF'
    minuscolor = '#54A60C'
    
    xlimspan = 4.0
    xlimL = xesProData.KaEnergy[xesProData.XESOff_Norm.argmax()]-xlimspan
    xlimH = xesProData.KaEnergy[xesProData.XESOff_Norm.argmax()]+xlimspan
    
    plt.figure(figsize = (4,5))
    
    gridspec.GridSpec(10,1)

    ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
    plt.errorbar(xesProData.KaEnergy, xesProData.XESOff_Norm, xesProData.Error_Off, color = 'k')
    plt.xlim([xlimL, xlimH])
    ax.set_xticklabels([])
    plt.ylabel('emission (arb.)')
    plt.tight_layout()
    
    ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
    plt.errorbar(xesProData.KaEnergy, (xesProData.XESOn_Norm - xesProData.XESOff_Norm)/xesProData.XESOff_Norm*100, np.sqrt(xesProData.Error_On**2+xesProData.Error_On**2)/xesProData.XESOff_Norm*100, color = 'k')
    ax.annotate('', xy=(peaksProDataP.EnergyLabel,1.5), xytext=(peaksProDataP.EnergyLabel,-0.5), arrowprops={'arrowstyle': '->', 'ec': pluscolor, 'lw': 3})
    ax.annotate('', xy=(peaksProDataM.EnergyLabel,-0.5), xytext=(peaksProDataM.EnergyLabel,1.5), arrowprops={'arrowstyle': '->', 'ec': minuscolor, 'lw': 3})
    plt.xlabel('energy (eV)')
    plt.ylabel('% $\Delta$ emission')
    #plt.ylim([-4, 4])
    plt.xlim([xlimL, xlimH])
    plt.tight_layout()