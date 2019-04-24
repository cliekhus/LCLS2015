clear all
close all
load('APS_Aug_2015_Fesamples.mat','FeRu_RIXS','Fe_RIXS_emitted_axis','Fe_RIXS_incident_axis','FeII_ref_RIXS','FeIII_ref_RIXS');
apsmono=fliplr(Fe_RIXS_incident_axis);
ferurixs=fliplr(FeRu_RIXS);
fe2rixs=fliplr(FeII_ref_RIXS);
fe3rixs=fliplr(FeIII_ref_RIXS);
figure
contourf(apsmono,Fe_RIXS_emitted_axis,ferurixs,20)
lclsmon=load(('FsCEEavg.mat'),'energy');
lclsmono=lclsmon.energy.monoaxis;
lclsherf=load(('FsCEEavg.mat'),'dataoffsm');
lclsherfd=lclsherf.dataoffsm;
%%
figure
plot(lclsmono+0.75, (lclsherfd-2030)/20, apsmono.*1000, sgolayfilt(ferurixs(451,:),2,5))
%% picking 451 index in the emitted axis
% generating the difference spectrum with Fe(III)CN6 - FeRu herfd
herfd_feru=ferurixs(451,:);
aps_modiff_herfd=(fe3rixs(451,:)-fe2rixs(451,:));
aps_diff_herfd=(fe3rixs(451,:)./10)-ferurixs(451,:);
figure
plotyy(apsmono.*1000,aps_modiff_herfd, apsmono.*1000,aps_diff_herfd)
%% Save files
save('herfdiff.mat','aps_modiff_herfd','aps_diff_herfd','apsmono','herfd_feru');
%%