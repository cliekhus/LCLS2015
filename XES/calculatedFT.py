# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 18:13:47 2019

@author: chels
"""
import matplotlib.pyplot as plt
import numpy as np
from numpy import loadtxt
from makeSpectralPlot import makeSpectralPlot
import matplotlib.gridspec as gridspec

#plt.close('all')


calc = loadtxt('Fe1s2p-gap-12.out')
#calc = loadtxt('Fe1s3p-gap-123.out')

FT = np.fft.rfft(calc[:,5])

Freq = np.fft.rfftfreq(len(calc[:,5]), d=(calc[0,0]-calc[1,0])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
line0 = plt.plot(Freq, abs(FT))
plt.ylabel('fourier amplitude')
plt.xlabel('cm$^{-1}$')
plt.title('straight FT')
plt.ylim([0,100])
plt.xlim([0,500])

plt.figure()
line0 = plt.plot(Freq, np.angle(FT))
plt.ylabel('phase')
plt.xlabel('cm$^{-1}$')
plt.title('straight FT')
plt.xlim([0,500])


HammingWindow = np.hamming(len(calc[:,5]))

FT = np.fft.rfft([x*y for x,y in zip(calc[:,5], HammingWindow)])

Freq = np.fft.rfftfreq(len(calc[:,5]), d=(calc[0,0]-calc[1,0])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
plt.plot(Freq, abs(FT))
plt.ylabel('fourier amplitude')
plt.xlabel('cm$^{-1}$')
plt.title('with Hamming window')
plt.ylim([0,100])
plt.xlim([0,500])


BlackmanWindow = np.blackman(len(calc[:,5]))

FT = np.fft.rfft([x*y for x,y in zip(calc[:,5], BlackmanWindow)])

Freq = np.fft.rfftfreq(len(calc[:,5]), d=(calc[0,0]-calc[1,0])*1e-15)

Freq = [-x*1e-12*33.356 for x in Freq]

plt.figure()
plt.plot(Freq, abs(FT),)
plt.ylabel('fourier amplitude')
plt.xlabel('cm$^{-1}$')
plt.title('with Blackman window')
plt.ylim([0,100])
plt.xlim([0,500])






makeSpectralPlot(calc[:,5], calc[:,0], 50, 500, True)








plt.figure()
plt.subplot(211)
plt.plot(calc[:,0], np.array(calc[:,5])-np.mean(calc[:,5]))
plt.ylabel('$\Delta$ 2p-1s (eV)')
plt.xlabel('time (fs)')

#gridspec.GridSpec(10,1)

#ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 7)
plt.subplot(212)
plt.plot(Freq, abs(FT), color='k')
plt.ylim([0,60])
plt.xlim([0,500])
plt.xlabel('frequency (cm$^{-1}$)')
plt.ylabel('oscillation strength')
plt.tight_layout()


#ax = plt.subplot2grid((10,1), (7,0), colspan = 1, rowspan = 3)
#plt.plot(calc[:,0], (calc[:,5]-np.mean(calc[:,5]))/np.max(calc[:,5]-np.mean(calc[:,5])))
#plt.xlabel('time (fs)')
#plt.ylabel('1s-2p $\Delta$ energy')
#plt.tight_layout()


def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

nb = 15
nt = 3
chunks = chunkIt(calc[:,5], nt)
times = chunkIt(calc[:,0], nt)

plt.figure()
num,bins,pat = plt.hist(calc[:,5],nb)
average = num/sum(num)
plt.figure(51)
plt.plot(bins[:-1], average, label = 'average')

for ii in range(nt):
    
    plt.figure(50)
    num,bins,pat = plt.hist(chunks[ii],nb)
    plt.figure(51)
    plt.plot(bins[:-1],num/sum(num), label = np.mean(times[ii]))
    plt.legend()
    plt.figure(52)
    plt.plot(bins[:-1], (num/sum(num)-average)/average, label=np.mean(times[ii]))
    
plt.legend()













