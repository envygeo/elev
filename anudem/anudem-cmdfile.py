enforce          # enforce off|on|diag
main_type        # Main datatype is...
rms vse        # RMS and vertical SE = 1.0 0.0
rough            # Roughness Trade-Off = 0.05
Tol_1 Tol_2    # tolerances
iterate          # Max Iterations = 40
Zunit            # meters = 1
minZ maxZ      # vertical extents
pix-cnt          # pixel center is = 1 (in center)
hor-unit         # Hor. Units (1 M, 2 FT, 3 KM, 4 MI, 5 DEG, 6 RAD)
minX maxX      # Long. extents
minY maxY      # Lat. extents
cell-size        # cell size
out-cols          # output columns
out-rows          # output rows
margin            # margin
wrk-cols          # working grid columns
wrk-rows          # working grid rows
&do   # cycle through all input data until done
   &s inputs = in_cont in_cont# in_spot in_spot# in_lakectr in_lakectr# in_crik in_crik# in_lake in_lake#
   &s in_total = [token inputs -count] / 2
      in_total       # number of input data files
   &do input_each &list inputs
      input_each
   &end
&end
# output files
out-dem         # output demfile
out-type        # output flavour (ArcGRID Ascii, etc.)
out-def         # output type definition (ascii, binary)
# diagnostics output
sinks             # sink errors
out-crik          # output streams (blank | dem.crk)
res               # large residuals
strmer            # stream errors
bnder             # boundary poly errors
conter            # contour errors
laker             # lake errors
grid_pnt          # grid point (blank | dem.pnt)
aspect            # aspect grid (blank | dem.asp)

# To fix "Data transfer beyond end of file" error messages from anudem
# uncomment the next line. This doesn't seem to be necessary under
# Windows 2000 (later: but is under windows xp?!) (and NT4)
&sys unix2dos cmdfile

#...ANUDEM cmdfile file is built.

##
##
##
##
### &args tile cell-size elev contours spots watercourses lake_ctr
##
##
##enforce = 1       # Enforcement [Off|On|Diag]
##main_type = 1     # contours=1, points=0
##rms = 1.0         # RMS  (1.0)
##vse = 0.0         # vertical SE (0.0)
##rough = 0.05      # roughness tradeoff penalty; contour=0.0, point=0.5
##&call Tolerances     # autocalc the values from input data
##   # Tol_1 =        # half contour interval
##   # Tol_2 =        # half the total elevation span
##iterate = 40      # max number of iterations (40)
##Zunit = 1         # 1=meters, 2=feet
### autocalc'd in Tolerances routine
##   #minZ =       # Elevation Extent
##   #maxZ =
##pix-cnt = 1       # pixel center = center of cell or corners (1)
##
### FIXME: should be auto-set from projection of input data
##hor-unit = 1      # horizontal units (1 M, 2 FT, 3 KM, 4 MI, 5 DEG, 6 RAD)
##
####cell-size = %cell-size%      # size of single pixel in ground units
##
### use pyExtents if using a fractional cell-size, amlExtents otherwise
### FIXME: should choose appropriate routine automaticaly
####&call pyExtents
#####&call amlExtents
##
###  no need to specify, columns/rows are automatically calculated by ANUDEM
##out-cols =              # num output columns
##out-rows =              # num output rows
##margin   = 0.0          # Margin (default = 20)
##wrk-cols =              # num working columns
##wrk-rows =              # num working rows
##
### ---------------------------------------------------------------------
####in_total =           # # of input data files (auto calculated later)
### ANUDEM type #s for ArcInfo ungenerate input data types:
###    21=ARC/INFO POINT DATA    24=ARC/INFO POLYGON
###    22=ARC/INFO SINK POINT    25=ARC/INFO CONTOUR
###    23=ARC/INFO STREAMLINE    26=ARC/INFO LAKE BDRY
### in_%cover% = path to ungenerate file
### in_%cover% = ANUDEM type #
##
##in_cont = %contours%.gen      # contours
##in_cont# = 25
##
##in_spot = %spots%.gen         # spot heights
##in_spot# = 21

