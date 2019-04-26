clear all
close all
hold off
%Runs=[371:373,375:394];
Runs=[371:373, 375:377, 379:382, 384:391, 393:394];
dataon=[];
dataoff=[];
rtheta=[];

for aa=1:length(Runs);
    str1=num2str(Runs(aa));
    dataon=[dataon; load(strcat('delta_T_cee',str1,'.mat'),'Rowland_On')];
    dataoff=[dataoff; load(strcat('delta_T_cee',str1,'.mat'),'Rowland_off')];
    energy= load(strcat('delta_T_cee',str1,'.mat'),'monoaxis');
    times=load(strcat('delta_T_cee',str1,'.mat'),'Timesaxis');
end
% figure
% plot(Timesmat(1,:), datamaton)
%% Plotting all the Rowland off
figure
for aa=1:length(Runs);
    y=dataoff(aa).Rowland_off;
    doff(:,aa)=(y);
    plot(energy.monoaxis, y);
    hold on
end

hold off

%% Plotting all the Rowland on

for aa=1:length(Runs);
    y=dataon(aa).Rowland_On;
    don(:,:,aa)=y;
end

don_sum=sum(don,3);
contourf(energy.monoaxis, times.Timesaxis, don_sum, 30)



%% Plotting don and doff

figure
plot(energy.monoaxis, nanmean(don_sum(4:7,:),1), energy.monoaxis,sum(doff,2).*3)
figure
plot(energy.monoaxis, (nanmean(don_sum(4:7,:),1)-sum(doff,2)')./(sum(doff,2)'))


%% First smoothing and then taking the difference

dataonsm=sgolayfilt(nanmean(don_sum(4:7,:),1), 3,5);
dataonavg=nanmean(don_sum(4:7,:),1);
doffavg=sum(doff,2,'double');
dataoffsm=sgolayfilt(doffavg, 3,5);
figure
plot(energy.monoaxis, dataonsm, energy.monoaxis,dataoffsm)
figure
plot(energy.monoaxis, (dataonsm-dataoffsm')./(dataoffsm'),energy.monoaxis, (dataonavg-doffavg')./(doffavg'),energy.monoaxis,zeros(length(energy.monoaxis)),energy.monoaxis, dataoffsm./100000)

%% constructing difference signals by taking difference of each run with d_off and then smoothing
for aa=1:length(Runs);
    yoff=doff(:,aa);
    for bb=1:8;
        deltmat(bb,:,aa)=don(bb,:,aa)-yoff';
        deltmat1(bb,:,aa)=(don(bb,:,aa)-yoff')./(doffavg'); %percent difference for each run
    end
end
deltmat_sum=sum(deltmat,3,'double');
deltmat1_sum=sum(deltmat1,3,'double');
deltaT=(nanmean(deltmat1_sum(4:7,:),1));
deltaTsm=sgolayfilt(nanmean(deltmat1_sum(4:7,:),1),2,5);

figure
plot(energy.monoaxis, (nanmean(deltmat1_sum(4:7,:),1)),energy.monoaxis, sgolayfilt(nanmean(deltmat1_sum(4:7,:),1),2,5),energy.monoaxis,zeros(length(energy.monoaxis))) 

figure
plot(energy.monoaxis, sgolayfilt(nanmean(deltmat1_sum(4:7,:),1),2,5),energy.monoaxis, (dataonsm-dataoffsm')./(dataoffsm')) 
%% Saving file

save('FsCEEavg.mat','energy','doffavg','dataoffsm','deltaT','deltaTsm');
