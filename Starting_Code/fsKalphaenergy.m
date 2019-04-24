clear;
hold off;
clf;
clc;
close all;
%%
Run=087;
str1='190';
f = strcat('ldat_xppj6715_Run',str1,'.h5');
Stacker = ones(size((h5read(f,'/lightStatus/xray')))); %Label runs that shouldn't get averaged together
xOn = (h5read(f,'/lightStatus/xray'));  %x-ray on or off
lOn = (h5read(f,'/lightStatus/laser'));  %laser on or off
ipm2_all = (h5read(f,'/ipm2/channels')); %shot to shot correction value
DiodeU_all=(h5read(f,'/diodeU/channels')); %Total Fluorescence Yield Diode
RowlandY = (h5read(f,'/Rowland/ROI_proj_ythres'));  %Rowland proj data
%vonHamosX = (h5read(f,'/vonHamos/ROI_proj_xthres')); %Von Hamos energy proj
tt = (h5read(f,'/ttCorr/tt')); % jitter time correction value (ps)
tt_ampl =  (h5read(f,'/tt/XPP_TIMETOOL_AMPL')); % TimingTool Fit Amplitude
tt_fwhm =  (h5read(f,'/tt/XPP_TIMETOOL_FLTPOSFWHM')); % TimingTool Fit FWHM
tt_fltpos =  (h5read(f,'/tt/XPP_TIMETOOL_FLTPOS')); % TimingTool Fit Position
ScanVar = (h5read(f,'/scan/var0')); %scanning stage position (ps)
%%
RowlandY = bsxfun(@minus,RowlandY,median(RowlandY)); %remove baseline
Rowlandsum1 = sum(RowlandY).';% get one number for Rowland detector
%Rowlandsum=sum(RowlandY).';
%%
figure
subplot(2,2,1)
histogram(ipm2_all(1,:))
title('ipm2_1')
subplot(2,2,2)
histogram(ipm2_all(2,:))
title('ipm2_2')
subplot(2,2,3)
histogram(ipm2_all(3,:))
title('ipm2_3')
subplot(2,2,4)
histogram(ipm2_all(4,:))
title('ipm2_4')
%%
figure
subplot(2,2,1)
histogram(DiodeU_all(1,:))
title('DiodeU_1')
subplot(2,2,2)
histogram(DiodeU_all(2,:))
title('DiodeU_2')
subplot(2,2,3)
histogram(DiodeU_all(3,:))
title('DiodeU_3')
subplot(2,2,4)
histogram(DiodeU_all(4,:))
title('DiodeU_4')
%%
DiodeU = DiodeU_all(3,:).';  %Take useful channel
%%
ipm2 = sum(ipm2_all([2,4],:),1).'; %sum useful channels
%%
scanunique = unique(ScanVar); %get each unique stage position used
stackunique = unique(Stacker);
%IsData = xOn&lOn;

%% Setup polynomial filter for laser off shots

CorrFilter_off = zeros(size(ipm2));
IntensityFilter_off = zeros(size(ipm2));
lOff=abs(lOn-1);
filt1=lOff&xOn;
%ipm2_f=ipm2(filt1);
%DiodeU_f=DiodeU(filt1);
ipmminf2 = nanmean(ipm2)-2*nanstd(ipm2);
ipmmaxf2 = nanmean(ipm2)+2*nanstd(ipm2);
DiodeUminf2 = nanmean(DiodeU)-2*nanstd(DiodeU);
DiodeUmaxf2 = nanmean(DiodeU)+2*nanstd(DiodeU);
CutOff = 0.035; %correlation filter variable

