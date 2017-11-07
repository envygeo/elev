#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mhwilkie
#
# Created:     10-03-2016
# Copyright:   (c) mhwilkie 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy

def main():
    out_surface_raster = arcpy.sa.TopoToRaster(r"'Spot Heights\point_metric' Z_m POINTELEVATION;'Spot Heights\point_imperial' Z_m POINTELEVATION;Contours\contour_metric Z_m CONTOUR;Contours\contour_imperial Z_m CONTOUR;NHN_lakes_3d_lines Z_m CONTOUR;vw_NHN_lakes # Lake;vw_NHN_streams # Stream;selection_buffer_90m # Boundary",
    30,
    "173810.886117477 1402236.5316 270359.969417885 1522138.55153143",
    100,
    0,
    5960,
    "ENFORCE",
    "CONTOUR",
    20,
    None,
    1,
    0,
    7.5,
    45,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None)

out_surface_raster.save(r"D:\p\ytdemv3.2016-03-08\Work\Feb-18\Work_116O\dem_30m.tif")

if __name__ == '__main__':
    main()
