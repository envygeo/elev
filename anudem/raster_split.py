"""
Raster Split Tool 6/16/2011
ArcGIS 10 Script Tool
Python 2.6.5

Contact:
Douglas A. Olsen
Geographer
Upper Midwest Environmental Sciences Center
U.S. Geological Survey
2630 Fanta Reed Road
La Crosse, Wisconsin 54603
Phone: 608.781.6333

#####
modified 2015-04-15 by Jeremiah Poling (jpoling@anra.org)
Now using only tools available at the ArcGIS Basic license level
#####

"""
import arcpy
from arcpy import env
import os

# Get Split Shapfile Name
splitShape = arcpy.GetParameterAsText(0)
# Get Field Name
splitField = arcpy.GetParameterAsText(1)
# Get Output Directory
outDirectory = arcpy.GetParameterAsText(2)
# Get Raster to Split
splitRaster = arcpy.GetParameterAsText(3)
# Get type of output tif, img, or GRID
rasterType = arcpy.GetParameterAsText(4)
# Set Workspace environment
env.workspace = outDirectory

# Loop through the rows in the clipping shapefile
cursor = arcpy.SearchCursor(splitShape)
for row in cursor:
    resultName = row.getValue(splitField)

    # Create feature layer of current clipping polygon
    whereClause = '"' + splitField + '" = ' + "'" + resultName + "'"
    arcpy.MakeFeatureLayer_management(splitShape, 'currentMask', whereClause)

    # Replace spaces with underscores
    resultName = resultName.replace(' ','_')

    # Remove .shp suffix
    if resultName[-4:] == '.shp':
        resultName = resultName[:-4]

    arcpy.AddMessage("Processing: " + resultName)

    if rasterType == 'img':
        resultName = resultName + "." + rasterType
    elif rasterType == 'tif':
        resultName = resultName + "." + rasterType
    else:
        print ('No extension')

    # Save the clipped raster
    arcpy.Clip_management(
        in_raster = splitRaster,
        rectangle = "#",
        out_raster = resultName,
        in_template_dataset = 'currentMask',
        nodata_value="255",
        clipping_geometry="ClippingGeometry",
        maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )

    if arcpy.Exists('currentMask'):
        arcpy.Delete_management('currentMask')