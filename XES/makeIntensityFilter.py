# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:47 2019

@author: chelsea
"""

def makeLineFilter(Diode2, Cspad, selectedRuns, ploton):
    

    import matplotlib.pyplot as plt
    import numpy as np
    
    if ploton:
            
        plt.figure()
        plt.scatter(Cspad[selectedRuns], Diode2[selectedRuns],s=2)
    
    if sum(selectedRuns.astype(int))>0:
            
        linfit = np.polyfit(Cspad[selectedRuns],Diode2[selectedRuns], 1)
        line = np.poly1d(linfit)
        res = line(Cspad)-Diode2
        statstdev = np.std(res[selectedRuns])
    
        if ploton:
            
            plt.plot(Cspad, line(Cspad))
        
        numstds = 1.5
        slopefilter = np.abs(res) < numstds*statstdev
        
        plotfilter = np.logical_and(np.abs(res) < numstds*statstdev, selectedRuns)
        
        if ploton:
            
            plt.scatter(Cspad[plotfilter], Diode2[plotfilter], s=2, c='r')
            plt.title(linfit[1])
            plt.xlabel('Diode')
            plt.ylabel('Rowland')
            print(linfit[1])
        
        
        return slopefilter, linfit[1]

    else:
        
        return selectedRuns, float('NaN')






