%%%%%  Matlab XES spectrum (based on plot_XES_specTT.py)
clear
clc
clf

PoI = 150;  %pixel of interest for 1D plot
run = 190;  %enter run number
f = strcat('ldat_xppj6715_Run', num2str(run),'.h5');

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
BinSize = 0.05;  %width of each bin (ps)


nBinSmall = 1+(Binmax-Binmin)/BinSize; %number of bins in array
scanBinsSmall = linspace(Binmin,Binmax,nBinSmall); %create nBinSmall equal spaced data bins (50 fs each)

Lowbins = find(scanunique < Binmin-0.3);  %index all bins below minimun in linspace bins
Highbins = find(scanunique > Binmax);  %index all bins above maximum in linspace bins

scanBins = cat(1,scanunique(Lowbins)+0.3,scanBinsSmall.',scanunique(Highbins));  %Combined total time bins
nBins = length(scanBins);

Filter = find((xOn>0)&(laserOn>0)&(tt==0|(tt>0.2 & tt<0.4)));  %filtering conditions using only tt=0 and 0.2<tt<0.4, and requires both xray and laser to be on

delaysf = delays(Filter).';
specf = spec(:,Filter);
ipm2f = ipm2(Filter).';

BinIndex = zeros(length(Filter),nBins);  %preallocate bin assignments

BinIndex(:,1) = delaysf < scanBins(1);  %find first bin indices

for k = 2:nBins  %Find the rest of the bin indices
    BinIndex(:,k) = k.*((delaysf > scanBins(k-1)).*(delaysf < scanBins(k)));
end

BinIndextot = sum(BinIndex,2).';  %Each data point is now assigned to a specific bin

BinnedData = zeros(npix,nBins);  %setup binned data matrix
Binnedipm2 = zeros(1,nBins);  %setup binned normalization constant matrix

for j = 1:nBins
    MeanIndex = BinIndextot == j;  %Find any points in the current bin
    IndexfAve = find(MeanIndex);  %get the index of those points
    questn = isempty(IndexfAve);  %if there are no data points in a bin will error so need the if statement
    if questn == 0;
        BinnedData(:,j) = sum(specf(:,IndexfAve),2);  %Average all data within a bin
        Binnedipm2(j) = sum(ipm2f(IndexfAve),2);  %Average all normalization constants within a bin
    end
end

pixels = (1:npix).';  %create pixel axis for plotting

Binnedipm2mat = repmat(Binnedipm2,[388,1]);
iSpecN = (BinnedData./Binnedipm2mat).';

%%
figure(1)
contourf(pixels, scanBins ,iSpecN,'LineStyle','none')
colormap(jet);
title('Binned Data');
xlabel('pixel');
ylabel('binned delaytime (ps)');
set(gca,'Ydir','reverse');
%%
figure(2)
contourf(iSpecN,'LineStyle','none')
colormap(jet);
title('Data Binned Time Trace');
xlabel('pixel');
ylabel('time bins custom units!');
set(gca,'Ydir','reverse');
%%
figure(3)
plot(iSpecN(:,PoI));
title('Subtracted Time Slice (By Bins)');
xlabel('time bins custom units!');
ylabel('Normalized intensity');
%%
figure(4)
plot(scanBins,iSpecN(:,PoI));
title('Subtracted Time Slice (By Bins)');
xlabel('time (ps)');
ylabel('Normalized intensity');