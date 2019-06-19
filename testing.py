# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:41:55 2019

@author: chelsea
"""





from itertools import compress









signalOn = sum(list(compress(RowlandWOffsetp,[x and y < -50 for x,y in zip(FilterpOn, TTDelaypp)])))

diodeOn = sum(list(compress(DiodeWOffsetp,[x and y < -50 for x,y in zip(FilterpOn, TTDelaypp)])))

OnNum = sum([int(x and y < -50) for x,y in zip(FilterpOn, TTDelaypp)])


signalOff = sum(list(compress(RowlandWOffsetp,FilterpOff)))

diodeOff = sum(list(compress(DiodeWOffsetp,FilterpOff)))

OffNum = sum([int(x) for x in FilterpOff])