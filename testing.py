# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:41:55 2019

@author: chelsea
"""





from itertools import compress









#signalOn = sum(list(compress(RowlandWOffsetm,[x and y < -50 for x,y in zip(FiltermOn, TTDelaymp)])))
signalOn = sum(list(compress(RowlandWOffsetm,[x and w and y < -50 for w,x,y in zip(LOnm, XOnm, TTDelaymp)])))

diodeOn = sum(list(compress(DiodeWOffsetm,[x and w and y < -50 for w,x,y in zip(LOnm, XOnm, TTDelaymp)])))

OnNum = sum([int(x and w and y < -50) for w,x,y in zip(LOnm, XOnm, TTDelaymp)])


signalOff = sum(list(compress(RowlandWOffsetm,[not x and y for x,y in zip(LOnm,XOnm)])))

diodeOff = sum(list(compress(DiodeWOffsetm,[not x and y for x,y in zip(LOnm,XOnm)])))

OffNum = sum([int(not x and y) for x,y in zip(LOnm,XOnm)])