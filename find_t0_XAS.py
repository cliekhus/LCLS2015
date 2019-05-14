"""
Find t0

"""

def find_t0_XAS(TTSteps, Peak, ploton):
    
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import savgol_filter
    
    #Filtered = savgol_filter(Peak, 5, 3)
    Filtered = Peak
    MinIndex = np.argmin(Filtered)
    
    Times = []
    
    for ii in range(len(TTSteps)-1):
        Times = Times + [(TTSteps[ii]+TTSteps[ii+1])/2]
        
    if ploton:
            
        plt.figure()
        plt.plot(Times, Peak, 'x')
        plt.plot(Times, Filtered, marker = 'x')
        plt.plot(Times[MinIndex], Filtered[MinIndex], marker = 'o')
        plt.title('peak is at ' + str(Times[MinIndex]) + ' fs')

    return Times[MinIndex]