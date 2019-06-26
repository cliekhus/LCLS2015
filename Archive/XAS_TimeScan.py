# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:34:15 2019

@author: chelsea
"""

    Diode = Diode + list(ScanName['/diodeU/channels'])
    Diode0 = Diode0 + [x[0] for x in Diode]
    Diode1 = Diode1 + [x[1] for x in Diode]
    Diode2 = Diode2 + [x[2] for x in Diode]
    Diode3 = Diode3 + [x[3] for x in Diode]
    
    


"""
%% Timing Info
TimeScanName = 'ldat_xppj6715_Run396.h5';

XrayOnTime = logical(h5read(TimeScanName, '/lightStatus/xray')); %x-ray on or off
LaserOnTime = logical(h5read(TimeScanName, '/lightStatus/laser')); %laser on or off
DiodeUSumTime = h5read(TimeScanName, '/diodeU/sum'); %Total Fluorescence Yield Diode
ScanVarTime = h5read(TimeScanName, '/scan/var0'); %scanning stage position (ps)
TTCorrTime = h5read(TimeScanName, '/ttCorr/tt'); %timing tool

ScanUniqueTime = unique(ScanVarTime);
XASOnTime = zeros(size(ScanUniqueTime));
XASOffTime = zeros(size(ScanUniqueTime));

for ii = 1:length(ScanUniqueTime)
    XASOnTime(ii) = sum(DiodeUSumTime((ScanUniqueTime(ii) == ScanVarTime)&XrayOnTime&LaserOnTime));
    XASOffTime(ii) = sum(DiodeUSumTime((ScanUniqueTime(ii) == ScanVarTime)&XrayOnTime&~LaserOnTime));
end

figure();
plot(ScanUniqueTime, XASOnTime/sum(XASOnTime), ScanUniqueTime, XASOffTime/sum(XASOffTime))
xlabel('delay time (ps)')
ylabel('norm counts - time scan')
legend('laser on', 'laser off')

figure();
plot(ScanUniqueTime, XASOnTime/sum(XASOnTime)-XASOffTime/sum(XASOffTime))
xlabel('delay time (ps)')
ylabel('difference norm counts - time scan (on-off)')

figure();
hist(TTCorrTime(XrayOnTime&LaserOnTime), 1000)
xlabel('timing jitter (ps?)')
ylabel('counts - time scan')

figure();
hist(TTCorrEnergy(XrayOnEnergy&LaserOnEnergy), 1000)
xlabel('timing jitter (ps?)')
ylabel('counts - energy scan')
"""