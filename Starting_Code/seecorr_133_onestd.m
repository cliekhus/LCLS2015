clear;
hold off;
clf;
clc;
close all;
%%
%Stacker = [];
%xOn = [];
%lOn = [];
%ipm2_all = [];
%tt = [];
%tt_ampl = [];
%tt_fwhm = [];
%tt_fltpos = [];
%RowlandY = [];
%vonHamosX = [];
%DiodeU_all = [];
%ScanVar = [];
%%
Run=133;
str1=num2str(Run);
f = strcat('ldat_xppj6715_Run',str1,'.h5');
Stacker = ones(size((h5read(f,'/lightStatus/xray')))); %Label runs that shouldn't get averaged together
xOn = (h5read(f,'/lightStatus/xray'));  %x-ray on or off
lOn = (h5read(f,'/lightStatus/laser'));  %laser on or off
ipm2_all = (h5read(f,'/ipm2/channels')); %shot to shot correction value
DiodeU_all=(h5read(f,'/diodeU/channels')); %Total Fluorescence Yield Diode
RowlandY = (h5read(f,'/Rowland/ROI_proj_ythres'));  %Rowland proj data
vonHamosX = (h5read(f,'/vonHamos/ROI_proj_xthres')); %Von Hamos energy proj
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
ipm2 = sum(ipm2_all([2 4],:),1).'; %sum useful channels
%%
scanunique = unique(ScanVar); %get each unique stage position used
stackunique = unique(Stacker);
IsData = xOn&lOn;

%% Setup polynomial filter for laser off shots

CorrFilter_off = zeros(size(ipm2));
IntensityFilter_off = zeros(size(ipm2));
lOff=abs(lOn-1);
filt1=lOff&xOn;
%ipm2_f=ipm2(filt1);
%DiodeU_f=DiodeU(filt1);
ipmminf2 = nanmedian(ipm2)-nanstd(ipm2);
ipmmaxf2 = nanmedian(ipm2)+nanstd(ipm2);
DiodeUminf2 = nanmedian(DiodeU)-nanstd(DiodeU);
DiodeUmaxf2 = nanmedian(DiodeU)+nanstd(DiodeU);
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
    refline(b1(1),b1(2)+(b1(2).*0.04));  %add reference lines for the final correlation filter
    refline(b1(1),b1(2));
    refline(b1(1),b1(2)-(b1(2).*0.04));
    
    y2 = polyval([b1(1) (b1(2)+(b1(2).*0.04))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b1(1) (b1(2)-(b1(2).*0.04))],ipm2);
    CorrFilter_off = DiodeU<y1&DiodeU>y2;
    figure
    plot(ipm2(CorrFilter_off&totIntensityFilter&filt1),DiodeU(CorrFilter_off&totIntensityFilter&filt1),'r.')
    figure
    hist(DiodeU(CorrFilter_off&totIntensityFilter&filt1)./ipm2(CorrFilter_off&totIntensityFilter&filt1))
    numshotslOffXon=size(DiodeU(CorrFilter_off&totIntensityFilter&filt1))
    %% Make Filter for laser off pulses
    Filtoff=CorrFilter_off&totIntensityFilter&filt1; 
       
    %% See if Correlation Works for RowlandOff shots
    %Rowlandsum1_off=Rowlandsum1(Filtoff);
    %DiodeU_off=DiodeU(Filtoff);
    %figure
    %hist(Rowlandsum1_off)
    figure
