mol delete top
mol addfile C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/feru-uvvis-5.cube
display resize 1000 600
display height 1.1
display cuemode Exp2
display cuedensity 0.2
color Display Background white
color Element Fe silver
color Element Ru ochre
color Element H white
color Element C black
color Element O red3
color Element N blue3
mol modcolor 0 top ColorID 8
mol modstyle 0 top Licorice {0.1 100 100}
mol modmaterial 0 top HardPlastic
#mol modstyle 0 top CPK {1 0.3 100 100}
#mol modselect 0 top all and(not index > 33)
mol addrep top
mol modstyle 1 top Isosurface {0.002 0 0 0}
mol modcolor 1 top ColorID 4
mol addrep top
mol modstyle 2 top Isosurface {-0.002 0 0 0}
mol modcolor 2 top ColorID 16
#rotate z by 5
#rotate x by 5
render snapshot /Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/UVVIS/UVTD.bmp