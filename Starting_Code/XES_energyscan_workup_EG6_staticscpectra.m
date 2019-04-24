%%%%% FeRu XES EG56 Static Spectra
clear;
hold off;
clf;
clc;
%%%%%% inputs %%%%%%
Info = 'FeRu_XES_EG6_staticspectra_190';
Runs = [190];
ScanStacker = ones(size(Runs)); %used to distinguish disimilar runs
ipmmin = 0.1;
DiodeUmin = 0.06;
DiodeUmax = 3.5;
CutOff = 0.05; %correlation filter variable
TTfiltmin = 100; %
TTfiltmax = 800;
tmin = -.4e-12;
tmax = .2e-12;
tstep = 2e-14;

Stacker = [];
xOn = [];
lOn = [];
ipm2_all = [];
tt = [];
tt_ampl = [];
tt_fwhm = [];
tt_fltpos = [];
RowlandY = [];
vonHamosX = [];
DiodeU_all = [];
ScanVar = [];

for zz = 1:length(Runs);
f = strcat('ldat_xppj6715_Run', num2str(Runs(zz)),'.h5');
Stacker = [Stacker; ones(size((h5read(f,'/lightStatus/xray')))).*ScanStacker(zz)]; %Label runs that shouldn't get averaged together
xOn = [xOn; (h5read(f,'/lightStatus/xray'))];  %x-ray on or off
lOn = [lOn; (h5read(f,'/lightStatus/laser'))];  %laser on or off
ipm2_all = [ipm2_all (h5read(f,'/ipm2/channels'))]; %shot to shot correction value
DiodeU_all=[DiodeU_all (h5read(f,'/diodeU/channels'))]; %Total Fluorescence Yield Diode
RowlandY = [RowlandY (h5read(f,'/Rowland/ROI_proj_ythres'))];  %Rowland proj data
vonHamosX = [vonHamosX (h5read(f,'/vonHamos/ROI_proj_xthres'))]; %Von Hamos energy proj
tt = [tt; (h5read(f,'/ttCorr/tt'))]; % jitter time correction value (ps)
tt_ampl = [tt_ampl; h5read(f,'/tt/XPP_TIMETOOL_AMPL')]; % TimingTool Fit Amplitude
tt_fwhm = [tt_fwhm; h5read(f,'/tt/XPP_TIMETOOL_FLTPOSFWHM')]; % TimingTool Fit FWHM
tt_fltpos = [tt_fltpos; h5read(f,'/tt/XPP_TIMETOOL_FLTPOS')]; % TimingTool Fit Position
ScanVar = [ScanVar; (h5read(f,'/scan/var0'))]; %scanning stage position (ps)
end

[vHPix,TotShots] = size(vonHamosX);


RowlandY = bsxfun(@minus,RowlandY,median(RowlandY)); %remove baseline
Rowlandsum = sum(RowlandY).'; %sum pixels up to get shot by shot integration

ipm2 = sum(ipm2_all([2 4],:),1).'; %sum useful channels
DiodeU = DiodeU_all(3,:).';  %Take useful channel
scanunique190 = sort(unique(ScanVar)); %get each unique stage position used
stackunique = unique(Stacker);
IsData = xOn&lOn;

%% Setup Kaspers polynomial correlation filter

CorrFilter = zeros(size(ipm2));
IntensityFilter = zeros(size(ipm2));

for zz = 1:length(stackunique);  %If scans shouldn't be averaged together they will have different correlation filters as well
    IntensityFilter = xOn&ipm2>ipmmin&DiodeU>DiodeUmin&DiodeU<DiodeUmax&Stacker==zz;  
    IntCorr = (ipm2./DiodeU);
    IntCorrfilter = (Stacker==zz&IntCorr>nanmedian(IntCorr)-nanstd(IntCorr)&IntCorr<nanmedian(IntCorr)+nanstd(IntCorr))&IntensityFilter; %rough filter to remove extreme points
   
    figure(1)
    plot(DiodeU(Stacker == zz), ipm2(Stacker == zz),'k.');
    xlabel ('User Diode');
    ylabel ('IPM 2');
    b = polyfit(DiodeU(IntCorrfilter)',ipm2(IntCorrfilter)',1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    hold on
    refline(b(1),b(2)+CutOff);  %add reference lines for the final correlation filter
    refline(b(1),b(2));
    refline(b(1),b(2)-CutOff);
    
    y2 = polyval([b(1) b(2)+CutOff],DiodeU); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b(1) b(2)-CutOff],DiodeU);
    CorrFilter = ipm2>y1&ipm2<y2;
    plot(DiodeU(IntensityFilter&CorrFilter),ipm2(IntensityFilter&CorrFilter),'r.')
end

%%  Average static spectra Data
FiltOff = xOn&not(lOn)&CorrFilter&IntensityFilter;

for ii = 1:length(scanunique190);
    RowlandStatic190(ii) = mean(Rowlandsum(FiltOff&ScanVar==scanunique190(ii)));
end

vonHamosStatic190 = mean(vonHamosX(:,FiltOff),2);


%% Plotting
Pixels = (1:vHPix).';

figure(2)
subplot(2,1,1)
plot(scanunique190,RowlandStatic190)
xlabel('rTheta (degrees)')
ylabel('Signal arb.')
title('k\alpha Energy scan')

subplot(2,1,2)
plot(Pixels,vonHamosStatic190)
xlabel('pixels')
ylabel('Signal arb.')
title('k\beta Energy scan')

%% Save Data Matrices

save(strcat('AveragedData_',Info),'RowlandStatic190','vonHamosStatic190','scanunique190');        