zz = 1;  %If scans shouldn't be averaged together they will have different correlation filters as well
    IntensityFilter_ipm = ipm2>ipmminf2&ipm2<ipmmaxf2; 
    IntensityFilter_diode = DiodeU>DiodeUminf2&DiodeU<DiodeUmaxf2;
    totIntensityFilter=IntensityFilter_ipm&IntensityFilter_diode;
    IntCorr = (DiodeU./ipm2);
    IntCorrfilter = IntCorr>(nanmean(IntCorr)-2*nanstd(IntCorr))&IntCorr<(nanmean(IntCorr)+2*nanstd(IntCorr)); %rough filter to remove extreme points
    %IntCorrfilterf = IntCorrfilter;%&IntensityFilter; %rough filter to remove extreme points
    figure
    plot(ipm2(IntCorrfilter&totIntensityFilter&filt1),DiodeU(IntCorrfilter&totIntensityFilter&filt1),'r.');
    xlabel ('IPM2');
    ylabel ('UserDiode');
    b1 = polyfit(ipm2(IntCorrfilter&totIntensityFilter&filt1),DiodeU(IntCorrfilter&totIntensityFilter&filt1),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    hold on
    refline(b1(1),b1(2)+(b1(2).*0.045));  %add reference lines for the final correlation filter
    refline(b1(1),b1(2));
    refline(b1(1),b1(2)-(b1(2).*0.045));
    
    y2 = polyval([b1(1) (b1(2)+(b1(2).*0.045))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b1(1) (b1(2)-(b1(2).*0.045))],ipm2);
    CorrFilter_off = DiodeU<y1&DiodeU>y2;
    figure
    plot(ipm2(CorrFilter_off&totIntensityFilter&filt1),DiodeU(CorrFilter_off&totIntensityFilter&filt1),'r.')
    figure
    hist(DiodeU(CorrFilter_off&totIntensityFilter&filt1)./ipm2(CorrFilter_off&totIntensityFilter&filt1))
    numshotslOffXon=size(DiodeU(CorrFilter_off&totIntensityFilter&filt1))
    %% Make Filter for laser off pulses
    Filtoff=CorrFilter_off&totIntensityFilter&filt1; 
   
     %% Setup polynomial filter for laser on shots

CorrFilter = zeros(size(ipm2));
%IntensityFilter = zeros(size(ipm2));
%lOff=abs(lOn-1);
filt2=lOn&xOn;
%ipm2_f2=ipm2(filt2);
%DiodeU_f2=DiodeU(filt2);
ipmmin = nanmean(ipm2)-2*nanstd(ipm2);
ipmmax = nanmean(ipm2)+2*nanstd(ipm2);
DiodeUmin = mean(DiodeU)-2*std(DiodeU);
DiodeUmax = mean(DiodeU)+2*std(DiodeU);
%CutOff = 0.035; %correlation filter variable

zz = 1;  %If scans shouldn't be averaged together they will have different correlation filters as well
    IntensityFilter_ipm = ipm2>ipmmin&ipm2<ipmmax; 
    IntensityFilter_diode = DiodeU>DiodeUmin&DiodeU<DiodeUmax;
    totInton=IntensityFilter_ipm&IntensityFilter_diode;
    IntCorr = (DiodeU./ipm2);
    IntCorrfilter = IntCorr>(nanmean(IntCorr)-2*nanstd(IntCorr))&IntCorr<(nanmean(IntCorr)+2*nanstd(IntCorr)); %rough filter to remove extreme points
    %IntCorrfilterf = IntCorrfilter;%&IntensityFilter; %rough filter to remove extreme points
    figure
    plot(ipm2(IntCorrfilter&filt2&totInton),DiodeU(IntCorrfilter&filt2&totInton),'r.');
    xlabel ('IPM2_laser on');
    ylabel ('UserDiode_laser on');
    b = polyfit(ipm2(IntCorrfilter&filt2&totInton),DiodeU(IntCorrfilter&filt2&totInton),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    hold on
    refline(b(1),b(2)+(b(2).*0.05));  %add reference lines for the final correlation filter
    refline(b(1),b(2));
    refline(b(1),b(2)-(b(2).*0.05));
    
    y2 = polyval([b(1) (b(2)+(b(2).*0.05))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b(1) (b(2)-(b(2).*0.05))],ipm2);
    CorrFilter = DiodeU<y1&DiodeU>y2;
    figure
    plot(ipm2(CorrFilter&filt2&totInton),DiodeU(CorrFilter&filt2&totInton),'r.')
    figure
    hist(DiodeU(CorrFilter&filt2&totInton)./ipm2(CorrFilter&filt2&totInton))
    numshotslOnXon=size(DiodeU(CorrFilter&filt2&totInton))
    %% Make Filter for laser on pulses
    Filton=CorrFilter&filt2&totInton;
%% See if Correlation Filter works with Rowland Sum
%Rowlandsum1_f2=Rowlandsum1(filt2);
Rowlandsum1_on=Rowlandsum1(CorrFilter&filt2&totInton);
figure
hist(Rowlandsum1_on)
figure
plot(Rowlandsum1(CorrFilter&filt2&totInton), DiodeU(CorrFilter&filt2&totInton),'g.')
%% Time Sorting

TTfiltmin = 200; %
TTfiltmax = 800;
tmin = -1.75e-12;
tmax = -1.20e-12;
tstep = 5e-14;

ttfwhm_min = mean(tt_fwhm)-2*std(tt_fwhm);
figure
subplot(2,2,1)
histogram(tt(Filton))
title('tt')
subplot(2,2,2)
histogram(tt_ampl(Filton))
title('tt_ampl')
subplot(2,2,3)
histogram(tt_fltpos(Filton))
title('tt_fltpos')
subplot(2,2,4)
histogram(tt_fwhm(Filton))
title('tt_fwhm')
    
%% Calculate Real Times    
RealTimes = -1.4e-12+tt*1e-12; %actual time delay including jitter
figure
hist(RealTimes)  
    
    
    %% Calculate RowlandOff shots
    Rowlandsum1_off=Rowlandsum1(Filtoff);
    DiodeU_off=DiodeU(Filtoff);
    figure
    hist(Rowlandsum1_off)
figure
plot(Rowlandsum1(Filtoff), DiodeU(Filtoff),'g.',Rowlandsum1(Filtoff), ipm2(Filtoff),'r.' )

%%
%%TTFilter = tt_ampl>0.15&tt_fwhm>110&tt_fwhm<140&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax;
TTFilter = tt_ampl>(nanmedian(tt_ampl(Filton))-2.*nanstd(tt_ampl(Filton)))&tt_fwhm>(nanmedian(tt_fwhm(Filton))-2.*nanstd(tt_fwhm(Filton)))&tt_fwhm<(nanmedian(tt_fwhm(Filton))+2.*std(tt_fwhm(Filton)))&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax; % Timing tool filters
%%
Times = [tmin:tstep:tmax];
Binedges = [60000:1000:70000];
RowlandOn_norm=[];
Ncounton=[];
for ii = 1:length(Times)-1;
    Shots = RealTimes>=Times(ii)&RealTimes<=Times(ii+1)&TTFilter&Filton;
    for jj=1:length(scanunique)
    EShots = ScanVar == scanunique(jj);
    %RowlandTT_off(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)));
    Ncountoff(jj) = sum(EShots&Filtoff);
    RowlandOff_norm(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)));
    %RowlandOff_stdnorm(jj) = double(nanstd((Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)),1));   
    RowlandOn_norm(ii,jj) = double(nanmean(Rowlandsum1(EShots&Filton&Shots)./DiodeU(EShots&Filton&Shots)));    
    Ncounton(ii,jj) = sum(EShots&Filton&Shots);
    end
