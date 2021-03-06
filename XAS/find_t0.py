"""
Find t0

"""

def find_t0_XAS(TTSteps, Peak, XAS, ploton):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    
    if XAS:
        
        minrange = -175
        maxrange = -100
    
    else:
        
        minrange = 850
        maxrange = 1050
    
    Filtered = savgol_filter(Peak, 5, 2)
    
    Times = (TTSteps[1:]+TTSteps[:-1])/2
    
    cond = np.logical_and(Times >= minrange, Times <= maxrange) 
    
    plt.figure()
    plt.plot(Times, Peak, 'x')
    
    fit = np.polyfit(Times[cond], Peak[cond], 2)
    
    poly = np.poly1d(fit)
    mintime = -fit[1]/(2*fit[0])    

    times = np.linspace(minrange,maxrange,num=50)
    
    if ploton:
            
        plt.figure()
        plt.plot(Times, Peak, 'x')
        plt.plot(Times, Filtered, marker = 'x')
        plt.plot(times, poly(times))
        plt.plot(mintime, poly(mintime), 'o')
        plt.title('peak is at ' + str(mintime) + ' fs')
        plt.xlabel('time (fs)')
        plt.ylabel('Absorption')

    return mintime

def find_t0_XES(Times, Peak, ploton):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    from itertools import compress
    
    minrange = -1600
    maxrange = -1440
    
    Filtered = savgol_filter(Peak, 5, 2)
    
    cond = [x >= minrange and x <= maxrange for x in Times] 
    
    fit = np.polyfit(list(compress(Times, cond)), list(compress(Peak, cond)), 2)
    poly = np.poly1d(fit)
    mintime = -fit[1]/(2*fit[0])    

    times = np.linspace(minrange,maxrange,num=50)
    
    if ploton:
            
        plt.figure()
        plt.plot(Times, Peak, 'x')
        plt.plot(Times, Filtered, marker = 'x')
        plt.plot(times, poly(times))
        plt.plot(mintime, poly(mintime), 'o')
        plt.title('peak is at ' + str(mintime) + ' fs')
        plt.xlabel('time (fs)')
        plt.ylabel('Absorption')

    return mintime