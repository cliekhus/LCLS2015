clear;
hold off;
clf;
clc;
close all;
%%
Run=190;
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
       
    %% Calculate RowlandOff shots
    Rowlandsum1_off=Rowlandsum1(Filtoff);
    DiodeU_off=DiodeU(Filtoff);
    figure
    hist(Rowlandsum1_off)
figure
plot(Rowlandsum1(Filtoff), DiodeU(Filtoff),'g.',Rowlandsum1(Filtoff), ipm2(Filtoff),'r.' )
title('Rowland')

%%

for jj = 1:length(scanunique);
    EShots = ScanVar == scanunique(jj);
    RowlandTT_off(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)));
    Ncount(jj) = sum(EShots&Filtoff);
    RowlandOff_norm(jj) = double(nanmean(Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)));
    RowlandOff_stdnorm(jj) = double(nanstd((Rowlandsum1(EShots&Filtoff)./DiodeU(EShots&Filtoff)),1));
end

figure
plotyy(scanunique,RowlandTT_off , scanunique,RowlandOff_norm)
figure
errorbar(scanunique, RowlandOff_norm,RowlandOff_stdnorm./sqrt(Ncount))
%% save files

%f1=strcat('delta_T_',str1,'_norm','.mat');
%f2=strcat('delta_T_',str1, '.mat');
rtheta = scanunique;
g1=RowlandOff_norm;
save(strcat('K_alpha_off',str1,'_norm','.mat'), 'g1')
save(strcat('rtheta',str1,'.mat'), 'rtheta')
save(strcat('NCount',str1,'.mat'), 'Ncount')
%% %end
%close all