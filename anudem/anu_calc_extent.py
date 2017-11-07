def calc_extent(cellsize, featureclass):
    ''' Calculate grid extent for ANUDEM from extent of input shape.

        ANUDEM requires cell (pixel) size evenly divide into extents.

        Returns [xmin, xmax, ymin, ymax]
    '''
    import arcpy
    cellsize = 200
    desc = arcpy.Describe(featureclass)
    ext = desc.Extent

    xmin = ext.XMin - (ext.XMin % cellsize)
    xmax = ext.XMax + (cellsize - (ext.XMax % cellsize))
    ymin = ext.YMin - (ext.YMin % cellsize)
    ymax = ext.YMax + (cellsize - (ext.YMax % cellsize))

    return [xmin, xmax, ymin, ymax]