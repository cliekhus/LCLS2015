# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 21:20:41 2020

@author: chels
"""
import subprocess

def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)

subprocess_cmd('vmd& play C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/UVTD.tcl')