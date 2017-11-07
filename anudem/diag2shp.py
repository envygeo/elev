'''Convert ANUDEM diagnostic files to GIS ready data'''
import os
import sys
import numpy as np
from osgeo import ogr

infile = sys.argv[1]
    ##infile = 'xx_large_residuals.pnt'

def large_residuals_to_csv(infile):
    '''Convert "Large Residuals" to CSV'''
    name = os.path.splitext(infile)[0]
    outfile = name + '.csv'
    header = 'Scaled_Residual,X,Y,Local_Std_Error,Vertical_Std_Error,Unscaled_Residual'
    data = np.genfromtxt(infile, names=header, dtype=None, comments='E')
        #'E' skips "END" lines
    np.savetxt(outfile, data, header=header, delimiter=',', comments='',
        fmt='%10s')
    print 'Saved', outfile
    return outfile

def contour_err_to_csv(infile):
    '''Convert "Contour Errors" to CSV'''
    name = os.path.splitext(infile)[0]
    outfile = name + '.csv'
    header = 'Flag,X,Y,Elevation_1,Elevation_2'
    data = np.genfromtxt(infile, names=header, dtype=None, comments='E')
        #'E' skips "END" lines
    np.savetxt(outfile, data, header=header, delimiter=',', comments='',
        fmt='%10s')
    print 'Saved', outfile
    return outfile

def contour_err_csv_to_vrt(csvfile):
    layer = os.path.splitext(os.path.basename(csvfile))[0]
        #filename with no path or extension
    template = '''<OGRVRTDataSource>
    <OGRVRTLayer name="{layer}">
    <SrcDataSource relativeToVRT="1">{filename}</SrcDataSource>
    <GeometryType>wkbPoint</GeometryType>
    <LayerSRS>EPSG:3579</LayerSRS>
    <GeometryField reportSrcColumn="false" encoding="PointFromColumns" x="X" y="Y"/>
      <Field name="Flag" src="Flag" type="Integer" />
      <Field name="Elevation_1" src="Elevation_1" type="Real" />
      <Field name="Elevation_2" src="Elevation_2" type="Real" />
    </OGRVRTLayer>
</OGRVRTDataSource>
'''.format(layer=layer, filename=csvfile)
    return template

def large_residuals_csv_to_vrt(csvfile):
    layer = os.path.splitext(os.path.basename(csvfile))[0]
        #filename with no path or extension
    template = '''<OGRVRTDataSource>
    <OGRVRTLayer name="{layer}">
    <SrcDataSource relativeToVRT="1">{filename}</SrcDataSource>
    <GeometryType>wkbPoint</GeometryType>
    <LayerSRS>EPSG:3579</LayerSRS>
    <GeometryField reportSrcColumn="false" encoding="PointFromColumns" x="X" y="Y"/>
      <Field name="Scaled_Residual" src="Scaled_Residual" type="Integer" />
      <Field name="Local_Std_Error" src="Local_Std_Error" type="Real" />
      <Field name="Vertical_Std_Error" src="Vertical_Std_Error" type="Real" />
      <Field name="Unscaled_Residual" src="Unscaled_Residual" type="Real" />
    </OGRVRTLayer>
</OGRVRTDataSource>
'''.format(layer=layer, filename=csvfile)
    return template

def write_file(content, outfile):
    with open(outfile, 'w') as f:
        f.write(content)
    f.close()
    print 'Saved', outfile
    return outfile

##def ogr2ogr(in_file, in_format, out_file, out_format):
##    if in_format == 'CSV' and in_file[-3:].lower() != 'csv':
##        in_file = 'CSV:' + in_file
##    in_ds = ogr.GetDriverByName(in_format).Open(in_file)
##    out_ds  = ogr.GetDriverByName(out_format).CopyDataSource(in_ds, out_file)

if __name__ == '__main__':
    dem_name = os.path.basename(os.path.dirname(infile))

    if 'large_residual' in infile.lower():
        csvfile = large_residuals_to_csv(infile)
        vrt = large_residuals_csv_to_vrt(csvfile)

    if 'contour_error' in infile.lower():
        csvfile = contour_err_to_csv(infile)
        vrt = contour_err_csv_to_vrt(csvfile)

    vrtfile = write_file(vrt, os.path.splitext(infile)[0] + '.vrt')
    print '\nNext run:\n\t ogr2ogr -f filegdb {}.gdb {}'.format(dem_name, vrtfile)



##    ogr2ogr(vrtfile, '', 'test', 'FileGDB')