# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:18:42 2020

@author: chelsea
"""


import pickle
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import gauswslope
import numpy as np
import matplotlib.pyplot as plt



#folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"
folder = "C:/Users/chels/Downloads/LCLS_python_data/LCLS_python_data/XAS_Spectra/"

with open(folder + "XASDiffBoot.pkl", "rb") as f:
    XASDiffBoot = pickle.load(f)
    
with open(folder + "XASDiffBootF.pkl", "rb") as f:
    XASDiffBootF = pickle.load(f)
    
with open(folder + "XASDiffBootE.pkl", "rb") as f:
    XASDiffBootE = pickle.load(f)
    
with open(folder + "XASOffBootF.pkl", "rb") as f:
    XASOffBootF = pickle.load(f)
    
with open(folder + "XASOffBootE.pkl", "rb") as f:
    XASOffBootE = pickle.load(f)

with open(folder + "XASOnBootF.pkl", "rb") as f:
    XASOnBootF = pickle.load(f)
        
with open(folder + "xasProData_one.pkl", "rb") as f:
    xasProData_one = pickle.load(f)
    
    



numboot = 1000

Asig = np.empty(numboot)
Bsig = np.empty(numboot)
Csig = np.empty(numboot)

Ax0 = np.empty(numboot)
Bx0 = np.empty(numboot)
Cx0 = np.empty(numboot)

Aa = np.empty(numboot)
Ba = np.empty(numboot)
Ca = np.empty(numboot)

Aoff = np.empty(numboot)
Boff = np.empty(numboot)
Coff = np.empty(numboot)

Aslope = np.empty(numboot)
Bslope = np.empty(numboot)
Cslope = np.empty(numboot)

errorhit = 0


for ii in range(numboot-1):
    
    try:
            
        Fit,Params,ParamsA,ParamsB,ParamsC,covA,covB,covC = \
            fitXASPiecewiseGauss(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBoot[:,ii+1],-4), np.delete(XASOffBootF,-4), np.delete(XASOnBootF,-4), False)
            
    except:
        
        errorhit += 1


    Asig[ii-errorhit] = abs(ParamsA[0])
    Bsig[ii-errorhit] = abs(ParamsB[0])
    Csig[ii-errorhit] = abs(ParamsC[0])

    Ax0[ii-errorhit] = abs(ParamsA[1])
    Bx0[ii-errorhit] = abs(ParamsB[1])
    Cx0[ii-errorhit] = abs(ParamsC[1])
    
    Aa[ii-errorhit] = abs(ParamsA[2])
    Ba[ii-errorhit] = abs(ParamsB[2])
    Ca[ii-errorhit] = abs(ParamsC[2])
    
    Aoff[ii-errorhit] = abs(ParamsA[3])
    Boff[ii-errorhit] = abs(ParamsB[3])
    Coff[ii-errorhit] = abs(ParamsC[3])
    
    Aslope[ii-errorhit] = abs(ParamsA[4])
    Bslope[ii-errorhit] = abs(ParamsB[4])
    Cslope[ii-errorhit] = abs(ParamsC[4])
    
Asig = Asig[:numboot-errorhit]
Bsig = Bsig[:numboot-errorhit]
Csig = Csig[:numboot-errorhit]

Ax0 = Ax0[:numboot-errorhit]
Bx0 = Bx0[:numboot-errorhit]
Cx0 = Cx0[:numboot-errorhit]

Aa = Aa[:numboot-errorhit]
Ba = Ba[:numboot-errorhit]
Ca = Ca[:numboot-errorhit]

Aoff = Aoff[:numboot-errorhit]
Boff = Boff[:numboot-errorhit]
Coff = Coff[:numboot-errorhit]

Aslope = Aslope[:numboot-errorhit]
Bslope = Bslope[:numboot-errorhit]
Cslope = Cslope[:numboot-errorhit]

cond = np.logical_and.reduce((Ax0>7110, Bx0<7115, Ax0<7113, Aa < 500, Ba < 500, Cx0 < 7200, Cx0 > 7000, Ca < 650))

fitout = {'Asig': np.mean(Asig[cond]), 'Bsig': np.mean(Bsig[cond]), 'Csig': np.mean(Csig[cond]),\
          'Ax0': np.mean(Ax0[cond]), 'Bx0': np.mean(Bx0[cond]), 'Cx0': np.mean(Cx0[cond]),\
          'Ax0unc': np.std(Ax0[cond]), 'Bx0unc': np.std(Bx0[cond]), 'Cx0unc': np.std(Cx0[cond]),\
          'BmA': np.mean(Bx0[cond]-Ax0[cond]), 'BmAunc': np.std(Bx0[cond]-Ax0[cond]), \
          'CmB': np.mean(Cx0[cond]-Bx0[cond]), 'CmBunc': np.std(Cx0[cond]-Bx0[cond]), \
          'Aa': np.mean(Aa[cond]), 'Ba': np.mean(Ba[cond]), 'Ca': np.mean(Ca[cond]),\
          'Aoff': np.mean(Aoff[cond]), 'Boff': np.mean(Boff[cond]), 'Coff': np.mean(Coff[cond]),\
          'Aslope': np.mean(Aslope[cond]), 'Bslope': np.mean(Bslope[cond]), 'Cslope': np.mean(Cslope[cond]),\
          'numpoints': np.sum(cond.astype('int'))}



with open(folder + "FitOuts.pkl", "wb") as f:
    XASDiffBoot = pickle.dump(fitout, f)


print('B A split: ' + str(fitout['BmA']) + ' pm ' + str(fitout['BmAunc']))
print('C B split: ' + str(fitout['CmB']) + ' pm ' + str(fitout['CmBunc']))








    