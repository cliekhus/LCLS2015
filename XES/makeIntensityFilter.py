# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:47 2019

@author: chelsea
"""

def makeLineFilter(Diode2, Cspad, selectedRuns, ploton):
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    if ploton:
            
        plt.figure(figsize = (3.3,3.3))
        ax = plt.subplot(111)
        plt.scatter(Cspad[selectedRuns]/np.max(Cspad[selectedRuns]), \
                    Diode2[selectedRuns]/np.max(Diode2[selectedRuns]),s=2)
    
    if sum(selectedRuns.astype(int))>0:
            
        linfit = np.polyfit(Cspad[selectedRuns], Diode2[selectedRuns], 1)
        line = np.poly1d(linfit)
        res = line(Cspad)-Diode2
        statstdev = np.std(res[selectedRuns])
    
        if ploton:
            
            plt.plot(Cspad/np.max(Cspad[selectedRuns]), \
                     line(Cspad)/np.max(Diode2[selectedRuns]), color = 'k')
        
        #numstds = 2.5
        numstds = 3
        slopefilter = np.abs(res) < numstds*statstdev
        
        plotfilter = np.logical_and(np.abs(res) < numstds*statstdev, selectedRuns)
        
        if ploton:
            
            plt.scatter(Cspad[plotfilter]/np.max(Cspad[selectedRuns]), \
                        Diode2[plotfilter]/np.max(Diode2[selectedRuns]), s=2)
            plt.xlim([0,1.2])
            plt.ylim([0,1.2])
            plt.title('linear filter')
            plt.xlabel('TFY diode')
            plt.ylabel('rowland measurement')
            plt.tight_layout()
            ax.set_xticks(np.linspace(0,1.2,7))
            ax.set_yticks(np.linspace(0,1.2,7))
            ax.set_aspect('equal')
            print(linfit[1])
        
        
        return slopefilter, linfit[1]

    else:
        
        return selectedRuns, float('NaN')