end


% 
% 
% for jj = 1:length(scanunique);
%     EShots = ScanVar == scanunique(jj);
%     RowlandTT_off(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)));
%     Ncount(jj) = sum(EShots&Filtoff);
%     RowlandOff_norm(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)));
%     RowlandOff_stdnorm(jj) = double(nanstd((Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)),1));
% end

figure
plot(scanunique,RowlandOff_norm)
% figure
% errorbar(scanunique, RowlandOff_norm,RowlandOff_stdnorm./sqrt(Ncount))
figure
contourf(scanunique,Times(1:end-1),RowlandOn_norm,20)

%% Create Difference Data

delta_T_e=[];

for ii= 1:length(Times)-1;
    delta_T_e(ii,:)=(RowlandOn_norm(ii,:)-RowlandOff_norm);
end

figure
contourf(scanunique,Times(1:end-1),delta_T_e,10)

figure
plot(scanunique, sum(delta_T_e(4:6,:),1),'-o',scanunique, smooth(sum(delta_T_e(4:6,:),1)),scanunique, medfilt1(sum(delta_T_e(4:6,:),1),4),scanunique, sgolayfilt(sum(delta_T_e(4:6,:),1),2,5) )

figure
plot(scanunique, smooth(sum(delta_T_e(4:6,:),1))./smooth(RowlandOff_norm))
%% Calibrating axis

load('bb.mat');


%en=-0.0311.*scanunique+8.7538;

figure
plot(polyval(bb, scanunique), smooth(sum(delta_T_e(4:6,:),1))./smooth(RowlandOff_norm))
%%
figure
subplot(1,2,1)
plot(polyval(bb, scanunique), sgolayfilt((sum(delta_T_e(4:6,:),1))./(RowlandOff_norm), 3, 5),polyval(bb, scanunique),(sum(delta_T_e(4:6,:),1))./sgolayfilt(RowlandOff_norm, 3,5))
title('deltaT%')
subplot(1,2,2)
plot(polyval(bb, scanunique), sgolayfilt((sum(delta_T_e(4:6,:),1)), 3, 5),polyval(bb, scanunique),(sum(delta_T_e(4:6,:),1)))
title('deltaT_counts')
%%


figure
plot(polyval(bb, scanunique), (RowlandOff_norm))

%% save files

%f1=strcat('delta_T_',str1,'_norm','.mat');
%f2=strcat('delta_T_',str1, '.mat');
rtheta = scanunique;
g1=RowlandOff_norm;
save(strcat('K_alpha_off',str1,'_norm','.mat'), 'g1')
save(strcat('rtheta',str1,'.mat'), 'rtheta')
save(strcat('NCount',str1,'.mat'), 'Ncount')
%% %end
close all