plot(Rowlandsum1(Filtoff), DiodeU(Filtoff),'g.')
%% Set up second filter for laser off shots
 figure
    plot(Rowlandsum1(Filtoff), DiodeU(Filtoff),'g.');
    xlabel ('Rowlandsum1');
    ylabel ('UserDiode');
    b1r = polyfit(Rowlandsum1(Filtoff),DiodeU(Filtoff),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    hold on
    refline(b1r(1),b1r(2)+(b1r(2).*0.35));  %add reference lines for the final correlation filter
    refline(b1r(1),b1r(2));
    refline(b1r(1),b1r(2)-(b1r(2).*0.35));
    y2 = polyval([b1r(1) (b1r(2)+(b1r(2).*0.35))],Rowlandsum1); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b1r(1) (b1r(2)-(b1r(2).*0.35))],Rowlandsum1);
    CorrFilter_off1 = DiodeU>y1&DiodeU<y2;
    figure
    plot(Rowlandsum1(CorrFilter_off1&Filtoff),DiodeU(CorrFilter_off1&Filtoff),'r.')
    numshotslOffXon=size(DiodeU(CorrFilter_off1&Filtoff))
    Filtoff=CorrFilter_off1&Filtoff;

  %% Setup polynomial filter for laser oon shots

CorrFilter = zeros(size(ipm2));
%IntensityFilter = zeros(size(ipm2));
%lOff=abs(lOn-1);
filt2=lOn&xOn;
ipm2_f2=ipm2(filt2);
DiodeU_f2=DiodeU(filt2);
ipmmin = nanmedian(ipm2)-nanstd(ipm2);
ipmmax = nanmedian(ipm2)+nanstd(ipm2);
DiodeUmin = nanmedian(DiodeU)-nanstd(DiodeU);
DiodeUmax = nanmedian(DiodeU)+nanstd(DiodeU);
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
    refline(b(1),b(2)+(b(2).*0.045));  %add reference lines for the final correlation filter
    refline(b(1),b(2));
    refline(b(1),b(2)-(b(2).*0.045));
    
    y2 = polyval([b(1) (b(2)+(b(2).*0.045))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b(1) (b(2)-(b(2).*0.045))],ipm2);
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
%Rowlandsum1_on=Rowlandsum1(CorrFilter&filt2&totInton);
%figure
%hist(Rowlandsum1_on)
figure
plot(Rowlandsum1(CorrFilter&filt2&totInton), DiodeU(CorrFilter&filt2&totInton),'g.')
%% Set up second filter for laser on shots
 figure
    plot(Rowlandsum1(Filton), DiodeU(Filton),'g.');
    xlabel ('Rowlandsum1');
    ylabel ('UserDiode');
    br = polyfit(Rowlandsum1(Filton),DiodeU(Filton),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    hold on
    refline(br(1),br(2)+(br(2).*0.35));  %add reference lines for the final correlation filter
    refline(br(1),br(2));
    refline(br(1),br(2)-(br(2).*0.35));
    y2 = polyval([br(1) (br(2)+(br(2).*0.35))],Rowlandsum1); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([br(1) (br(2)-(br(2).*0.35))],Rowlandsum1);
    CorrFilter_1 = DiodeU>y1&DiodeU<y2;
    figure
    plot(Rowlandsum1(CorrFilter_1&Filton),DiodeU(CorrFilter_1&Filton),'r.')
    numshotslOnXon=size(DiodeU(CorrFilter_1&Filton))
    Filton=CorrFilter_1&Filton;
%% Time Sorting

TTfiltmin = 200; %
TTfiltmax = 800;
tmin = -2.1e-12;
tmax = -0.2e-12;
tstep = 2e-14;

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
%%


RealTimes = ScanVar+tt*1e-12; %actual time delay including jitter
figure
hist(RealTimes)
%%
%TTFilter = tt_ampl>0.15&tt_fwhm>110&tt_fwhm<140&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax;
TTFilter = tt_ampl>(nanmedian(tt_ampl(Filton))-2.*nanstd(tt_ampl(Filton)))&tt_fwhm>(nanmedian(tt_fwhm(Filton))-2.*nanstd(tt_fwhm(Filton)))&tt_fwhm<(nanmedian(tt_fwhm(Filton))+2.*std(tt_fwhm(Filton)))&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax; % Timing tool filters
%%
Times = [tmin:tstep:tmax];
Binedges = [60000:1000:70000];

for ii = 1:length(Times)-1;
    Shots = RealTimes>=Times(ii)&RealTimes<=Times(ii+1)&TTFilter&Filton;
       RowlandTT(ii) = double(nanmean(Rowlandsum1(Shots)));
        Ncount(ii) = sum(Shots);
        RowlandOn_norm(ii) = double(nanmean(Rowlandsum1(Shots)./DiodeU(Shots)));
        end
            %RowlandOn(ii) = double(nanmean(Rowlandsum1_on(Shots)./DiodeU(Shots)));
        %On_Rowland(ii) = double(nanmean(Rowlandsum(Shots)));
        %On_Diode(ii) = double(mean(DiodeU(Shots)));
        %OnErr_Rowland(ii) = double(std(Rowlandsum(Shots),'omitnan'));
        %OnErr_Diode(ii) = double(std(DiodeU(Shots),'omitnan'));
        %RowlandTT(ii) = RowlandOn(ii)-RowlandOff;
        %RowlandTT_nondiv(ii) = On_Rowland(ii) - Off_Rowland;
%         RowlandTT(ii) = double(nanmean(RowlandDiff(Shots)));
%         RowlandErr(ii) = double(std(RowlandDiff(Shots)));
       
        %RowlandRawhist(ii,:) = histcounts(Rowlandsum(Shots),Binedges);
%         for kk = 1:vHPix;
%         vonHamosTT(kk,ii) = double(nanmean(vonHamosDiff(kk,Shots)));
%         end
 
figure
plotyy(Times(1:end-1), RowlandTT,Times(1:end-1),  RowlandOn_norm )

%% Set up Difference Data

%Rowland_Off=double(nanmean(Rowlandsum1(Filtoff)));
%Diode_Off=double(nanmean(DiodeU(Filtoff)));
RowlandOff_norm=double(nanmean(Rowlandsum1(Filtoff)./DiodeU(Filtoff)))
RowlandOff_std=double(nanstd(Rowlandsum1(Filtoff)./DiodeU(Filtoff)))

figure
plotyy(Times(1:end-1), (RowlandOn_norm-RowlandOff_norm),Times(1:end-1),  (RowlandOn_norm-RowlandOff_norm)./RowlandOff_norm)

%% save files

%f1=strcat('delta_T_',str1,'_norm','.mat');
%f2=strcat('delta_T_',str1, '.mat');
pTimes = Times(1:end-1)*1e12;
save(strcat('delta_T_',str1,'_norm','.mat'), 'pTimes','RowlandOn_norm','RowlandOff_norm','Ncount')

%% %end 
%%




%%%%%% inputs %%%%%%
Info = 'FeRu_XES_TG12_smallbins';
Runs = [180:188];
ScanStacker = ones(size(Runs)); %used to distinguish disimilar runs
ipmminf2 = 0.1;
DiodeUminf2 = 0.13;
DiodeUmaxf2 = 3.5;
CutOff = 0.035; %correlation filter variable
TTfiltmin = 200; %
TTfiltmax = 800;
tmin = -2.1e-12;
tmax = -0.2e-12;
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
scanunique = unique(ScanVar); %get each unique stage position used
stackunique = unique(Stacker);
IsData = xOn&lOn;

%% Setup Kaspers polynomial correlation filter

CorrFilter = zeros(size(ipm2));
IntensityFilter = zeros(size(ipm2));

for zz = 1:length(stackunique);  %If scans shouldn't be averaged together they will have different correlation filters as well
    IntensityFilter = xOn&ipm2>ipmminf2&DiodeU>DiodeUminf2&DiodeU<DiodeUmaxf2&Stacker==zz;  
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

%%  Create Difference Data
Filt = IsData&CorrFilter&IntensityFilter;
FiltOff = xOn&not(lOn)&CorrFilter&IntensityFilter;

RowlandOff = double(nanmean(Rowlandsum(FiltOff)./DiodeU(FiltOff)));
Off_Rowland = double(nanmean(Rowlandsum(FiltOff)));
Off_Diode = double(mean(DiodeU(FiltOff)));


% RowlandDiff(Filt) = bsxfun(@minus,Rowlandsum(Filt)./DiodeU(Filt),mean(Rowlandsum(FiltOff)./DiodeU(FiltOff)));
% for kk = 1:vHPix;
% vonHamosDiff(kk,Filt) =  bsxfun(@minus,vonHamosX(kk,Filt)./DiodeU(Filt).',mean(vonHamosX(kk,FiltOff)./DiodeU(FiltOff).',2));
% end

