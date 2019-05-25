# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:55:23 2019

@author: chelsea
"""

def convertPixel2Energy(RowlandYRaw):
    
    import numpy as np
    
    startpixel = 55
    endpixel = 90
    
    RowlandY = [0 for y in range(len(RowlandYRaw))]
    
    for ii in range(len(RowlandYRaw)):
        RowlandY[ii] = RowlandYRaw[ii][startpixel:(endpixel+1)]
    
    spectra = np.linspace(startpixel, endpixel-1, endpixel-startpixel+1)
    
    return spectra, RowlandY