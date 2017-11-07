import sys
from osgeo import ogr

def main(in_file, in_format, out_file, out_format):
    if in_format == 'CSV' and in_file[-3:].lower() != 'csv':
        in_file = 'CSV:' + in_file
    in_ds = ogr.GetDriverByName(in_format).Open(in_file)
    out_ds  = ogr.GetDriverByName(out_format).CopyDataSource(in_ds, out_file)

if __name__ == '__main__':
    main(*sys.argv[1:])