%% Time Sorting

RealTimes = ScanVar+tt*1e-12; %actual time delay including jitter

TTFilter = tt_ampl>0.15&tt_fwhm>120&tt_fwhm<140&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax;
%TTFilter = tt_ampl>median(tt_ampl(IntensityFilter&CorrFilter))-std(tt_ampl(IntensityFilter&CorrFilter))&tt_fwhm>median(tt_fwhm(IntensityFilter&CorrFilter))-std(tt_fwhm(IntensityFilter&CorrFilter))&tt_fwhm<median(tt_fwhm(IntensityFilter&CorrFilter))+std(tt_fwhm(IntensityFilter&CorrFilter))&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax; % Timing tool filters

Times = [tmin:tstep:tmax];
Binedges = [60000:1000:70000];

for ii = 1:length(Times)-1;
    Shots = RealTimes>=Times(ii)&RealTimes<=Times(ii+1)&TTFilter&Filt;
    %if length(stackunique)>1
        for qq = 1:length(stackunique);
            RowlandTT(ii,qq) = double(nanmean(RowlandDiff(Shots&Stacker==stackunique(qq))));
            for kk = 1:vHPix;
            vonHamosTT(kk,ii,qq) = double(nanmean(vonHamosDiff(kk,Shots&Stacker==stackunique(qq))));
            end
        end
    else
        RowlandOn(ii) = double(nanmean(Rowlandsum(Shots)./DiodeU(Shots)));
        On_Rowland(ii) = double(nanmean(Rowlandsum(Shots)));
        On_Diode(ii) = double(mean(DiodeU(Shots)));
        OnErr_Rowland(ii) = double(std(Rowlandsum(Shots),'omitnan'));
        OnErr_Diode(ii) = double(std(DiodeU(Shots),'omitnan'));
        RowlandTT(ii) = RowlandOn(ii)-RowlandOff  
        RowlandTT_nondiv(ii) = On_Rowland(ii) - Off_Rowland;
