# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:21:20 2019

@author: chelsea
"""

def makeTimePlot(TCentersP, TCentersM, peaksProDataP, peaksProDataM, minTime, maxTime, ploton):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXES
    import numpy as np
    from fittingfunctions import convolved
    import matplotlib.gridspec as gridspec
    import math
        
    
    pluscolor = '#0070DF'
    minuscolor = '#54A60C'
    darkpluscolor = '#004B95'
    darkminuscolor = '#376E08'
    
    
    Fitp, Fitm, params, info = fitXES(TCentersP, TCentersM, peaksProDataP.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    
    cov= np.sqrt(np.diag(info))
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))


    tt = np.linspace(minTime, maxTime, 1000)
    
    plt.figure(figsize = (4,5))
    
    gridspec.GridSpec(10,1)
    
    ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 7)
    plt.plot(TCentersM, peaksProDataM.XESDiff, 's', color = minuscolor, label = str(peaksProDataM.EnergyLabel) +' eV', markersize = 3)
    plt.plot(TCentersP, peaksProDataP.XESDiff, 'o', color = pluscolor, label = str(peaksProDataP.EnergyLabel) +' eV', markersize = 3)
    plt.plot(tt, convolved(tt, params[1], params[2], 0, params[3], params[4]), '--', color = darkminuscolor, label = str(peaksProDataM.EnergyLabel) +' eV fit')
    plt.plot(tt, convolved(tt, params[0], params[2], 0, params[3], params[4]), color = darkpluscolor, label = str(peaksProDataP.EnergyLabel) +' eV fit')
    plt.annotate('BET = ' + str(round(params[2]*math.log(2),0)) + ' $\pm $ ' + str(round(cov[2]*math.log(2),0)) + ' (fs)', (300, -0.01))
    plt.annotate('IRF = ' + str(round(params[4]*math.sqrt(2*math.log(2)),0)) + ' $\pm $ ' + str(round(cov[4]*math.log(2),0)) + ' (fs)', (300, -0.015))
    plt.ylabel('rel. $\Delta$ emission')
    plt.legend()
    plt.tight_layout()
    ax.set_xticklabels([])

    Residualp = peaksProDataP.XESDiff - Fitp
    Residualm = peaksProDataM.XESDiff - Fitm
    
    ax = plt.subplot2grid((10,1), (7,0), colspan = 1, rowspan = 3)
    plt.plot(TCentersM, Residualm, marker = 's', color = minuscolor, label = str(peaksProDataM.EnergyLabel) +' eV', markersize = 3)
    plt.plot(TCentersP, Residualp, marker = 'o', color = pluscolor, label = str(peaksProDataP.EnergyLabel) +' eV', markersize = 3)
    plt.ylabel('residuals')
    plt.xlabel('time delay (fs)')
    plt.tight_layout()
    
    
    
    
        
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>0]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>0]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP>0], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM>0], bartlettWindowm)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP>0]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    plt.figure(figsize = (4,5))
    plt.plot(Freq, np.abs(FTm), color = minuscolor, label = str(peaksProDataM.EnergyLabel) +' eV')
    plt.plot(Freq, np.abs(FTp), color = pluscolor, label = str(peaksProDataP.EnergyLabel) +' eV')
    
    
    
    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP<0]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM<0]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP<0], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM<0], bartlettWindowm)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP<0]), d=(TCentersP[0]-TCentersP[1])*1e-15)

    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    plt.plot(Freq, np.abs(FTm), color = minuscolor, label = str(peaksProDataM.EnergyLabel) +' eV noise', linestyle = '--')
    plt.plot(Freq, np.abs(FTp), color = pluscolor, label = str(peaksProDataP.EnergyLabel) +' eV noise', linestyle = '--')
    
    
    plt.ylabel('fourier amplitude')
    plt.xlabel('cm$^{-1}$')
    plt.xlim([0,500])
    plt.ylim([0,0.03])
    plt.legend()
    plt.tight_layout()

    
    
    
def makeTimePlotThree(TCentersP, TCentersP2, TCentersM, peaksProDataP, peaksProDataP2, peaksProDataM, minTime, maxTime, numzeros, ploton):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXESthree
    import numpy as np
    from fittingfunctions import convolved
    import matplotlib.gridspec as gridspec
    import math
        
    
    pluscolor = '#009E73'
    minuscolor = '#0072b2'
    pluscolor2 = '#e69f00'
    
    
    Fitp, Fitm, params, info = fitXESthree(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    
    cov= np.sqrt(np.diag(info))
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))
    Fitp2 = np.array(convolved(TCentersP2, params[5], params[2], 0, params[3], params[4]))

    Residualp = peaksProDataP.XESDiff - Fitp
    Residualm = peaksProDataM.XESDiff - Fitm
    Residualp2 = peaksProDataP2.XESDiff - Fitp2    

    tt = np.linspace(minTime, maxTime, 1000)
    
    plt.figure(figsize = (4,5))
    
    gridspec.GridSpec(10,1)
    
    ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 7)
    plt.plot(TCentersM, peaksProDataM.XESDiff*100, 's', color = minuscolor, markersize = 3)
    plt.plot(TCentersP, peaksProDataP.XESDiff*100, 'o', color = pluscolor, markersize = 3)
    plt.plot(TCentersP2, peaksProDataP2.XESDiff*100, '^', color = pluscolor2, markersize = 3)
    plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
    plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
    plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
    plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
    plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
    plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
    #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
    #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
    plt.ylabel('%$\Delta$ emission')
    plt.legend()
    plt.tight_layout()
    plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
    plt.annotate('IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
    ax.set_xticklabels([])
    plt.xlim([-500, 1500])


    ax = plt.subplot2grid((10,1), (7,0), colspan = 1, rowspan = 3)
    plt.plot(TCentersM, (Residualm-0.005)*100, marker = 's', color = minuscolor, label = str(peaksProDataM.EnergyLabel) +' eV', linestyle = '--', markersize = 3)
    plt.plot(TCentersP, Residualp*100, marker = 'o', color = pluscolor, label = str(peaksProDataP.EnergyLabel) +' eV', linestyle = ':', markersize = 3)
    plt.plot(TCentersP2, (Residualp2+0.005)*100, marker = '^', color = pluscolor2, label = str(peaksProDataP2.EnergyLabel) +' eV', markersize = 3)
    plt.ylabel('residuals')
    plt.xlabel('time delay (fs)')
    plt.tight_layout()
    plt.xlim([-500, 1500])
    plt.ylim([-1.2, 1.2])
    
    
    
    Residualp = np.concatenate((Residualp,np.zeros((numzeros))))
    Residualm = np.concatenate((Residualm,np.zeros((numzeros))))
    Residualp2 = np.concatenate((Residualp2,np.zeros((numzeros))))
    
    TCentersP = np.concatenate((TCentersP,np.linspace(TCentersP[-1]+TCentersP[1]-TCentersP[0], TCentersP[-1]+(TCentersP[1]-TCentersP[0])*numzeros, num=numzeros)))
    TCentersM = np.concatenate((TCentersM,np.linspace(TCentersM[-1]+TCentersM[1]-TCentersM[0], TCentersM[-1]+(TCentersM[1]-TCentersM[0])*numzeros, num=numzeros)))
    TCentersP2 = np.concatenate((TCentersP2,np.linspace(TCentersP2[-1]+TCentersP2[1]-TCentersP2[0], TCentersP2[-1]+(TCentersP2[1]-TCentersP2[0])*numzeros, num=numzeros)))

    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>0]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>0]))
    bartlettWindowp2 = np.bartlett(len(Residualp2[TCentersP2>0]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP>0], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM>0], bartlettWindowm)])
    FTp2 = np.fft.rfft([x*y for x,y in zip(Residualp2[TCentersP2>0], bartlettWindowp2)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP>0]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    print('length of freq')
    print(len(Freq))
    
    plt.figure(figsize = (4,5))
    plt.plot(Freq, np.abs(FTm), color = minuscolor, linewidth = 2, linestyle = '--')
    plt.plot(Freq, np.abs(FTp)+0.01, color = pluscolor, linewidth = 2, label = str(peaksProDataP.EnergyLabel) +' eV', linestyle = ':')
    plt.plot(Freq, np.abs(FTp2)+0.02, color = pluscolor2, linewidth = 2, label = str(peaksProDataP2.EnergyLabel) +' eV')
    
    
    
    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP<0]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM<0]))
    bartlettWindowp2 = np.bartlett(len(Residualp2[TCentersP2<0]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP<0], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM<0], bartlettWindowm)])
    FTp2 = np.fft.rfft([x*y for x,y in zip(Residualp2[TCentersP<0], bartlettWindowp2)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP<0]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    plt.plot(Freq, np.abs(FTm), color = minuscolor, linestyle = '--')
    plt.plot(Freq, np.abs(FTp)+0.01, color = pluscolor, linestyle = ':')
    plt.plot(Freq, np.abs(FTp2)+0.02, color = pluscolor2)
    
    
    plt.plot([0,1000], [0.01, 0.01], linewidth = 0.5, color = 'k')
    plt.plot([0,1000], [0.02, 0.02], linewidth = 0.5, color = 'k')
    
    plt.annotate(str(peaksProDataM.EnergyLabel) +' eV', (372, 0.008))
    plt.annotate(str(peaksProDataP.EnergyLabel) +' eV', (372, 0.018))
    plt.annotate(str(peaksProDataP2.EnergyLabel) +' eV', (372, 0.035))
    
    
    plt.ylabel('fourier amplitude')
    plt.xlabel('cm$^{-1}$')
    plt.xlim([0,500])
    plt.ylim([0,0.037])
    plt.tight_layout()
    












def makeBootFT(TCentersP, TCentersM, XESDiffP, XESDiffM, minTime, maxTime, ploton):
        
    from fitXES import fitXES
    import numpy as np
    from fittingfunctions import convolved
  
    
    Fitp, Fitm, params, info = fitXES(TCentersP, TCentersM, XESDiffP, XESDiffM, 0, ploton)
    
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))


    Residualp = XESDiffP - Fitp
    Residualm = XESDiffM - Fitm
    
    
    
    
        
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>0]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>0]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP>0], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM>0], bartlettWindowm)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP>0]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    
    
    
    return FTp, FTm, Freq




def makeOneBootFT(TCenters, XESDiff, minTime, maxTime, starta, startrate, startsig, ploton):
        
    from fitXES import fitOneXES
    import numpy as np
    from fittingfunctions import convolved

    Fit, params, info = fitOneXES(TCenters, XESDiff, 0, starta, startrate, startsig, ploton)
    
    
    Fit = np.array(convolved(TCenters, params[0], params[1], 0, params[2], params[3]))


    Residual = XESDiff - Fit
    
    
    
    
        
    bartlettWindow = np.bartlett(len(Residual[TCenters>0]))
    
    FT = np.fft.rfft([x*y for x,y in zip(Residual[TCenters>0], bartlettWindow)])
    
    Freq = np.fft.rfftfreq(len(Residual[TCenters>0]), d=(TCenters[0]-TCenters[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    
    
    
    return FT, Freq