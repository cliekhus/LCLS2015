# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:45:18 2019

@author: chelsea
"""

#NumTTSteps, Diode2, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, FPlots

import random
import math
import numpy as np
import matplotlib.pyplot as plt
from makeXES import makeXES
from itertools import compress

num = 10000
NumTTSteps = 50

TTDelay = [-random.randint(0,2000) for x in range(num)]
#TTDelay = [-x for x in range(num)]

Diode2 = [random.randint(900,1000)/1000 for x in range(num)]

RowlandY = [y*math.exp(-((x+1600)/500)**2) for x,y in zip(TTDelay, Diode2)]

#LOn = [True for x in range(num)]
LOn = [bool(random.randint(0,1)) for x in range(num)]

#XOn = [True for x in range(num)]
XOn = [bool(random.randint(0,1)) for x in range(num)]

RowlandY = [x*int(y)*int(z) for x,y,z in zip(RowlandY, LOn, XOn)]

Filter = [True for x in range(num)]

TTSteps = np.linspace(-2000.5,0,NumTTSteps+1)

FPlots = True

plt.figure(), plt.scatter(TTDelay, RowlandY)

Ideal = [w/x for w,x,y,z in zip(RowlandY, Diode2, LOn, XOn) if y and z and x>0]
Times = [x for w,x,y,z in zip(Diode2, TTDelay, LOn, XOn) if y and z and w>0]

Idealp = []

for ii in range(NumTTSteps):
    filt = [x>=TTSteps[ii] and x < TTSteps[ii+1] for x in Times]
    Idealp = Idealp + [sum(list(compress(Ideal, filt)))/sum([int(x) for x in filt])]

plt.figure(), plt.scatter(Times, Ideal)
plt.figure(), plt.scatter(TTSteps[1:], Idealp)



XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTSteps, Diode2, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)