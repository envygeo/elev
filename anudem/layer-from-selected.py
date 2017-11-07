''' Create layer from selected features.

    Duplicates "r-click > ... > Create Layer from Selected Features".

    Adapted from:
        - use a selection of features in ArcMap in Python script
            http://gis.stackexchange.com/questions/63717/

        - copy only selected with CopyFeature_management
            http://gis.stackexchange.com/questions/123414/
'''
import arcpy

selected = ''
result = ''
outname = result + '_selection'

def main():
    arcpy.CopyFeatures_management(selected, result)
    arcpy.MakeFeatureLayer_management(result, outname)

if __name__ == '__main__':
    main()
