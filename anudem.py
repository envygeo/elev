'''A helper module to produce files and data ready to ingest into ANUDEM.

License:    MIT/X Open Source, (c) 2015 Environment Yukon
Matt.Wilkie@gov.yk.ca, 2015-Feb-27
'''
import sys
from osgeo import ogr

def get_ogr_extent(layer, gdb="clipped.gdb"):
    '''Return extent of layer as (xmin, xmax, ymin, ymax) using OGR'''
    driver = ogr.GetDriverByName('OpenFileGDB')
    ds = driver.Open(gdb, 0)
    #print ds
    lyr = ds.GetLayer(layer)
    return lyr.GetExtent()

def get_arc_extent(layer):
    '''Return extent of layer as (xmin, xmax, ymin, ymax) using arcpy'''
    import arcpy # import inside function because it's so time expensive
    ext = arcpy.Describe(layer).Extent
    return [ext.XMin, ext.XMax, ext.YMin, ext.YMax]

def calc_anu_extent(cellsize, (xmin,xmax,ymin,ymax)):
    ''' Calculate grid extent for ANUDEM from extent coordinates.
        (ANUDEM requires cell/pixel size evenly divide into extents.)

        Returns [xmin, xmax, ymin, ymax]
    '''
    if cellsize == 0: cellsize = 1 # prevent modolo by zero error
    axmin = xmin - (xmin % cellsize)
    axmax = xmax + (cellsize - (xmax % cellsize))
    aymin = ymin - (ymin % cellsize)
    aymax = ymax + (cellsize - (ymax % cellsize))

    return [axmin, axmax, aymin, aymax]


def calc_tiles(extent, cellsize):
    '''Split extent into tiles of manageable size.

    tile_num = 0
    tile_extent = [xmin, xmax, ymin, ymax]
    tiles = {[tile_num]: tile_extent}

    '''
    extent =  202260.0,317100.0, 727320.0,846660.0
    xmin, xmax, ymin, ymax = extent

    xspan = xmax - xmin
    yspan = ymax - ymin

    A1.xmin = xmin
    A1.xmax = xmin + (xspan/2)
    A1.ymin = ymin
    A1.ymax = ymin + (yspan/2)

    A2.xmin = A1.xmax
    A2.xmax = xmax
    A2.ymin = A1.ymax
    A2.ymax = ymax

    B1.xmin = A1.xmin
    B1.xmax = A1.xmax
    B1.ymin = A1.ymax
    B1.ymax = ymax

    B2.xmin = A1.xmin
    B2.xmax = A1.xmax
    B2.ymin = A1.ymax
    B2.ymax = ymax

    return

def anu_cell_extents(extent_layer, start=15, stop=120, step=15):
    ''' Build dictionary of Cell sizes and their Anudem X,Y extent rectangles.
        Arguments are cell sizes to start, stop and increment by.
        Returns: {cellsize: [xmin, xmax, ymin, ymax]}
    '''
    d = {}
    for i in range(start, stop, step):
        d[i] = calc_anu_extent(i, get_ogr_extent(extent_layer))
    return d

if __name__ == '__main__':
    #infile = sys.argv[1]
    extent_layer = 'selection_buffer_3000m'
    cell_extents = anu_cell_extents(extent_layer)
    for k in sorted(cell_extents.keys()):
        print k, cell_extents[k]

