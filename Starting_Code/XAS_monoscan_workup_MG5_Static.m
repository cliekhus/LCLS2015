%%%%% FeRu RIXS MG5 Static Spectra
clear;
hold off;
clf;
clc;
%%%%%% inputs %%%%%%
Info = 'FeRu_RIXS_MG5_staticspectra';
Runs = [375:379,381:382,384,386];
ScanStacker = ones(size(Runs)); %used to distinguish disimilar runs
ipmmin = 0.1;
DiodeUmin = 0.0025;
DiodeUmax = 3.5;
CutOff = 1; %correlation filter variable
TTfiltmin = 100; %
TTfiltmax = 800;
tmin = -.6e-12;
tmax = -.1e-12;
tstep = 2e-14;
Mmin1 = 7.108;
Mmax1 = 7.1155;
Mstep1 = 0.0003;
Mmin2 = 7.1160;
Mmax2 = 7.1205; %make sure to add an extra bin
Mstep2 = 0.0005;

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
scanunique = [Mmin1:Mstep1:Mmax1, Mmin2:Mstep2:Mmax2]; %custom range didn't work very well in ScanVar
%scanunique = uniquetol(ScanVar,1e-5); %get each unique stage position used
stackunique = unique(Stacker);

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


%% Time and energy Sorting
FiltOff = xOn&not(lOn)&CorrFilter&IntensityFilter;
FiltOn = xOn&lOn&CorrFilter&IntensityFilter;

TTFilter = tt_ampl>median(tt_ampl(IntensityFilter&CorrFilter))-std(tt_ampl(IntensityFilter&CorrFilter))&tt_fwhm>median(tt_fwhm(IntensityFilter&CorrFilter))-std(tt_fwhm(IntensityFilter&CorrFilter))&tt_fwhm<median(tt_fwhm(IntensityFilter&CorrFilter))+std(tt_fwhm(IntensityFilter&CorrFilter))&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax; % Timing tool filters

for jj = 1:length(scanunique)-1;
    Dlta = (scanunique(jj+1)-scanunique(jj))/2;
    EShots(:,jj) = ScanVar>=scanunique(jj)-Dlta&ScanVar<scanunique(jj)+Dlta;
    DiodeUStatic(jj) = double(nanmean(DiodeU(EShots(:,jj)&FiltOn&TTFilter)));
    RowlandStatic(jj) = double(nanmean(Rowlandsum(EShots(:,jj)&FiltOn&TTFilter)));
        for kk = 1:vHPix;
            vonHamosStatic(kk,jj) = double(nanmean(vonHamosX(kk,EShots(:,jj)&FiltOn&TTFilter)));
end
end
    

%% Plotting

Pixels = (1:vHPix).';
pScan = scanunique(1:end-1); %last bin is always empty thanks for for loop

figure(2)
subplot(2,1,1)
plot(pScan,RowlandStatic);
xlabel('Mono Energy (keV)')
ylabel('Rowland Signal')
title('k\alpha RIXS CEE projection')
axis tight

subplot(2,1,2)
contourf(pScan,Pixels',vonHamosStatic);
xlabel('Mono Energy (keV)');
ylabel('Pixels');
title('k\beta RIXS plane');

figure(3)
plot(pScan,DiodeUStatic);
xlabel('Mono Energy (keV)')
ylabel('Diode Signal')
title('XAS spectrum')

%% Save Data Matrices

save(strcat('AveragedData_',Info),'DiodeUStatic','RowlandStatic','vonHamosStatic','scanunique');        