%         RowlandTT(ii) = double(nanmean(RowlandDiff(Shots)));
%         RowlandErr(ii) = double(std(RowlandDiff(Shots)));
        Ncount(ii) = sum(Shots);
        %RowlandRawhist(ii,:) = histcounts(Rowlandsum(Shots),Binedges);
%         for kk = 1:vHPix;
%         vonHamosTT(kk,ii) = double(nanmean(vonHamosDiff(kk,Shots)));
%         end
    end
end

%%%% Error propogation    
OffErr_Rowland = double(std(Rowlandsum(FiltOff),'omitnan'));
OffErr_Diode = double(std(DiodeU(FiltOff),'omitnan'));
OffErr = double(sqrt((OffErr_Rowland/Off_Rowland)^2+(OffErr_Diode/Off_Diode)^2)*(Off_Rowland/Off_Diode));
OnErr = sqrt((OnErr_Rowland./On_Rowland).^2+(OnErr_Diode./On_Diode).^2).*(On_Rowland./On_Diode);
TotErr = sqrt(OnErr.^2+OffErr^2);

%% Plotting
pTimes = Times(1:end-1)*1e12; %The last bin is always empty because of the for loop
Pixels = (1:vHPix).';

% figure(2)
% subplot(2,1,1)
% plot(pTimes,RowlandTT)
% xlabel('time (ps)')
% ylabel('Rowland Signal')
% title('k\alpha time scan')
% axis tight
% 
% subplot(2,1,2)
% contourf(pTimes',Pixels',vonHamosTT,'LineStyle','None')
% colormap('jet')
% xlabel('Time (ps)')
% ylabel('Pixels')
% title('k\beta time scan')

