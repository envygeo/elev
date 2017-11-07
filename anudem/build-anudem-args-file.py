''' Build an Anudem v5.3 parameter file.

Anudem is a command line program which is fed by typing in the parameters or redirecting the same from text file:

    anudemc < make_30m_dem.cmd

Thus the line order of the text file is immutable.

    Section 1 - Variables:
        - Lines 1 to 15 never change position, e.g. Line 8 is always elevation min/max bounds while lines 11 & 12 are always X,Y min/max.

    Section 2 - Input files:
        - Lines 16+ are input data files and thus variable number of lines
        - format:
            \path\to\filename
            integer of format type (arcinfo, idrisi, etc.)

    Section 3 - Output files
        - Output DEM
        - Diagnostic files

This is a minimal summary, refer to Anudem docs for details and options.
'''
import os
import glob
from anudem import *
from attrdict import AttrDict

##in_gen_files = ['BDG_DBA_nhn_hhyd_Waterbody_2_lakes.gen',
##    'BDG_DBA_nhn_hhyd_Waterbody_2_notlakes.gen',
##    'BDG_DBA_nhn_hnet_Network_Linear_Flow_1.gen',
##    'contour_imperial.gen',
##    'contour_metric.gen',
##    'NHN_lake_z.gen',
##    'cvplus_lake_z.gen',
##    'point_imperial.gen',
##    'point_metric.gen',
##    'selection_buffer_3000m.gen']

in_gen_files = []

a = AttrDict()

# Parameters, listed in same order as they are written to the file
a.enforce = '1'         # 0/1 = on/off, 2 = sink diagnostics
a.datatype = '1'        # 0 = mainly spot heights, 1 = mainly contours
a.rms_vse = '1.0, 0.0, 0.0, 0.2'
                        # Error factors: Discretization, Vertical standard,
                        # cliff position, stream position
a.roughness = '0.0, 0.05'   # roughness tradeoff, profile curvature
a.tolerances = '7.5, 45.0'  # Elevation tolerances: half contour interval, 6 * 1st tol
a.iterations = '20'     #max number of iterations
a.z_units = '1'         # Elevation units, 1=meters, 2=feet
a.z_min_max = '0, 5959' # min and max elevation bounds (max is Mt Logan ;-)
a.centering = '1'       # 0=point at cell corner, 1=point at centre
a.xy_units = '1'        # 1=m, 2=ft, 3=km, 4=mi, 5=degrees, 6=radians
a.x_limits = ' '         # min, max X coordinates
a.y_limits = ' '         # min, max Y coordinates
a.cellsize = '30'        # grid spacing
a.margin = '3000'        # use data X distance beyond final DEM bounds
a.num_files = ' '        # number of input data files

# --- Dynamic settings ---
# These redefine the above items, and are just repeated here for easy editing.
a.tolerances = '7.5, 45.0'  # Elev tolerances: half contour interval, 6 * 1st tol
a.z_min_max = '0, 5960'     # min and max elevation bounds
a.x_limits = ' ' # min, max X coordinates
a.y_limits = ' ' # min, max Y coordinates
a.cellsize = ' '        # grid spacing
a.margin = '3000'        # use data X distance beyond final DEM bounds
a.num_files = str(len(in_gen_files))


def get_file_names(folder, pattern):
    '''Return list of files matching 'pattern' in 'folder'.
       Only filename and extension is returned, leading path is stripped.'''
    pattern = os.path.join(folder, pattern)
    files = [os.path.basename(x) for x in glob.glob(pattern)]
    return files

def parse_data_types(in_gen_files):
    '''Build Anudem input data file parameters.

    Returns: [{datafile.ext}, {Anudem data type integer}]

    Data types are determined from keywords in the filenames.
    Brittle, but works well enough for present.

        Elevation:      countour, point, lake_z
        Lakes:          lake
        Watercourses:   flow, notlake

    Anudem Data Types:
        25 = Elevation Contour
        21 = Elevation Point
        26 = Waterbody
        23 = Stream data
    '''
    outfiles = []
    for f in in_gen_files:
        if not os.path.exists(f):
            print '--- Skipping not exist', f
            continue
        if os.path.getsize(f) < 1:
            print '--- Skipping empty', f
            continue

        # Elevation
        if 'contour' in f.lower():
            outfiles.append([f,'25'])
        if 'point' in f.lower():
            outfiles.append([f,'21'])
        if f.lower().endswith('_z'):
            outfiles.append([f,'25'])

        # Waterbodies
        if '_lake' in f.lower():
            outfiles.append([f,'26'])

