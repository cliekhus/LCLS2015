#mol delete top
#mol addfile C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/feru-uvvis-5.cube
display resize 1000 800
#display height 1.1
display height 2.3
display cuemode Exp2
display cuedensity 0.2
color Display Background white
color Element Fe silver
color Element Ru ochre
color Element H white
color Element C black
color Element O red3
color Element N blue3
color change rgb silver
color change rgb ochre
color change rgb black
color change rgb white
color change rgb red3 0.95 0.07 0.07
color change rgb blue3 0.09 0.25 0.81
color change rgb gray 0.23 0.23 0.25
color change rgb orange3 1 0.89 0
color change rgb violet2 0.42 0 0.93
color change rgb green2 0.21 0.86 0.15
mol modcolor 0 top Element
mol modstyle 0 top Licorice {0.1 100 100}
mol modmaterial 0 top Edgy
mol addrep top
mol modstyle 1 top Isosurface {2e8 0 0 0}
mol modcolor 1 top ColorID 26
mol modmaterial 1 top Edgy
mol addrep top
mol modstyle 2 top Isosurface {-2e8 0 0 0}
mol modcolor 2 top ColorID 19
mol modmaterial 2 top Edgy
mol addrep top
mol modstyle 3 top DynamicBonds {2.2 0.1 100}
mol modcolor 3 top Element
mol modmaterial 3 top Edgy
mol modselect 3 top "not name H"
#rotate z by 5
#rotate x by 5
light 0 on
light 1 on
light 2 on
light 3 off
render snapshot C:///Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/UVTD.bmp