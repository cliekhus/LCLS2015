# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:29:47 2019

@author: chelsea
"""

def makeOneDiodeFilter(xasRawData, selectedRuns, ploton):
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    if ploton:
            
        plt.figure()
        #plt.scatter(xasRawData.Ipm2Sum[selectedRuns], xasRawData.Diode2[selectedRuns],s=2)
        plt.scatter(xasRawData.CspadSum[selectedRuns], xasRawData.Diode2[selectedRuns],s=2)
    
    if sum(selectedRuns.astype(int))>0:
            
        #linfit = np.polyfit(xasRawData.Ipm2Sum[selectedRuns], xasRawData.Diode2[selectedRuns], 1)
        linfit = np.polyfit(xasRawData.CspadSum[selectedRuns], xasRawData.Diode2[selectedRuns], 1)
        line = np.poly1d(linfit)
        #res = line(xasRawData.Ipm2Sum)-xasRawData.Diode2
        res = line(xasRawData.CspadSum)-xasRawData.Diode2
        statstdev = np.std(res[selectedRuns])
    
        if ploton:
            
            #plt.plot(xasRawData.Ipm2Sum, line(xasRawData.Ipm2Sum))
            plt.plot(xasRawData.CspadSum, line(xasRawData.CspadSum))
        
        numstds = 3
        slopefilter = np.abs(res) < numstds*statstdev
        
        plotfilter = np.logical_and(np.abs(res) < numstds*statstdev, selectedRuns)
        
        if ploton:
            
            #plt.scatter(xasRawData.Ipm2Sum[plotfilter], xasRawData.Diode2[plotfilter], s=2, c='r')
            plt.scatter(xasRawData.CspadSum[plotfilter], xasRawData.Diode2[plotfilter], s=2, c='r')
            plt.ylabel('diode2')
            plt.xlabel('cspadsum')
        
        
        return slopefilter, -linfit[1]/linfit[0]

    else:
        
        return selectedRuns, float('NaN')













def makeOneRowlandFilter(diode2, rowlandsum, xOn, ploton):
    
    import matplotlib.pyplot as plt
    from itertools import compress
    import math
    import numpy as np
    import statistics as stat
    
    xonnan = [not math.isnan(x) and y and not math.isnan(z) for x,y,z in zip(rowlandsum, xOn, diode2)]
    
    if ploton:
            
        plt.figure()
        plt.scatter(list(compress(diode2, xonnan)), list(compress(rowlandsum, xonnan)),s=2)
    
    meanrowlandsum = stat.mean(list(compress(rowlandsum, xonnan)))
    
    stdrowlandsum = stat.stdev(list(compress(rowlandsum, xonnan)))
    
    stdlimit = 2
    
    rowlandfilter = [abs(x-meanrowlandsum)<stdlimit*stdrowlandsum and y for x,y in zip(rowlandsum, xonnan)]
    
    linfit = np.polyfit(list(compress(diode2, rowlandfilter)), list(compress(rowlandsum, rowlandfilter)), 1)
    line = np.poly1d(linfit)
    rowlandres = [abs(x-y) for x,y in zip(list(line(diode2)),rowlandsum)]
    statstdev = stat.stdev(list(compress(rowlandres, rowlandfilter)))
    
    
    
    
    if ploton:
        
        plt.plot(list(compress(diode2,rowlandres)), list(line(list(compress(diode2,rowlandres)))))
    
    numstds = 2
    
    slopefilter = [a < numstds*statstdev and b for a,b in zip(rowlandres,rowlandfilter)]
    
    if ploton:
        
        plt.scatter(list(compress(diode2, slopefilter)),list(compress(rowlandsum,slopefilter)),s=2,c='r')
        plt.xlabel('diode2')
        plt.ylabel('rowlandsum')
    
    
    return slopefilter, -linfit[1]/linfit[0]
















def makeRowlandFilter(diode2, rowlandsum, xOn, lon, ploton):
    
    import matplotlib.pyplot as plt
    from itertools import compress
    import math
    import numpy as np
    import statistics as stat
    
    xonnan = [not math.isnan(x) and y and not math.isnan(z) for x,y,z in zip(rowlandsum, xOn, diode2)]
    
    if ploton:
            
        plt.figure()
        plt.scatter(list(compress(diode2, xonnan)), list(compress(rowlandsum, xonnan)),s=2)
    
    meanrowlandsumOn = stat.mean(list(compress(rowlandsum, [x and y for x,y in zip(xonnan, lon)])))
    meanrowlandsumOff = stat.mean(list(compress(rowlandsum, [x and not y for x,y in zip(xonnan, lon)])))
    
    stdrowlandsumOn = stat.stdev(list(compress(rowlandsum, [x and y for x,y in zip(xonnan, lon)])))
    stdrowlandsumOff = stat.stdev(list(compress(rowlandsum, [x and not y for x,y in zip(xonnan, lon)])))
    
    stdlimit = 2
    
    rowlandfilteron = [abs(x-meanrowlandsumOn)<stdlimit*stdrowlandsumOn and y and z for x,y,z in zip(rowlandsum, xonnan, lon)]
    
    linfiton = np.polyfit(list(compress(diode2, rowlandfilteron)), list(compress(rowlandsum, rowlandfilteron)), 1)
    lineon = np.poly1d(linfiton)
    rowlandreson = [abs(x-y) for x,y in zip(list(lineon(diode2)),rowlandsum)]
    statstdevon = stat.stdev(list(compress(rowlandreson, rowlandfilteron)))
    
    
    rowlandfilteroff = [abs(x-meanrowlandsumOff)<stdlimit*stdrowlandsumOff and y and not z for x,y,z in zip(rowlandsum, xonnan, lon)]
    
    linfitoff = np.polyfit(list(compress(diode2, rowlandfilteroff)), list(compress(rowlandsum, rowlandfilteroff)), 1)
    lineoff = np.poly1d(linfitoff)
    rowlandresoff = [abs(x-y) for x,y in zip(list(lineoff(diode2)),rowlandsum)]
    statstdevoff = stat.stdev(list(compress(rowlandresoff, rowlandfilteroff)))
    
    
    
    if ploton:
        
        plt.plot(list(compress(diode2,rowlandreson)), list(lineon(list(compress(diode2,rowlandreson)))))
        plt.plot(list(compress(diode2, rowlandresoff)), list(lineon(list(compress(diode2,rowlandresoff)))))
    
    numstds = 1.75
    
    slopefilteron = [a < numstds*statstdevon and b for a,b in zip(rowlandreson,rowlandfilteron)]
    slopefilteroff = [a < numstds*statstdevoff and b for a,b in zip(rowlandresoff,rowlandfilteroff)]
    
    if ploton:
        
        plt.scatter(list(compress(diode2, slopefilteron)),list(compress(rowlandsum,slopefilteron)),s=2,c='r')
        plt.scatter(list(compress(diode2, slopefilteroff)),list(compress(rowlandsum,slopefilteroff)),s=2,c='r')
        plt.xlabel('diode2')
        plt.ylabel('rowlandsum')
    
    
    return slopefilteron, slopefilteroff, -linfiton[1]/linfiton[0], -linfitoff[1]/linfitoff[0]








