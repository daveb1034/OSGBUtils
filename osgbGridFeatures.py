# updates a set of fishnet grids with the relevant tilref
# field set by the osgbutils tools.
# this script requires ArcGIS for the arcpy module

import arcpy
import osgbutils
import math

fc100km = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_100km'
fc10km = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_10km'
fc5km = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_5km'
fc1km = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_1km'
fc500m = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_500m'
fc100m = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_100m'
fc10m = r'C:\Users\daveb\Documents\ArcGIS\Projects\OSGB\Default.gdb\osgb_10m_su'
fcs = [[fc100km,100],[fc10km,10],[fc5km,5],[fc1km,1],[fc500m,0.5],[fc100m,0.1]]
fields = ['SHAPE@XY','tileref']
# for fc in fcs:
#     with arcpy.da.UpdateCursor(fc[0], fields) as cursor:
#         for row in cursor:
#             row[1] = osgbutils.gridSquare(int(row[0][0]),int(row[0][1]),fc[1])
#             print(row[1])
#             cursor.updateRow(row)
with arcpy.da.UpdateCursor(fc10m, fields) as cursor:
    for row in cursor:
        row[1] = osgbutils.gridSquare(int(row[0][0]),int(row[0][1]),0.01)
        print(row[1])
        cursor.updateRow(row)