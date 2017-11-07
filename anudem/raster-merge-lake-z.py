import arcview
import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

lake = r'Q:\ytdemv3\scratch\clipped.gdb\NHN_lake_Z_15m'
dem = r'Q:\ytdemv3\scratch\h05\dem_15m.flt'
out =  r'Q:\ytdemv3\scratch\clipped.gdb\dem_flak_15m'
r_out = Con(IsNull(lake),dem,lake)
r_out.save(out)
