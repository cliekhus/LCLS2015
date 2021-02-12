All of the figures in the LCLS 2015 paper can be created form the files in this folder (except the SI figure explaining the bootstrapping, which has to be done by hand.)

All of the data for the figures is contained in the paper are in the folder "LCLS_Data"
You will have to update the the position of this folder in the code.

Note: Some python scripts change the default text size.  You may have to restart the kernel before running the figure scripts to get the correct font sizes.

Now a more detailed explanation of how to create each figure:

Figure 1:
Created in Adobe Illustrator
Location: LCLS2015/Figures/LCLS_2015_Exp_Fig.ai

Figure 2, 3, S8:
Created in Python
Location: LCLS2015/XES/XES_Final_Plot.py

Update the file variables
APSName
folder1
folder2
folder3

Figure 4, S9, S10:
Created in Python
Location: LCLS/Harmonics/InfraRed.py and LCLS/Harmonics/VectorFile.py
Figure 4 Left hand side: Comment out line 242, comment out line 74, and uncomment line 75 in "InfraRed.py" then run "VectorFile.py"
Figure 4 Right hand side, S9, S10: Use the code as it was written and run "VectorFile.py"

Figure 5, 6, S19, S21:
Created in Python
Location: LCLS/XAS/FinalFigure.py

Update the file variables
folder (line 140)
line 1100 and 1102 update location of the LCLS_Data folder

Figure 7:
Created in VMD
Use LCLS2015/XAS/simulation/TDs.tcl to create each transition density in VMD.
a) feru-pt10-tdens-1.cube
b) feru-pt10-tdens-5.cube
c) feru-pt68-tdens-1.cube
d) feru-pt68-tdens-5.cube

Figure 8:
Created in Adobe Illustrator
LCLS2015/Figures/MMCTPlot.ai

Figure S1:
Created in Python
LCLS2015/Harmonics/Full_IR.py

Figure S2:
Created in Python
LCLS2015/UVVIS/UVVIS.py

Figure S3:
Created in VMD
Use LCLS2015/UVVIS/UVTD.tcl to create the transition density from feru-uvvis-5.cube.

Figure S4, S5, S13:
Created in Python
Location: LCLS2015/XAS/APS_Figure.py
Change lines 31, 172, 174, 176, 178 with the appropriate file locations
S5 additionally used Adobe Illustrator
See LCLS2015/Figures/RIXS_HERFD.ai and LCLS2015/Figures/FeMOs.ai

Figure S6:
Created in Python
Location: LCLS2015/XES/laser_scan.py

Update file locations at lines
19, 41, 68

Figure S7:
Created in Python
move to location LCLS/XES
enter the following into your console
import pickle
folder = "D://LCLS_Data/LCLS_python_data/XES_Spectra/" # change this accordingly
with open(folder + "xesProData.pkl", "rb") as f: xesProData = pickle.load(f)
import makeStaticPlot
xesProData.makeStaticPlot()

Figure S11:
Created in Python
Location LCLS/Harmonics/calculatedFT.py

Figure S12:
Created in Python
Location LCLS/XES/delta_estimate.py

Update file location on line 24

Figure S15:
Created in Python
Location LCLS2015/XAS/CompareHERFD_TFY.py
Update file locations on lines
14, 17, 20, 25, 30

Figures S16, S17, S18:
Creates with VMD
Use LCLS2015/XAS/simulation/MOs.tcl on the mo cube files

Figure S20:
Created with VMD
Use LCLS2015/XAS/simulation/TDs.tcl on the tdens cube files

Figure S22:
Created with Python
Location: LCLS2015/XAS/Cpeak_analysis.py