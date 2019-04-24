clear all
hold off
Runs=[190 191];

dataon=[];
dataoff=[];
rtheta=[];

for aa=1:length(Runs);
    str1=num2str(Runs(aa));
    dataon=[dataon; load(strcat('deltaTKalphaenergy_',str1,'.mat'),'RowlandOn_norm')];
    dataoff=[dataoff; load(strcat('deltaTKalphaenergy_',str1,'.mat'),'RowlandOff_norm')];
    rtheta=[rtheta; load(strcat('deltaTKalphaenergy_',str1,'.mat'),'rtheta')];
    times=load(strcat('deltaTKalphaenergy_',str1,'.mat'),'Timesaxis');
end
% figure
% plot(Timesmat(1,:), datamaton)
%% averaging 190 and 191
dataon190=nanmean(dataon(1).RowlandOn_norm(4:6,:));
dataoff190=dataoff(1).RowlandOff_norm;
dataon191=nanmean(dataon(2).RowlandOn_norm(4:6,:));
dataoff191=dataoff(2).RowlandOff_norm;
rth=rtheta(1).rtheta;
for zz=1:length(rth);
    eshots=rtheta(2).rtheta==rth(zz);
    dataon1(zz)=double(nansum(dataon191(eshots)));
    dataoff1(zz)=double(nansum(dataoff191(eshots)));  
end
totdata(1,:)=dataon190;
totdata(2,:)=dataon1;

totdataoff(1,:)=dataoff190;
totdataoff(2,:)=dataoff1;

%dataonavg=nanmean(totdata);
%dataoffavg=nanmean(totdataoff);

delT190=dataon190-dataoff190;
delT191=dataon1-dataoff1;

plot(rth, delT190, rth-0.005, delT191)

%cannot average 190 and 191 together because there is a difference in the
%energy scales of the two data sets. 


%% First average all the data for Run 190

%construct delta T averaged over a specific time interval 4:5

delT46=(nanmean(dataon(1).RowlandOn_norm(4:6,:)))-dataoff(1).RowlandOff_norm;
figure
plot(rtheta(1).rtheta, delT46)
figure
plot(rtheta(1).rtheta, delT46./dataoff(1).RowlandOff_norm)
%% Filter the data and then plot it

dataoff_filt=sgolayfilt(dataoff(1).RowlandOff_norm, 2,5);
dataon_filt=sgolayfilt(nanmean(dataon(1).RowlandOn_norm(4:6,:)), 2,5);
figure
figure
plot(rtheta(1).rtheta, (dataon_filt-dataoff_filt),rtheta(1).rtheta, delT46, rtheta(1).rtheta, sgolayfilt(delT46, 2,5))
figure
plot(rtheta(1).rtheta, (dataon_filt-dataoff_filt)./dataoff_filt,rtheta(1).rtheta, delT46./dataoff_filt )


%%

%% First average all the data for Run 190

%construct delta T averaged over a specific time interval 4:5

delT56=((dataon(1).RowlandOn_norm(5,:)))-dataoff(1).RowlandOff_norm;
figure
plot(rtheta(1).rtheta, delT56)
figure
plot(rtheta(1).rtheta, delT56./dataoff(1).RowlandOff_norm)
%% Filter the data and then plot it

dataoff_filt=sgolayfilt(dataoff(1).RowlandOff_norm, 2,5);
dataon_filt=sgolayfilt((dataon(1).RowlandOn_norm(5,:)), 2,5);
figure
figure
plot(rtheta(1).rtheta, (dataon_filt-dataoff_filt),rtheta(1).rtheta, delT56, rtheta(1).rtheta, sgolayfilt(delT56, 2,5))
figure
plot(rtheta(1).rtheta, (dataon_filt-dataoff_filt)./dataoff_filt,rtheta(1).rtheta, delT56./dataoff_filt )
%%
for zz=1:length(times);
    


dataon_avg=nanmean(datamaton(1:end,:));
dataoff_avg=nanmean(dataoff(1:end));
delta_Tavg=(dataon_avg-dataoff_avg)/(dataoff_avg);

figure
plot(Timesmat(1,:), delta_Tavg)

%error propagation
dataon_std=nanstd(datamaton(1:end,:),1)./sqrt(9);
dataoff_std=nanstd(dataoff(1:end),1)./(sqrt(9));
delta_Tstd=sqrt(((dataon_std)./(dataon_avg)).^2+(dataoff_std/dataoff_avg)^2);

figure
plot(Timesmat(2,:), delta_Tavg)
title('Average delta_T Runs 155-158 and 160-164')

figure
errorbar(Timesmat(2,:), delta_Tavg, delta_Tstd/2)
title('Average delta_T Runs 155-158 and 160-164 with standard mean error')

% figure
% errorbar(Timesmat(1,:), delta_Tavg, ((dataon_std)./(dataon_avg))./2)

%% First calculate delta_T and then average. 

for zz=1:length(Runs)-1;
    delta_Tmat(zz,:)=(datamaton(zz+1,:)-dataoff_avg)./dataoff_avg;
end

for zz=1:length(Runs)-1;
    delta_Tmat1(zz,:)=(datamaton(zz+1,:)-dataoff(zz+1))./dataoff(zz+1);
end


figure
plot(Timesmat(1,:), nanmean(delta_Tmat), Timesmat(1,:), delta_Tmat)
 
figure
plot(Timesmat(1,:), delta_Tavg, Timesmat(1,:), nanmean(delta_Tmat))

%% Sticking with delta_Tavg assembling final data set

Ncount_avg=nansum(countmat(2:end,:));
Timedelay=Timesmat(2,:);
delta_Tstdmeanerror=delta_Tstd;
save('data_155_164_FeRu.mat','Timedelay','delta_Tavg','delta_Tstdmeanerror','Ncount_avg');

%%

