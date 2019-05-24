# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:55:23 2019

@author: chelsea
"""

def convertPixel2Energy(RowlandY):
    
    import numpy as np
    
    spectra = np.linspace(0,183,len(RowlandY[0]))
    
    return spectra