## Skipping 2 line rivers all together. Too much artifacting in resultant DEM
##        # Waterbodies to treat as streams
##        if 'notlake' in f.lower():
##            outfiles.append([f,'23'])

        # streams, watercourses
        if 'flow' in f.lower():
            outfiles.append([f,'23'])
    return outfiles

def write_data_files(cmdfile, data_files):
    '''Split data_files list into "name, type" and append to cmdfile'''
    with open(cmdfile, 'at') as f:
        f.write('\n')
        f.write(str(len(data_files)))
        #print data_files
        for i in data_files:
            f.write('\n')
            f.write('\n'.join(i))
    f.close()

def write_diag_parms(cmdfile, name, cellsize):
    ''' Paths and names of Anudem output files (DEM and diagnostics).
        3rd and final section of the command parameters file.
    '''
    dem = '{name}\\{name}_dem.flt\n{mode}\n{type}\n'.format(name=name,
        mode='2', # 2 = ArcGrid
        type=''  # blank for binary
        )
    lines = ['{name}\\{name}_sinks.pnt',
    '{name}\\{name}_large_residuals.pnt',
    '{name}\\{name}_stream_errors.pnt',
    '{name}\\{name}_polygon_errors.pnt',
    '{name}\\{name}_contour_errors.pnt',
    '{name}\\{name}_derived_streams.lin',
    '{name}\\{name}_derived_breaks.lin',
    '{name}\\{name}_grid_point_codes.asc',
    '{name}\\{name}_grid_flow.asc',
    '{name}\\{name}_grid_aspect.flt']

    with open(cmdfile, 'at') as f:
        f.write('\n')
        f.write(dem)
        f.write('\n'.join(x.format(name=name) for x in lines))
    f.close()

def show_file(fname):
    '''Display file with line numbers.'''
    with open(fname, 'rt') as f:
        print '\n--- {} ---'.format(fname)
        count = 0
        for row in f.readlines():
            count += 1
            print '{:>3}: {}'.format(count, row),
                #trailing comma strips extra newline
        print '\n------'

def write_lines(cmdfile, lines):
    with open(cmdfile, 'wt') as f:
        f.write('\n'.join(str(x) for x in lines))
    f.close()

def usage():
    print "\nbuild-anudem-args [source path] [cell-size] [extent-layer] {file1.gen file2.gen ...}\n"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    path = sys.argv[1]
    a.cellsize = int(sys.argv[2])
    extent_layer = sys.argv[3]

    in_gen_files = get_file_names(path, '*.gen')

    if len(sys.argv) >= 5:
        print "--- Adding to default .gen files:", sys.argv[4]
        in_gen_files = list(set(in_gen_files + sys.argv[4:]))
            # merge and remove dupes, http://stackoverflow.com/a/15219904/14420

##    path = r'D:\p\ytdemv3\work_105mn'
##    path = r'D:\p\ytdemv3\bugs\Anudem_2015-05-08'
##    a.cellsize = 20
##    extent_layer = 'selection_buffer_3000m'
##    extent_layer = 'extent_105m12'

    os.chdir(path)

    gdb = os.path.join(path, 'clipped.gdb')

    outdir = 'dem_{}m'.format(a.cellsize)
    cmdfile = 'dem_{}m.anu'.format(a.cellsize)

    # build full path for input files
    in_gen_files = [os.path.join(path, x) for x in in_gen_files]

    s = calc_anu_extent(a.cellsize, get_ogr_extent(extent_layer, gdb=gdb))
    a.x_limits = '%s, %s' % (s[0], s[1])
    a.y_limits = '%s, %s' % (s[2], s[3])


    # Remember, item order is critical!
    # Part 1
    part1_lines = [a.enforce, a.datatype, a.rms_vse, a.roughness, a.tolerances,
    a.iterations, a.z_units, a.z_min_max, a.centering, a.xy_units, a.x_limits,
    a.y_limits, a.cellsize, a.margin]
    write_lines(cmdfile, part1_lines)

    # Part 2, input data
    data_files = parse_data_types(in_gen_files)
    a.num_files = len(data_files)
    write_data_files(cmdfile, data_files)

    # Part 3, output and diagnostics
    write_diag_parms(cmdfile, outdir, a.cellsize)

    show_file(cmdfile)
