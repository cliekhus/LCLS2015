%%%%%  Matlab XES spectrum with pump on/off subtraction (based on plot_XES_specTT.py)
clear
clc
clf

PoI = 150;  %Pixel of Interest for 1D plot
run = 104;  %enter run number
f = strcat('ldat_xppi3815_Run', num2str(run),'.h5');

%%%% Load idividual data from data file
xOn = h5read(f,'/lightStatus/xray');  %x-ray on or off
laserOn = h5read(f,'/lightStatus/laser');  %laser on or off
ipm2 = h5read(f,'/ipm2/sum'); %shot to shot correction value
spec = h5read(f,'/vonHamos/ROI_proj_thresRms');  %detector data
tt = h5read(f,'/ttCorr/tt'); % jitter time correction value (ps)
ScanVar = h5read(f,'/scan/lxt_vitara_ttc'); %scanning stage position (sec)
picoScanVar = ScanVar*1e12; %scanning stage position (ps)
scanunique = unique(picoScanVar); %get each unique stage position used

[npix, ntpts] = size(spec); % number of pixels and total points

delays = picoScanVar+tt; %get true delay (ps) for each time point using stage position and jitter correction

Binmin = 0.2;  %first time bin (ps)
Binmax = 1.3;  %last time bin (ps)
nBinSmall = 23; %number of bins in array

scanBinsSmall = linspace(Binmin,Binmax,nBinSmall); %create nBinSmall equal spaced data bins (50 fs each)

Lowbins = find(scanunique < Binmin-0.3);  %index all bins below minimun in linspace bins
Highbins = find(scanunique > Binmax);  %index all bins above maximum in linspace bins

scanBins = cat(1,scanunique(Lowbins)+0.3,scanBinsSmall.',scanunique(Highbins));  %Combined total time bins
nBins = length(scanBins);


FilterOn = find((xOn>0)&(laserOn>0)&(tt==0|(tt>0.2&tt<0.4)));  %filtering conditions using only tt=0 and 0.2<tt<0.4, and requires both xray and laser to be on
FilterOff = find((xOn>0)&(laserOn<1));  %filtering conditions using only scans with the xray on and the laser off

delaysfOn = delays(FilterOn).';  %On vs. Off refers to the laser pump
delaysfOff = delays(FilterOff).';
specfOn = spec(:,FilterOn);
specfOff = spec(:,FilterOff);
ipm2fOn = ipm2(FilterOn).';
ipm2fOff = ipm2(FilterOff).';

BinIndexOn = zeros(length(FilterOn),nBins);  %preallocate bin assignments

BinIndexOn(:,1) = delaysfOn < scanBins(1);  %find first bin indices

for k = 2:nBins  %Find the rest of the bin indices
    BinIndexOn(:,k) = k.*((delaysfOn > scanBins(k-1)).*(delaysfOn < scanBins(k)));
end

BinIndexTotOn = sum(BinIndexOn,2).';  %Each data point is now assigned to a specific bin

BinnedDataOn = zeros(npix,nBins);  %setup binned data matrix
Binnedipm2On = zeros(1,nBins);  %setup binned normalization constant matrix

for j = 1:nBins
    MeanIndexOn = BinIndexTotOn == j;  %Find any points in the current bin
    IndexfAveOn = find(MeanIndexOn);  %get the index of those points
    questn = isempty(IndexfAveOn);  %if there are no data points in a bin will error so need the if statement  !Will only process if both ON and OFF bins have data!
    if questn == 0;
        BinnedDataOn(:,j) = sum(specfOn(:,IndexfAveOn),2);  %Average all data within a bin
        Binnedipm2On(j) = sum(ipm2fOn(IndexfAveOn),2);  %Average all normalization constants within a bin
    end
end

pixels = (1:npix).';  %create pixel axis for plotting

iSpecNoff = mean(specfOff,2);
ipm2offave = mean(ipm2fOff);

Binnedipm2matOn = repmat(Binnedipm2On,[npix,1]);  %Creates matrix for normalization division

iSpecNOn = (BinnedDataOn./Binnedipm2matOn).';
iSpecNOff = (iSpecNoff/ipm2offave).';

subtspec = repmat(iSpecNOff, [nBins,1]);

iSpecNSub = iSpecNOn-subtspec;

%%
figure(1)
contourf(pixels, scanBins ,iSpecNOn,'LineStyle','none');
colormap(jet);
title('Pumped Spectrum (By Time)');
xlabel('pixel');
ylabel('binned delaytime (ps)');
set(gca,'Ydir','reverse');
%%
figure(2)
contourf(iSpecNOn,'LineStyle','none');
colormap(jet);
title('Pumped Spectrum (By Bins)');
xlabel('pixel');
ylabel('time bins custom units!');
set(gca,'Ydir','reverse');
%%
figure(3)
contourf(pixels, scanBins, iSpecNSub,'LineStyle','None');
colormap(jet);
title('Subtracted Spectrum (By Bins)');
xlabel('pixel');
ylabel('time bins custom units!');
set(gca,'ydir','reverse');
%%
figure(4)
contourf(iSpecNSub,'LineStyle','None');
colormap(jet);
title('Subtracted Spectrum (By Bins)');
xlabel('pixel');
ylabel('time bins custom units!');
set(gca,'ydir','reverse');
%%
figure(5)
plot(scanBins,iSpecNSub(:,PoI));
title('Subtracted Time Slice (By Bins)');
xlabel('time bins custom units!');
ylabel('Normalized intensity');