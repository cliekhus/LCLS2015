%%Energy Info
EnergyScanName = 'ldat_xppj6715_Run371.h5';

XrayOnEnergy = logical(h5read(EnergyScanName, '/lightStatus/xray')); %x-ray on or off
LaserOnEnergy = logical(h5read(EnergyScanName, '/lightStatus/laser')); %laser on or off
DiodeUSumEnergy = h5read(EnergyScanName, '/diodeU/sum'); %Total Fluorescence Yield Diode
ScanVarEnergy = h5read(EnergyScanName, '/scan/var0'); %scanning stage position (ps)
TTCorrEnergy = h5read(EnergyScanName, '/ttCorr/tt'); %timing tool

ScanUniqueEnergy = unique(ScanVarEnergy);
XASOnEnergy = zeros(size(ScanUniqueEnergy));
XASOffEnergy = zeros(size(ScanUniqueEnergy));

for ii = 1:length(ScanUniqueEnergy)
    XASOnEnergy(ii) = sum(DiodeUSumEnergy((ScanUniqueEnergy(ii) == ScanVarEnergy)&XrayOnEnergy&LaserOnEnergy));
    XASOffEnergy(ii) = sum(DiodeUSumEnergy((ScanUniqueEnergy(ii) == ScanVarEnergy)&XrayOnEnergy&~LaserOnEnergy));
end

figure();
plot(ScanUniqueEnergy, XASOnEnergy/sum(XASOnEnergy), ScanUniqueEnergy, XASOffEnergy/sum(XASOffEnergy))
xlabel('x-ray energy (keV)')
ylabel('summed diode intensity')
title('1 ps delay?')
legend('laser on', 'laser off')

figure();
plot(ScanUniqueEnergy, XASOnEnergy/sum(XASOnEnergy)-XASOffEnergy/sum(XASOffEnergy))
xlabel('x-ray energy (keV)')
ylabel('difference diode intensity (on-off)')
title('1 ps delay?')


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
















