# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:10:17 2020

@author: chels
"""

def VectorFile(number, wavenumber, D3, savename, legend):
        
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from math import cos, sin, pi
    
    theta = 20/180*pi
    psi = 0/180*pi
    phi = -60/180*pi
    
    x1 = np.array([cos(theta)*cos(psi), -cos(phi)*sin(psi)+sin(phi)*sin(theta)*cos(psi), \
                   sin(phi)*sin(psi)+cos(phi)*sin(theta)*cos(psi)])
    x2 = np.array([cos(theta)*sin(psi), cos(phi)*cos(psi)+sin(phi)*sin(theta)*sin(psi), \
                   -sin(phi)*cos(psi)+cos(phi)*sin(theta)*sin(psi)])
    x3 = np.array([-sin(theta), sin(phi)*cos(theta), cos(phi)*cos(theta)])
    
    #########################################
    #Obviously you'll want to adjust this line
    folder = "C:/Users/chelsea/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/Calculations/FeRu-freq-xyzs/"
    
    f = open(folder+'freq.m-' + str(int(number)).zfill(3) + '.xyz', 'r')
    
    contents = f.read()
    
    data = contents.split('    34\n geometry\n')
    
    frames = np.empty((len(data)-1,len(data[1].split('\n'))-1,3))
    atoms = []
    colors = []
    
    for ii in range(len(data)-1):
        frame = data[ii+1].split('\n')
        
        for jj in range(len(frame)-1):
            pos = frame[jj].split()
            frames[ii,jj,:] = np.array(pos[1:4])
            
            if ii == 0:
                atoms = atoms + [pos[0]]
    
    
    ###########################################
    #Pick which atoms you want to form basis vectors out of.
    Fepos = atoms.index('Fe')
    Rupos = atoms.index('Ru')
    Cpos = atoms[4:].index('C')
    
    PA = frames[0,Rupos,:]-frames[0,Fepos,:]
    PA = PA/(PA.dot(PA))**.5
    PA1 = frames[0,Fepos,:]-frames[0,Cpos+4,:]
    PA1 = PA1 - PA1.dot(PA)*PA
    PA1 = PA1/(PA1.dot(PA1))**.5
    PA2 = np.cross(PA,PA1)
    PA2 = PA2/(PA2.dot(PA2))**.5
    
    framesp = np.empty(np.shape(frames))
    
    for ii in range(len(data)-1):
        for jj in range(len(frame)-1):
            
            framesp[ii,jj,0] = frames[ii,jj,:].dot(PA)
            framesp[ii,jj,1] = frames[ii,jj,:].dot(PA1)
            framesp[ii,jj,2] = frames[ii,jj,:].dot(PA2)
    
    
    fig = plt.figure(figsize = (1.5,1.5))
    if D3:
        ax = fig.add_subplot(111, projection='3d')
    else:
        ax = fig.add_subplot(111)
    
    ###################################
    #Put in your color choices here
    FeC = 'r'
    CC = 'b'
    NC = 'c'
    RuC = 'y'
    HC = 'k'
    
    FeS = 500
    CS = 200
    NS = 200
    RuS = 500
    HS = 100
    
    ###################################
    #Modify this chunk to look for each atom.  set s to the size you want for each atom
    frameNum = 0
    
    
    distance = np.empty((np.shape(frames)[0],np.shape(frames)[1],np.shape(frames)[1]))
    
    for jj in range(np.shape(frames)[0]):
        for ii in range(np.shape(frames)[1]):
            for kk in range(np.shape(frames)[1]):
                distance[jj,ii,kk] = (frames[jj,ii,:]-frames[jj,kk,:]).dot(frames[jj,ii,:]-frames[jj,kk,:])
    
    
    distance[distance==0] = 10000
    
    
    ####################################
    #mindist is the minimum distance to draw a bond.
    #Note that this line "(atoms[jj] !=atoms[ii])" makes it so like atoms don't bond.  
    #You may have to adjust this line to fit your individual needs.
    #You can also change the bond color, or change it's thickness here.
    
    mindist = 4.6
    for jj in range(np.shape(distance)[1]):
        for ii in range(np.shape(distance)[2]):
            if (distance[frameNum,jj,ii] < mindist) and (atoms[jj] !=atoms[ii]):
            
                if D3:
                    ax.plot([framesp[frameNum,jj,0],framesp[frameNum,ii,0]], \
                            [framesp[frameNum,jj,1],framesp[frameNum,ii,1]], \
                            [framesp[frameNum,jj,2],framesp[frameNum,ii,2]], color = 'g')
                else:
                    ax.plot([framesp[frameNum,jj,:].dot(x1), framesp[frameNum,ii,:].dot(x1)], \
                             [framesp[frameNum,jj,:].dot(x2), framesp[frameNum,ii,:].dot(x2)], color = 'g', zorder = ii*jj)
    
    
    sizescale = 0.1
    for jj in range(len(frame)-1):
        
        if not D3:
            D21 = framesp[frameNum,jj,:].dot(x1)
            D22 = framesp[frameNum,jj,:].dot(x2)
            D23 = framesp[frameNum,jj,:].dot(x3)
            order = int(D23*1000+5000)
        
        if atoms[jj] == 'Fe':
            if D3:
                ax.scatter(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
                       color = FeC, s = FeS*sizescale)
            else:
                ax.scatter(D21, D22, color = FeC, s = FeS*sizescale, zorder = order)
                    
        if atoms[jj] == 'C':
            if D3:
                ax.scatter(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
                       color = CC, s = CS*sizescale)
            else:
                ax.scatter(D21, D22, color = CC, s = CS*sizescale, zorder = order)
                
        if atoms[jj] == 'N':
            if D3:
                ax.scatter(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
                       color = NC, s = NS*sizescale)
            else:
                ax.scatter(D21, D22, color = NC, s = NS*sizescale, zorder = order)
                
        if atoms[jj] == 'Ru':
            if D3:
                ax.scatter(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
                       color = RuC, s = RuS*sizescale)
            else:
                ax.scatter(D21, D22, color = RuC, s = RuS*sizescale, zorder = order)
        if atoms[jj] == 'H':
            if D3:
                ax.scatter(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
                       color = HC, s = HS*sizescale)
            else:
                ax.scatter(D21, D22, color = HC, s = HS*sizescale, zorder = order)
    
    ######################################
    #mult controls the relative vector size
    mult = 100
    
    for jj in range(len(frame)-1):
        
        D21 = framesp[frameNum,jj,:].dot(x1)
        D22 = framesp[frameNum,jj,:].dot(x2)
        D23 = framesp[frameNum,jj,:].dot(x3)
        
        D21p = framesp[frameNum+1,jj,:].dot(x1)
        D22p = framesp[frameNum+1,jj,:].dot(x2)
        D23p = framesp[frameNum+1,jj,:].dot(x3)
        
        if D3:
            ax.quiver(framesp[frameNum,jj,0], framesp[frameNum,jj,1], framesp[frameNum,jj,2], \
               (framesp[frameNum+1,jj,0] - framesp[frameNum,jj,0])*mult, \
               (framesp[frameNum+1,jj,1] - framesp[frameNum,jj,1])*mult, \
               (framesp[frameNum+1,jj,2] - framesp[frameNum,jj,2])*mult, color = 'k')
        else:
            ax.quiver(D21, D22, (D21p - D21), (D22p - D22), scale = 0.2, \
                      color = 'k', zorder = 10000000, width = 0.01)
    
    #########################################
    #Stuff to get rid of the axes and make them square and stuff like that
    
    if D3:
            
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        
        ax.xaxis.pane.set_edgecolor('w')
        ax.yaxis.pane.set_edgecolor('w')
        ax.zaxis.pane.set_edgecolor('w')
        ax.w_xaxis.line.set_color("w")
        ax.w_yaxis.line.set_color("w")
        ax.w_zaxis.line.set_color("w")
        
        frame1 = plt.gca()
        frame1.axes.xaxis.set_ticklabels([])
        frame1.axes.yaxis.set_ticklabels([])
        frame1.axes.zaxis.set_ticklabels([])
        
        for line in ax.xaxis.get_ticklines():
            line.set_visible(False)
        for line in ax.yaxis.get_ticklines():
            line.set_visible(False)
        for line in ax.zaxis.get_ticklines():
            line.set_visible(False)
            
    else:
        
        ax.spines['bottom'].set_color('w')
        ax.spines['top'].set_color('w') 
        ax.spines['right'].set_color('w')
        ax.spines['left'].set_color('w')
        
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim([-6,6])
        ax.set_ylim([-2,4])
        
            
    ax.title.set_text(str(int(wavenumber)) + ' cm$^{-1}$')
    
    ax.grid(False)
    
    
    ax.axis('equal')
    
    if not D3:
        plt.tight_layout()


    if bool(savename):
        plt.savefig(savename, dpi=150)
        
    if legend:
        plt.figure(figsize = (1.5,1.5))
        ax = plt.subplot(111)
        plt.scatter(-5,3, s = FeS*sizescale, color = FeC, )
        ax.text(-1,3, 'Iron', verticalalignment='center')
        plt.scatter(-5,2, s = CS*sizescale, color = CC)
        ax.text(-1,2, 'Carbon', verticalalignment='center')
        plt.scatter(-5,1, s = NS*sizescale, color = NC)
        ax.text(-1,1, 'Nitrogen', verticalalignment='center')
        plt.scatter(-5,0, s = RuS*sizescale, color = RuC)
        ax.text(-1,0, 'Ruthenium', verticalalignment='center')
        plt.scatter(-5,-1, s = HS*sizescale, color = HC)
        ax.text(-1,-1, 'Hydrogen', verticalalignment='center')
        ax.set_xlim([-6,6])
        ax.set_ylim([-2,4])
        
        ax.spines['bottom'].set_color('w')
        ax.spines['top'].set_color('w') 
        ax.spines['right'].set_color('w')
        ax.spines['left'].set_color('w')
        
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim([-6,6])
        ax.set_ylim([-2,4])
        
        ax.grid(False)
        
        if bool(savename):
            plt.savefig('HAlegend.png', dpi=150)
    

        

        














