# updates a set of fishnet grids with the relevant tilref
# field set by the osgbutils tools.
# this script requires ArcGIS for the arcpy module

import arcpy
import osgbutils
import math

fc100km = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_100km'
fc10km = r''
fc5km = r''
fc1km = r''
fc500m = r''
fc100m = r''
fields = ['SHAPE@XY','tileref']
with arcpy.da.UpdateCursor(fc100km, fields) as cursor:
    for row in cursor:
        row[1] = osgbutils.gridSquare(int(row[0][0]),int(row[0][1]),100)

        cursor.updateRow(row)