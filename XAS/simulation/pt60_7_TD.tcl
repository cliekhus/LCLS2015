mol delete top
mol addfile C://Users/chelsea/Downloads/cubes/feru-pt60-tdens-7.cube
#mol addfile C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/simulation/feru-pt10-tdens-7.cube
display resize 1000 600
display height 1.6
display cuemode Exp2
display cuedensity 0.2
color Display Background white
mol modcolor 0 top ColorID 8
mol modstyle 0 top Licorice {0.1 100 100}
mol modmaterial 0 top HardPlastic
#mol modstyle 0 top CPK {1 0.3 100 100}
#mol modselect 0 top all and(not index > 33)
mol addrep top
mol modstyle 1 top Isosurface {60 0 0 0}
mol modcolor 1 top ColorID 4
mol addrep top
mol modstyle 2 top Isosurface {-60 0 0 0}
mol modcolor 2 top ColorID 16
rotate z by 0
rotate x by 0
rotate y by 0
translate by -.05 0 0
#render snapshot C://Users/chels/OneDrive/Documents/UW/Mixed-Valence-Complexes/LCLS2015/XAS/pt10_7_TD.bmp
render snapshot C://Users/chelsea/Downloads/cubes/pt60_7_TD.png