figure(3)
subplot(2,1,1)
errorbar(pTimes,RowlandTT,TotErr);
xlabel('time (ps)')
ylabel('Rowland Signal')
title('k\alpha time scan')

subplot(2,1,2)
errorbar(pTimes,RowlandTT_nondiv,OnErr_Rowland+OffErr_Rowland)
title('Undivided k\alpha time scan')
xlabel('time (ps)')
ylabel('Rowland Signal (undiv.)')

figure(4)
subplot(2,2,1)
stem(0,Off_Rowland)
title('Laser off Rowland amplitude')
xlabel('time bins')
ylabel('Rowland Signal (arb.)')
text(0.1,Off_Rowland,num2str(Off_Rowland))

subplot(2,2,2)
plot(On_Rowland)
title('Laser on Rowland amplitude')
xlabel('time bins')
ylabel('Rowland Signal (arb.)')

subplot(2,2,3)
stem(0,Off_Diode)
xlabel('time bins')
ylabel('User Diode Signal (arb.)')
title('Laser off DiodeU amplitude')
text(0.1,Off_Diode,num2str(Off_Diode))

subplot(2,2,4)
plot(On_Diode)
title('Laser on DiodeU amplitude')
xlabel('time bins')
ylabel('User Diode Signal (arb.)')

% figure(4)
% subplot(2,2,1)
% histogram(tt_ampl(IntensityFilter&CorrFilter))
% title('tt ampl')
% xlabel('time (ps)')
% ylabel('# of shots')
% 
% subplot(2,2,2)
% histogram(tt_fltpos(IntensityFilter&CorrFilter))
% title('tt fltpos')
% xlabel('time (ps)')
% ylabel('# of shots')
% 
% subplot(2,2,3)
% histogram(tt_fwhm(IntensityFilter&CorrFilter))
% title('tt fwhm')
% xlabel('time (ps)')
% ylabel('# of shots')
% 
% subplot(2,2,4)
% plot(Ncount)
% xlabel('time bin')
% ylabel('# of shots')
% title('shots per bin')

figure(5)
subplot(3,2,1)
stem(0,OffErr)
title('Total laser off error \sigma_{off}')
xlabel('time bins')
ylabel('st. dev.')
text(0.1,OffErr,num2str(OffErr))

subplot(3,2,2)
plot(OnErr)
title('Total laser on error \sigma_{on}')
xlabel('time bins')
ylabel('st. dev.')

subplot(3,2,3)
stem(0, OffErr_Rowland)
title('Rowland laser off error')
xlabel('time bins')
ylabel('st. dev.')
text(0.1,OffErr_Rowland,num2str(OffErr_Rowland))

subplot(3,2,4)
plot(OnErr_Rowland)
title('Rowland laser on error')
xlabel('time bins')
ylabel('st. dev.')

subplot(3,2,5)
stem(0, OffErr_Diode)
title('DiodeU laser off error')
xlabel('time bins')
ylabel('st. dev.')
text(0.1,OffErr_Diode,num2str(OffErr_Diode))

subplot(3,2,6)
plot(OnErr_Diode)
title('DiodeU laser on error')
xlabel('time bins')
ylabel('st. dev.')

figure(6)
plot(pTimes,TotErr)
title('Total propogated error \sigma_{tot}')
xlabel('time bins');
ylabel('ste');

% figure(5)
% contourf(pTimes,Binedges(1:end-1),RowlandRawhist')
% colormap('jet')
% xlabel('time (ps)')
% ylabel('Rowland counts')
% title('distribution of data in different time points')

%% Save Data Matrices

%save(strcat('AveragedData_',Info),'RowlandTT','vonHamosTT','pTimes');       