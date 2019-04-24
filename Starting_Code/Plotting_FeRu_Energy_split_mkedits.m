load('FeRu_XES_Static_Calibration')
load('FeRu_EG6_XES_plotting')

XaxR = FeRu_XES_Rowland_keV;
XaxvH = FeRu_XES_vonHamos_keV;


figure(1)
P = plot(XaxR, UnfiltRowland_FeRu_EG6',XaxR, FiltRowland_FeRu_EG6');
NameArray1 = {'LineStyle'};
NameArray2 = {'Color'};
NameArray3 = {'LineWidth'};
PropArray = {'-',':'}';
ColorArray = {'b',[.25 .25 .25]}';
ThickArray = {1,2}'; 
set(P,NameArray1,PropArray);
set(P,NameArray2,ColorArray);
set(P,NameArray3,ThickArray);
title('FeRu k\alpha energy difference spectrum');
xlabel('Energy (keV)');
ylabel('\Delta Signal');

figure(2)
plot(XaxR,FeRu_XES_static_Rowland','k')
title('FeRu k\alpha static spectrum')
xlabel('Energy(keV)')
ylabel('Static Signal')

figure(3)
Q = plot(XaxvH,UnfiltvonHamos_FeRu_EG6,XaxvH, FiltvonHamos_FeRu_EG6);
set(Q,NameArray1,PropArray);
set(Q,NameArray2,ColorArray);
set(Q,NameArray3,ThickArray);
title('FeRu k\beta energy difference spectrum');
xlabel('Energy (keV)');
ylabel('\Delta Signal');

figure(4)
plot(XaxvH,FeRu_XES_static_vonHamos','k')
title('FeRu k\beta static spectrum')
xlabel('Energy(keV)')
ylabel('Static Signal')
