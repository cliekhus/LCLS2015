clear;
hold off;
clf;
clc;
close all;
%%
%Run=087;
str1='378';
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
ScanVar = (h5read(f,'/scan/var0')).*1000; %scanning stage position (ps)
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
scanunique = uniquetol(ScanVar, 1e-6); %get each unique stage position used
stackunique = unique(Stacker);
%IsData = xOn&lOn;

%% Setup polynomial filter for laser off shots

%CorrFilter_off = zeros(length(ipm2),length(scanunique));
%IntensityFilter_off = zeros(length(ipm2),length(scanunique));
lOff=abs(lOn-1);
filt1=lOff&xOn;
%ipm2_f=ipm2(filt1);
%DiodeU_f=DiodeU(filt1);
%IntCorr = (DiodeU./ipm2);
%figure
%plot(IntCorr)
%IntCorrfilter = IntCorr>(nanmean(IntCorr)-2*nanstd(IntCorr))&IntCorr<(nanmean(IntCorr)+2*nanstd(IntCorr));

%CutOff = 0.035; %correlation filter variable
for zz=1:length(scanunique);
    EShots = ScanVar == scanunique(zz);
    ipmminf2 = nanmean(ipm2(EShots))-nanstd(ipm2(EShots));
    ipmmaxf2 = nanmean(ipm2(EShots))+nanstd(ipm2(EShots));
    DiodeUminf2 = nanmean(DiodeU(EShots))-nanstd(DiodeU(EShots));
    DiodeUmaxf2 = nanmean(DiodeU(EShots))+nanstd(DiodeU(EShots));
    IntensityFilter_ipm = ipm2>ipmminf2&ipm2<ipmmaxf2&EShots&filt1; 
    IntensityFilter_diode = DiodeU>DiodeUminf2&DiodeU<DiodeUmaxf2&EShots&filt1;
    totIntensityFilter=IntensityFilter_ipm&IntensityFilter_diode;
    cutoff=nanstd(DiodeU(totIntensityFilter&filt1&EShots));
    %figure
    %plot(ipm2(totIntensityFilter&filt1&EShots),DiodeU(totIntensityFilter&filt1&EShots),'r.', ipm2(EShots),DiodeU(EShots),'.g');
    %xlabel ('IPM2');
    %ylabel ('UserDiode');
    b1 = polyfit(ipm2(totIntensityFilter&filt1&EShots),DiodeU(totIntensityFilter&filt1&EShots),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    %hold on
    %refline(b1(1),b1(2)+(cutoff));  %add reference lines for the final correlation filter
    %refline(b1(1),b1(2));
    %refline(b1(1),b1(2)-(cutoff));
    y2 = polyval([b1(1) (b1(2)+(cutoff))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b1(1) (b1(2)-(cutoff))],ipm2);
    CorrFilter_off = DiodeU>y1&DiodeU<y2;
    %figure
    %plot(ipm2(CorrFilter_off&totIntensityFilter&filt1&EShots),DiodeU(CorrFilter_off&totIntensityFilter&filt1&EShots),'r.')
    %figure
    %hist(DiodeU(CorrFilter_off&totIntensityFilter&filt1&EShots)./ipm2(CorrFilter_off&totIntensityFilter&filt1&EShots))
    %numshotslOffXon=size(DiodeU(CorrFilter_off&totIntensityFilter&filt1&EShots))
    Filtoff=CorrFilter_off&totIntensityFilter&filt1&EShots;
    Rowland_off(zz)=nanmean(Rowlandsum1(Filtoff));
    Rowland_off_norm(zz)=double(nanmean(Rowlandsum1(Filtoff)./ipm2(Filtoff)));
    DiodeU_off_norm(zz)=double(nanmean(DiodeU(Filtoff)./ipm2(Filtoff)));
    DiodeU_off(zz)=nanmean(DiodeU(Filtoff),'double');
    ipm2_off(zz)=nanmean(ipm2(Filtoff));
%     figure
%     histogram(DiodeU_off_norm)
%     figure
%     histogram(DiodeU_off)
    %ncountsoff(zz)=size(DiodeU(Filtoff));
end
   figure
   plot(scanunique, Rowland_off);
   figure
   plot(scanunique, DiodeU_off);
   figure
   plot(scanunique, ipm2_off);
   figure
   plot(scanunique, DiodeU_off./ipm2_off);
   figure
   plot(scanunique, Rowland_off./ipm2_off);
   
    
   %% Time Sorting

TTfiltmin = 200; %
TTfiltmax = 800;


ttfwhm_min = mean(tt_fwhm)-2*std(tt_fwhm);
figure
subplot(2,2,1)
histogram(tt(lOn&xOn))
title('tt')
subplot(2,2,2)
histogram(tt_ampl(lOn&xOn))
title('tt_ampl')
subplot(2,2,3)
histogram(tt_fltpos(lOn&xOn))
title('tt_fltpos')
subplot(2,2,4)
histogram(tt_fwhm(lOn&xOn))
title('tt_fwhm')
    
%% Calculate Real Times    
RealTimes = -1.05e-12+tt*1e-12; %actual time delay including jitter
figure
hist(RealTimes)  
    
    %% Setup 2D matrix for time and mono energy
filt2=lOn&xOn;

tmin = -1.3e-12;
tmax = -0.9e-12;
tstep = 5e-14;
Times = [tmin:tstep:tmax];
Binedges = [60000:1000:70000];
Rowland_On=[];
Ncount_on=[];

for zz=1:length(scanunique);
   EShots = ScanVar == scanunique(zz);
    ipmminf2 = nanmean(ipm2(EShots))-nanstd(ipm2(EShots));
    ipmmaxf2 = nanmean(ipm2(EShots))+nanstd(ipm2(EShots));
    DiodeUminf2 = nanmean(DiodeU(EShots))-nanstd(DiodeU(EShots));
    DiodeUmaxf2 = nanmean(DiodeU(EShots))+nanstd(DiodeU(EShots));
    IntensityFilter_ipm = ipm2>ipmminf2&ipm2<ipmmaxf2&EShots&filt2; 
    IntensityFilter_diode = DiodeU>DiodeUminf2&DiodeU<DiodeUmaxf2&EShots&filt2;
    totIntensityFilter=IntensityFilter_ipm&IntensityFilter_diode;
    cutoff=nanstd(DiodeU(totIntensityFilter&filt2&EShots));
    %figure
    %plot(ipm2(totIntensityFilter&filt2&EShots),DiodeU(totIntensityFilter&filt2&EShots),'r.', ipm2(filt2&EShots),DiodeU(filt2&EShots),'.g');
    %xlabel ('IPM2');
    %ylabel ('UserDiode');
    b = polyfit(ipm2(totIntensityFilter&filt2&EShots),DiodeU(totIntensityFilter&filt2&EShots),1); %fit the correlation to line: b(1) = slope, b(2) = intercept
    %hold on
    %refline(b(1),b(2)+(cutoff));  %add reference lines for the final correlation filter
    %refline(b(1),b(2));
    %refline(b(1),b(2)-(cutoff));
    y2 = polyval([b(1) (b(2)+(cutoff))],ipm2); %evaluate the filter lines for a given DiodeU value
    y1 = polyval([b(1) (b(2)-(cutoff))],ipm2);
    CorrFilter_on = DiodeU>y1&DiodeU<y2;
    %figure
    %plot(ipm2(CorrFilter_off&totIntensityFilter&filt2&EShots),DiodeU(CorrFilter_off&totIntensityFilter&filt2&EShots),'r.')
    %figure
    %hist(DiodeU(CorrFilter_off&totIntensityFilter&filt2&EShots)./ipm2(CorrFilter_off&totIntensityFilter&filt2&EShots))
    Filton=totIntensityFilter&filt2&CorrFilter_on&EShots;
    TTFilter = tt_ampl>(nanmedian(tt_ampl(Filton))-2.*nanstd(tt_ampl(Filton)))&tt_fwhm>(nanmedian(tt_fwhm(Filton))-2.*nanstd(tt_fwhm(Filton)))&tt_fwhm<(nanmedian(tt_fwhm(Filton))+2.*std(tt_fwhm(Filton)))&tt_fltpos>TTfiltmin&tt_fltpos<TTfiltmax; % Timing tool filters
    for ii = 1:length(Times)-1;
    Shots = RealTimes>=Times(ii)&RealTimes<=Times(ii+1)&TTFilter&Filton&EShots; 
    Rowland_On(ii,zz) = double(nanmean(Rowlandsum1(Shots))); 
    Rowland_On_norm(ii,zz) = double(nanmean(Rowlandsum1(Shots)./ipm2(Shots))); 
    Ncount_on(ii,zz) = sum(Shots);
    xan_on(ii,zz)=double(nanmean(DiodeU(Shots)));
    xan_on_norm(ii,zz)=double(nanmean(DiodeU(Shots)./ipm2(Shots)));
    ipm2_on(ii,zz)=double(nanmean(ipm2(Shots)));
    end
end
    
figure
contourf(scanunique,Times(1:end-1),Rowland_On, 30)

figure
contourf(scanunique,Times(1:end-1),ipm2_on, 30)
%Rowland_On_norm=Rowland_On./ipm2_on;
%xan_on_norm=xan_on./ipm2_on;

%% Create Difference Data

delta_T_cee=[];
delta_T_cee_norm=[];

for jj= 1:length(Times)-1;
    delta_T_cee(jj,:)=(Rowland_On(jj,:)-Rowland_off);
    delta_T_cee_norm(jj,:)=(Rowland_On_norm(jj,:)-Rowland_off_norm);
end

Timesaxis=Times(1:end-1); % Time axis with last bin removed. 

figure
contourf(scanunique,Times(1:end-1),delta_T_cee,30)

figure
contourf(scanunique,Times(1:end-1),delta_T_cee_norm,30)

figure
plot(scanunique,delta_T_cee )

Timesaxis=Times(1:end-1);
monoaxis=scanunique;
%% Create xanes Difference Data

delta_T_xan=[];
delta_T_xan_norm=[];

for jj= 1:length(Times)-1;
    delta_T_xan(jj,:)=(xan_on(jj,:)-DiodeU_off);
    delta_T_xan_norm(jj,:)=(xan_on_norm(jj,:)-DiodeU_off_norm);
end


figure
contourf(scanunique,Times(1:end-1),delta_T_xan,30)

figure
plot(scanunique,delta_T_xan) 
figure
plot(scanunique,delta_T_xan_norm)

%%
figure
plot(scanunique, sum(delta_T_cee(4:7,:),1),'-o',scanunique, smooth(sum(delta_T_cee(4:7,:),1)),scanunique, medfilt1(sum(delta_T_cee(4:7,:),1),4),scanunique, sgolayfilt(sum(delta_T_cee(4:7,:),1),3,5) )

figure
plot(scanunique, sum(delta_T_xan(4:7,:),1),'-o',scanunique, smooth(sum(delta_T_xan(4:7,:),1)),scanunique, medfilt1(sum(delta_T_xan(4:7,:),1),4),scanunique, sgolayfilt(sum(delta_T_xan(4:7,:),1),3,5) )

% figure
% plot(scanunique, sum(delta_T_cee_norm(4:7,:),1),'-o',scanunique, smooth(sum(delta_T_cee_norm(4:7,:),1)),scanunique, medfilt1(sum(delta_T_cee_norm(4:7,:),1),4),scanunique, sgolayfilt(sum(delta_T_cee_norm(4:7,:),1),3,5) )
% 
% figure
% plot(scanunique, sum(delta_T_xan_norm(4:7,:),1),'-o',scanunique, smooth(sum(delta_T_xan_norm(4:7,:),1)),scanunique, medfilt1(sum(delta_T_xan_norm(4:7,:),1),4),scanunique, sgolayfilt(sum(delta_T_xan_norm(4:7,:),1),3,5) )

% figure
% plot(scanunique, smooth(sum(delta_T_cee(4:6,:),1))./smooth(RowlandOff_norm))

%% save files

%f1=strcat('delta_T_',str1,'_norm','.mat');
%f2=strcat('delta_T_',str1, '.mat');
%rtheta = scanunique;
%energyaxis=polyval(bb, scanunique);
save(strcat('delta_T_cee',str1,'_1.mat'), 'delta_T_cee','delta_T_cee_norm','Timesaxis', 'monoaxis','Ncount_on','Rowland_off','Rowland_off_norm','Rowland_On','Rowland_On_norm')
save(strcat('delta_T_xan',str1,'_1.mat'), 'delta_T_xan','delta_T_xan_norm','Timesaxis', 'monoaxis','Ncount_on','xan_on','xan_on_norm','DiodeU_off','DiodeU_off_norm')
%% %end
close all