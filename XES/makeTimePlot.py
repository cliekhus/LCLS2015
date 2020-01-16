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
    plt.annotate('IRF = ' + str(round(params[4],0)) + ' $\pm $ ' + str(round(cov[4],0)) + ' (fs)', (300, -0.015))
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
    


    
    
    
def makeTimePlotThree(TCentersP, TCentersP2, TCentersM, peaksProDataP, peaksProDataP2, peaksProDataM, minTime, maxTime, numzeros, ploton, MakePlots):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXESthree
    from fitXES import fitXESthreeExtra
    import numpy as np
    from fittingfunctions import convolved
    import matplotlib.gridspec as gridspec
    import math
    import scipy.signal as ss
        
    
    pluscolor = '#009E73'
    minuscolor = '#0072b2'
    pluscolor2 = '#e69f00'
    
    
    #Fitp, Fitm, params, info = fitXESthree(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    Fitp, Fitm, params, info = fitXESthreeExtra(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    
    cov= np.sqrt(np.diag(info))
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))
    Fitp2 = np.array(convolved(TCentersP2, params[5], params[2], 0, params[3], params[4]))
    Fitm2 = np.array(convolved(TCentersM, params[7], params[6], 0, params[3], params[4]))

    Residualp = peaksProDataP.XESDiff - Fitp
    Residualm = peaksProDataM.XESDiff - Fitm- Fitm2
    Residualp2 = peaksProDataP2.XESDiff - Fitp2    

    tt = np.linspace(minTime, maxTime, 1000)
    
    if MakePlots:
            
        plt.figure(figsize = (4,5))
        
        plt.plot(TCentersM, peaksProDataM.XESDiff*100, 's', color = minuscolor, markersize = 3)
        plt.plot(TCentersP, peaksProDataP.XESDiff*100, 'o', color = pluscolor, markersize = 3)
        plt.plot(TCentersP2, peaksProDataP2.XESDiff*100, '^', color = pluscolor2, markersize = 3)
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
        plt.xlim([-250, 1400])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
        
        
        plt.figure(figsize = (4,5))
        
        plt.plot(TCentersM, ss.savgol_filter(peaksProDataM.XESDiff*100,5,3), 's', color = minuscolor, markersize = 3)
        plt.plot(TCentersP, ss.savgol_filter(peaksProDataP.XESDiff*100,5,3), 'o', color = pluscolor, markersize = 3)
        plt.plot(TCentersP2, ss.savgol_filter(peaksProDataP2.XESDiff*100,5,3), '^', color = pluscolor2, markersize = 3)
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
        plt.xlim([-250, 1400])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
    
    mt = 200
    
    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>mt]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>mt]))
    bartlettWindowp2 = np.bartlett(len(Residualp2[TCentersP2>mt]))    
    
    Residualp = np.concatenate((Residualp,np.zeros((numzeros))))
    Residualm = np.concatenate((Residualm,np.zeros((numzeros))))
    Residualp2 = np.concatenate((Residualp2,np.zeros((numzeros))))
    
    
    bartlettWindowp = np.concatenate((bartlettWindowp,np.zeros((numzeros))))
    bartlettWindowm = np.concatenate((bartlettWindowm,np.zeros((numzeros))))
    bartlettWindowp2 = np.concatenate((bartlettWindowp2,np.zeros((numzeros))))
    
    TCentersP = np.concatenate((TCentersP,np.linspace(TCentersP[-1]+TCentersP[1]-TCentersP[0], TCentersP[-1]+(TCentersP[1]-TCentersP[0])*numzeros, num=numzeros)))
    TCentersM = np.concatenate((TCentersM,np.linspace(TCentersM[-1]+TCentersM[1]-TCentersM[0], TCentersM[-1]+(TCentersM[1]-TCentersM[0])*numzeros, num=numzeros)))
    TCentersP2 = np.concatenate((TCentersP2,np.linspace(TCentersP2[-1]+TCentersP2[1]-TCentersP2[0], TCentersP2[-1]+(TCentersP2[1]-TCentersP2[0])*numzeros, num=numzeros)))

    

    
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP>mt], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM>mt], bartlettWindowm)])
    FTp2 = np.fft.rfft([x*y for x,y in zip(Residualp2[TCentersP2>mt], bartlettWindowp2)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP>mt]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    if MakePlots:

        plt.figure(figsize = (4,5))
        plt.plot(Freq, np.abs(FTp2), color = pluscolor2, linewidth = 2, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot(Freq, np.abs(FTp), color = pluscolor, linewidth = 2, label = str(peaksProDataP.EnergyLabel) +' eV', linestyle = ':')
        plt.plot(Freq, np.abs(FTm), color = minuscolor, linewidth = 2, label = str(peaksProDataM.EnergyLabel) + ' eV', linestyle = '--')
        plt.legend()
        
        
        #plt.plot([0,1000], [0.004,0.004], color = minuscolor, linestyle = '--')
        #plt.plot([0,1000], [0.005+0.01, 0.005+0.01], color = pluscolor, linestyle = ':')
        #plt.plot([0,1000], [0.0065+0.02, 0.0065+0.02], color = pluscolor2)
        
        
        #plt.plot([0,1000], [0.01, 0.01], linewidth = 0.5, color = 'k')
        #plt.plot([0,1000], [0.02, 0.02], linewidth = 0.5, color = 'k')
        
        #plt.annotate(str(peaksProDataM.EnergyLabel) +' eV', (372, 0.008))
        #plt.annotate(str(peaksProDataP.EnergyLabel) +' eV', (372, 0.018))
        #plt.annotate(str(peaksProDataP2.EnergyLabel) +' eV', (372, 0.028))
        
        
        plt.ylabel('fourier amplitude')
        plt.xlabel('cm$^{-1}$')
        plt.xlim([0,500])
        plt.ylim([0,0.017])
        plt.tight_layout()
    
    return params, cov, Freq, FTp, FTm, FTp2







def makeTimePlotThreeError(TCentersP, TCentersP2, TCentersM, peaksProDataP, peaksProDataP2, peaksProDataM, minTime, maxTime, numzeros, ploton, MakePlots):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXESthree
    from fitXES import fitXESthreeExtra
    import numpy as np
    from fittingfunctions import convolved
    import matplotlib.gridspec as gridspec
    import math
    import scipy.signal as ss
        
    
    pluscolor = '#009E73'
    minuscolor = '#0072b2'
    pluscolor2 = '#e69f00'
    
    
#    Fitp, Fitm, params, info = fitXESthree(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    Fitp, Fitm, params, info = fitXESthreeExtra(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    print(params)
    cov= np.sqrt(np.diag(info))
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))
    Fitp2 = np.array(convolved(TCentersP2, params[5], params[2], 0, params[3], params[4]))
    Fitm2 = np.array(convolved(TCentersM, params[7], params[6], 0, params[3], params[4]))

    Residualp = peaksProDataP.XESDiff - Fitp
    Residualm = peaksProDataM.XESDiff - Fitm- Fitm2
    Residualp2 = peaksProDataP2.XESDiff - Fitp2    

    tt = np.linspace(minTime, maxTime, 1000)
    
    if MakePlots:
            
        plt.figure(figsize = (4,5))
        
        plt.errorbar(TCentersM, peaksProDataM.XESDiff*100, peaksProDataM.XESDiffE*100, marker = 's', color = minuscolor, markersize = 3, linestyle = 'none')
        plt.errorbar(TCentersP2, peaksProDataP2.XESDiff*100, peaksProDataP2.XESDiffE*100, marker = '^', color = pluscolor2, markersize = 3, linestyle = 'none')
        plt.errorbar(TCentersP, peaksProDataP.XESDiff*100, peaksProDataP.XESDiffE*100, marker = 'o', color = pluscolor, markersize = 3, linestyle = 'none')
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
        plt.xlim([-250, 1400])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
        
        
        plt.figure(figsize = (4,5))
        
        plt.plot(TCentersM, ss.savgol_filter(peaksProDataM.XESDiff*100,5,3), 's', color = minuscolor, markersize = 3)
        plt.plot(TCentersP2, ss.savgol_filter(peaksProDataP2.XESDiff*100,5,3), '^', color = pluscolor2, markersize = 3)
        plt.plot(TCentersP, ss.savgol_filter(peaksProDataP.XESDiff*100,5,3), 'o', color = pluscolor, markersize = 3)
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
        plt.xlim([-250, 1400])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
    
    mt = 200
    
    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>mt]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>mt]))
    bartlettWindowp2 = np.bartlett(len(Residualp2[TCentersP2>mt]))    
    
    Residualp = np.concatenate((Residualp,np.zeros((numzeros))))
    Residualm = np.concatenate((Residualm,np.zeros((numzeros))))
    Residualp2 = np.concatenate((Residualp2,np.zeros((numzeros))))
    
    
    bartlettWindowp = np.concatenate((bartlettWindowp,np.zeros((numzeros))))
    bartlettWindowm = np.concatenate((bartlettWindowm,np.zeros((numzeros))))
    bartlettWindowp2 = np.concatenate((bartlettWindowp2,np.zeros((numzeros))))
    
    TCentersP = np.concatenate((TCentersP,np.linspace(TCentersP[-1]+TCentersP[1]-TCentersP[0], TCentersP[-1]+(TCentersP[1]-TCentersP[0])*numzeros, num=numzeros)))
    TCentersM = np.concatenate((TCentersM,np.linspace(TCentersM[-1]+TCentersM[1]-TCentersM[0], TCentersM[-1]+(TCentersM[1]-TCentersM[0])*numzeros, num=numzeros)))
    TCentersP2 = np.concatenate((TCentersP2,np.linspace(TCentersP2[-1]+TCentersP2[1]-TCentersP2[0], TCentersP2[-1]+(TCentersP2[1]-TCentersP2[0])*numzeros, num=numzeros)))

    

    
    
    
    if MakePlots:
            
        plt.figure(figsize = (4,5))
        plt.errorbar(peaksProDataP.Freq, peaksProDataP.FT+0.01, peaksProDataP.FTE, color = pluscolor, linewidth = 2, label = str(peaksProDataP.EnergyLabel) +' eV', linestyle = ':')
        plt.errorbar(peaksProDataP2.Freq, peaksProDataP2.FT+0.005, peaksProDataP2.FTE, color = pluscolor2, linewidth = 2, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.errorbar(peaksProDataM.Freq, peaksProDataM.FT, peaksProDataM.FTE, color = minuscolor, linewidth = 2, label = str(peaksProDataM.EnergyLabel) + ' eV', linestyle = '--')
        plt.legend()
        
        
        #plt.plot([0,1000], [0.004,0.004], color = minuscolor, linestyle = '--')
        #plt.plot([0,1000], [0.005+0.01, 0.005+0.01], color = pluscolor, linestyle = ':')
        #plt.plot([0,1000], [0.0065+0.02, 0.0065+0.02], color = pluscolor2)
        
        
        #plt.plot([0,1000], [0.01, 0.01], linewidth = 0.5, color = 'k')
        #plt.plot([0,1000], [0.02, 0.02], linewidth = 0.5, color = 'k')
        
        #plt.annotate(str(peaksProDataM.EnergyLabel) +' eV', (372, 0.008))
        #plt.annotate(str(peaksProDataP.EnergyLabel) +' eV', (372, 0.018))
        #plt.annotate(str(peaksProDataP2.EnergyLabel) +' eV', (372, 0.028))
        
        
        plt.ylabel('fourier amplitude')
        plt.xlabel('cm$^{-1}$')
        plt.xlim([0,500])
        plt.ylim([0,0.03])
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
    
    
    
    mt = 200
        
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>mt]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>mt]))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp[TCentersP>mt], bartlettWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm[TCentersM>mt], bartlettWindowm)])
    
    Freq = np.fft.rfftfreq(len(Residualp[TCentersP>mt]), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    
    
    
    return FTp, FTm, Freq




def makeOneBootFT(TCenters, XESDiff, minTime, maxTime, starta, startrate, startsig, PM, ploton):
        
    from fitXES import fitOneXES
    import numpy as np
    from fittingfunctions import convolvedzero

    TCenters = np.ndarray.flatten(TCenters)
    XESDiff = np.ndarray.flatten(XESDiff)

    Fit, params, info = fitOneXES(TCenters, XESDiff, 0, PM*starta, startrate, startsig, ploton)
    
    Fit = np.array(convolvedzero(TCenters, params[0], params[1], params[2], params[3]))


    Residual = XESDiff - Fit
    
    #minFTtime = -1500
    minFTtime = 200
        
    bartlettWindow = np.bartlett(len(Residual[TCenters>minFTtime]))
    
    FT = np.fft.rfft([x*y for x,y in zip(Residual[TCenters>minFTtime], bartlettWindow)])
    
    Freq = np.fft.rfftfreq(len(Residual[TCenters>minFTtime]), d=(TCenters[0]-TCenters[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    
    
    
    return FT, Freq, params



def makenofitBootFT(TCenters, XESDiff, ploton):
        
    from fitXES import fitOneXES
    import numpy as np
    from fittingfunctions import convolvedzero

    TCenters = np.ndarray.flatten(TCenters)
    XESDiff = np.ndarray.flatten(XESDiff)


    Residual = XESDiff 
    
    minFTtime = 60
        
    bartlettWindow = np.bartlett(len(Residual[TCenters>minFTtime]))
    
    FT = np.fft.rfft([x*y for x,y in zip(Residual[TCenters>minFTtime], bartlettWindow)])
    
    Freq = np.fft.rfftfreq(len(Residual[TCenters>minFTtime]), d=(TCenters[0]-TCenters[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    
    
    
    return FT, Freq, 0









def makeTimePlotSubPlot(FeIIIEnergy, FeIIISignal, FeIIEnergy, FeIISignal, TCentersP, TCentersP2, TCentersM, peaksProDataP, peaksProDataP2, peaksProDataM, minTime, maxTime, numzeros, ploton, MakePlots):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXESthree
    from fitXES import fitXESthreeExtra
    import numpy as np
    from fittingfunctions import convolved
    import matplotlib.gridspec as gridspec
    import math
    import scipy.signal as ss
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
        
    
    pluscolor = '#009E73'
    minuscolor = '#0072b2'
    pluscolor2 = '#e69f00'
    
    pcolorlight = "#00d39a"
    mcolorlight = "#00a3ff"
    p2colorlight = "#ffcb56"
    
    
    xlimL = min(FeIIEnergy*1000)
    xlimH = max(FeIIEnergy*1000)

#    Fitp, Fitm, params, info = fitXESthree(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    Fitp, Fitm, params, info = fitXESthreeExtra(TCentersP, TCentersP2, TCentersM, peaksProDataP.XESDiff, peaksProDataP2.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    print(params)
    cov= np.sqrt(np.diag(info))
    
    Fitp = np.array(convolved(TCentersP, params[0], params[2], 0, params[3], params[4]))
    Fitm = np.array(convolved(TCentersM, params[1], params[2], 0, params[3], params[4]))
    Fitp2 = np.array(convolved(TCentersP2, params[5], params[2], 0, params[3], params[4]))
    Fitm2 = np.array(convolved(TCentersM, params[7], params[6], 0, params[3], params[4]))

    Residualp = peaksProDataP.XESDiff - Fitp
    Residualm = peaksProDataM.XESDiff - Fitm- Fitm2
    Residualp2 = peaksProDataP2.XESDiff - Fitp2    

    tt = np.linspace(minTime, maxTime, 1000)
    
    if MakePlots:
            
        fig, ax = plt.subplots(figsize = (4,6))
        
        
                
        plt.plot(TCentersM, peaksProDataM.XESDiff*100, marker = 's', color = minuscolor, markersize = 3, linestyle = 'none')
        plt.plot(TCentersP2, peaksProDataP2.XESDiff*100+.5, marker = '^', color = pluscolor2, markersize = 3, linestyle = 'none')
        plt.plot(TCentersP, peaksProDataP.XESDiff*100+1, marker = 'o', color = pluscolor, markersize = 3, linestyle = 'none')


        plt.errorbar(TCentersM, peaksProDataM.XESDiff*100, peaksProDataM.XESDiffE*100, marker = 's', color = minuscolor, markersize = 3, linestyle = 'none')
        plt.errorbar(TCentersP2, peaksProDataP2.XESDiff*100+.5, peaksProDataP2.XESDiffE*100, marker = '^', color = pluscolor2, markersize = 3, linestyle = 'none')
        plt.errorbar(TCentersP, peaksProDataP.XESDiff*100+1, peaksProDataP.XESDiffE*100, marker = 'o', color = pluscolor, markersize = 3, linestyle = 'none')
     
        """
        plt.fill_between(TCentersM, peaksProDataM.XESDiff*100+peaksProDataM.XESDiffE*100, peaksProDataM.XESDiff*100-peaksProDataM.XESDiffE*100, color = mcolorlight)
        plt.fill_between(TCentersP2, peaksProDataP2.XESDiff*100+peaksProDataP2.XESDiffE*100, peaksProDataP2.XESDiff*100-peaksProDataP2.XESDiffE*100, color = p2colorlight)
        plt.fill_between(TCentersP, peaksProDataP.XESDiff*100+peaksProDataP.XESDiffE*100, peaksProDataP.XESDiff*100-peaksProDataP.XESDiffE*100, color = pcolorlight)
        """
        
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100+.5, color = pluscolor2)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100+1, linestyle = ':', color = pluscolor)
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (750, 2))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (750, 1.7))
        plt.xlim([-250, 1400])
        plt.ylim([-3, 3.1])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
        axins = inset_axes(ax, width=1.75, height=.5, bbox_to_anchor=(1, .39), bbox_transform=ax.transAxes)
        #axins.plot(range(10), range(10))

        #plt.figure(figsize = (4,5))

        #gridspec.GridSpec(10,1)
        
        #ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
        #ax1 = axins.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)    
        plt.rcParams.update({'mathtext.default': 'regular' }     )
        axins.plot(FeIIEnergy*1000, FeIISignal/100000, color = 'k', linewidth = 0.85, label = 'Fe$^{II}$')
        axins.plot(FeIIIEnergy*1000, FeIIISignal/100000, color = 'k', linewidth = 0.85, linestyle='--', label = 'Fe$^{III}$')
        axins.set_xlim([xlimL, xlimH])
        axins.set_xticks(np.arange(6397, 6412, 4))
        axins.set_xticklabels([])
        leg = axins.legend(bbox_to_anchor=(0.03, 1.5), loc='upper left', borderaxespad=0., facecolor = 'white', handlelength = 1.2)
        leg.get_frame().set_alpha(1)
        #plt.ylabel('emission')
        #axins.legend()
        #plt.tight_layout()

        axins2 = inset_axes(ax, width=1.75, height=.8, bbox_to_anchor=(1, .27), bbox_transform=ax.transAxes)
        #ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
        axins2.plot(FeIIIEnergy*1000, (FeIIISignal-FeIISignal)/FeIISignal*100, color = 'k', linewidth = 0.85)
        axins2.annotate('', xy=(peaksProDataP.EnergyLabel,0.2*100), xytext=(peaksProDataP.EnergyLabel,-0.13*100), arrowprops={'arrowstyle': '->', 'ls': 'dotted', 'ec': pluscolor, 'lw': 2})
        axins2.annotate('', xy=(peaksProDataM.EnergyLabel,-0.13*100), xytext=(peaksProDataM.EnergyLabel,0.2*100), arrowprops={'arrowstyle': '->', 'ls': 'dashed', 'ec': minuscolor, 'lw': 2})
        axins2.annotate('', xy=(peaksProDataP2.EnergyLabel,0.2*100), xytext=(peaksProDataP2.EnergyLabel,-0.13*100), arrowprops={'arrowstyle': '->', 'ec': pluscolor2, 'lw': 2})
        axins2.set_xlim([xlimL, xlimH])
        axins2.set_xticks(np.arange(6397, 6412, 4))
        axins2.set_xlabel('energy (eV)')
        #axins2.set_ylabel('%$\Delta$ emission')
        #plt.ylim([-4, 4])
        #plt.xlim([xlimL, xlimH])
        #plt.xticks(np.arange(6397, 6412, 4))
        #plt.tight_layout()
        
    
        
        
        plt.figure(figsize = (4,5))
        
        plt.plot(TCentersM, ss.savgol_filter(peaksProDataM.XESDiff*100,5,3), 's', color = minuscolor, markersize = 3)
        plt.plot(TCentersP2, ss.savgol_filter(peaksProDataP2.XESDiff*100,5,3), '^', color = pluscolor2, markersize = 3)
        plt.plot(TCentersP, ss.savgol_filter(peaksProDataP.XESDiff*100,5,3), 'o', color = pluscolor, markersize = 3)
        plt.plot(tt, np.array(convolved(tt, params[1], params[2], 0, params[3], params[4]))*100+np.array(convolved(tt, params[7], params[6], 0, params[3], params[4]))*100, linestyle = '--', color = minuscolor)
        plt.plot(tt, np.array(convolved(tt, params[5], params[2], 0, params[3], params[4]))*100, color = pluscolor2)
        plt.plot(tt, np.array(convolved(tt, params[0], params[2], 0, params[3], params[4]))*100, linestyle = ':', color = pluscolor)
        plt.plot([-1000, -1000], [0.02, 0.02], 'o', color = pluscolor, markerfacecolor = pluscolor, markeredgecolor = pluscolor, linestyle = ':', markersize = 3, label = str(peaksProDataP.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], '^', color = pluscolor2, markerfacecolor = pluscolor2, markeredgecolor = pluscolor2, linestyle = 'solid', markersize = 3, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.plot([-1000, -1000], [0.02, 0.02], 's', color = minuscolor, fillstyle = 'none', markerfacecolor = minuscolor, markeredgecolor = minuscolor, linestyle = '--', markersize = 3, label = str(peaksProDataM.EnergyLabel) +' eV')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs')
        #plt.plot([-1000, -1000], [0.02, 0.02], linestyle = 'none', label = 'IRF = ' + str(int(params[4]*math.sqrt(2*math.log(2)))) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs')
        plt.ylabel('%$\Delta$ emission')
        plt.legend()
        plt.annotate('BET = ' + str(int(params[2]*math.log(2))) + ' $\pm $ ' + str(int(cov[2]*math.log(2))) + ' fs', (450, -1.1))
        plt.annotate('IRF = ' + str(int(params[4])) + ' $\pm $ ' + str(int(cov[4]*math.log(2))) + ' fs', (450, -1.45))
        plt.xlim([-250, 1400])
        plt.xlabel('time delay (fs)')
        plt.tight_layout()
        
        
    
    mt = 200
    
    
    bartlettWindowp = np.bartlett(len(Residualp[TCentersP>mt]))
    bartlettWindowm = np.bartlett(len(Residualm[TCentersM>mt]))
    bartlettWindowp2 = np.bartlett(len(Residualp2[TCentersP2>mt]))    
    
    Residualp = np.concatenate((Residualp,np.zeros((numzeros))))
    Residualm = np.concatenate((Residualm,np.zeros((numzeros))))
    Residualp2 = np.concatenate((Residualp2,np.zeros((numzeros))))
    
    
    bartlettWindowp = np.concatenate((bartlettWindowp,np.zeros((numzeros))))
    bartlettWindowm = np.concatenate((bartlettWindowm,np.zeros((numzeros))))
    bartlettWindowp2 = np.concatenate((bartlettWindowp2,np.zeros((numzeros))))
    
    TCentersP = np.concatenate((TCentersP,np.linspace(TCentersP[-1]+TCentersP[1]-TCentersP[0], TCentersP[-1]+(TCentersP[1]-TCentersP[0])*numzeros, num=numzeros)))
    TCentersM = np.concatenate((TCentersM,np.linspace(TCentersM[-1]+TCentersM[1]-TCentersM[0], TCentersM[-1]+(TCentersM[1]-TCentersM[0])*numzeros, num=numzeros)))
    TCentersP2 = np.concatenate((TCentersP2,np.linspace(TCentersP2[-1]+TCentersP2[1]-TCentersP2[0], TCentersP2[-1]+(TCentersP2[1]-TCentersP2[0])*numzeros, num=numzeros)))

    

    
    
    
    if MakePlots:
            
        plt.figure(figsize = (4,5))
        plt.errorbar(peaksProDataP.Freq, peaksProDataP.FT+0.01, peaksProDataP.FTE, color = pluscolor, linewidth = 2, label = str(peaksProDataP.EnergyLabel) +' eV', linestyle = ':')
        plt.errorbar(peaksProDataP2.Freq, peaksProDataP2.FT+0.005, peaksProDataP2.FTE, color = pluscolor2, linewidth = 2, label = str(peaksProDataP2.EnergyLabel) +' eV')
        plt.errorbar(peaksProDataM.Freq, peaksProDataM.FT, peaksProDataM.FTE, color = minuscolor, linewidth = 2, label = str(peaksProDataM.EnergyLabel) + ' eV', linestyle = '--')
        plt.legend()
        
        
        #plt.plot([0,1000], [0.004,0.004], color = minuscolor, linestyle = '--')
        #plt.plot([0,1000], [0.005+0.01, 0.005+0.01], color = pluscolor, linestyle = ':')
        #plt.plot([0,1000], [0.0065+0.02, 0.0065+0.02], color = pluscolor2)
        
        
        #plt.plot([0,1000], [0.01, 0.01], linewidth = 0.5, color = 'k')
        #plt.plot([0,1000], [0.02, 0.02], linewidth = 0.5, color = 'k')
        
        #plt.annotate(str(peaksProDataM.EnergyLabel) +' eV', (372, 0.008))
        #plt.annotate(str(peaksProDataP.EnergyLabel) +' eV', (372, 0.018))
        #plt.annotate(str(peaksProDataP2.EnergyLabel) +' eV', (372, 0.028))
        
        
        plt.ylabel('fourier amplitude')
        plt.xlabel('cm$^{-1}$')
        plt.xlim([0,500])
        plt.ylim([0,0.03])
        plt.tight_layout()
    
    
