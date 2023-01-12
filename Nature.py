"""Provides a scripting component.
    Inputs:
        osm: from osm file.
    Output:
        green: outputs the key:leisure breps.
        """

__author__ = "zoeyzhao"

import rhinoscriptsyntax as rs
import xml.etree.ElementTree as ET
import ghpythonlib.treehelpers as th
import random
import math
import os
import Rhino 

####
# TODO: extract meta data and output in list.
####
 

R = 6367000 # radius of earth in meters

def latlon2xy(lat, lon, dx, dy, min_lat, min_lon):
    x = (lon - min_lon) * dx
    y = (lat - min_lat) * dy
    return x, y

def coord2pt(coord):
    return Rhino.Geometry.Point3d(coord[0], coord[1], 0)

def pts2srf(pts):
    if len(pts) <= 2: 
        return None # Can only build surface from at least 3 pts.
    if pts[0] != pts[-1]: # close pts if not done already 
        pts.append(pts[0])
    crv = rs.AddPolyline(pts)
    if rs.ClosedCurveOrientation(crv) == -1:
        rs.ReverseCurve(crv)
    return rs.AddPlanarSrf(crv)[0]
    
def srfdiff(isrfs, osrfs):
    if len(isrfs) == 0 and len(osrfs) == 1:
        return osrfs[0]
    elif len(isrfs) == 1 and len(osrfs) == 0:
        return isrfs[0]
    elif len(isrfs) > 1 and len(osrfs) == 0:
        return rs.BooleanUnion(isrfs)[0]
    elif len(isrfs) == 0 and len(osrfs) > 1:
        return rs.BooleanUnion(osrfs)[0]
    elif len(isrfs) > 0 and len(osrfs) > 0:
        return rs.BooleanDifference(osrfs, isrfs)[0]
    elif len(isrfs) == 0 and len(osrfs) == 0:
        return None

tree = ET.parse(osm)
root = tree.getroot()

# 1. Find area min/max lat/lon bounds
bounds = root.find("bounds")
min_lat, max_lat = float(bounds.attrib['minlat']), float(bounds.attrib['maxlat'])
min_lon, max_lon = float(bounds.attrib['minlon']), float(bounds.attrib['maxlon'])

# 2. Find lat/lon area extension
delta_lat = max_lat - min_lat
delta_lon = max_lon - min_lon

# 3. Convert from lat/lon to Cartesian space (x,y)
mid_lat = min_lat + delta_lat / 2
dy = math.pi / 180 * R
dx = dy * math.cos( math.radians( mid_lat ) )

# 4. Find all lat/lon coordinates and convert to x,y
node_coord_dict = dict()
for node_tag in root.findall("node"):
    node_id = node_tag.attrib['id']
    lat = float(node_tag.attrib['lat'])
    lon = float(node_tag.attrib['lon'])
    x,y = latlon2xy(lat, lon, dx, dy, min_lat, min_lon)
    node_coord_dict[node_id] = (x,y)

def pts_from_way(way):
    pts = []
    for nd in way.findall("nd"):
        node_id = nd.attrib['ref']
        coord = node_coord_dict[node_id]
        pt = coord2pt(coord)
        pts.append(pt)
    return pts
    
# Things to keep track of 
green = []

# 5. Parse relations, create brep, track
for relation in root.findall('relation'):
    if relation.find("tag[@k='leisure']") is not None:
        isrfs, osrfs = [], []

        for member in relation.findall("member[@type='way']"):
            way_id, role = member.attrib['ref'], member.attrib['role']
            way = root.find("way[@id='%s']" % way_id)
            if way:
                pts = pts_from_way(way)
                srf = pts2srf(pts)
                if srf:
                    if role == 'inner' or role == 'part': 
                        isrfs.append(srf)
                    if role == 'outer' or role == 'outline': 
                        osrfs.append(srf)
        
        brep = srfdiff(isrfs,osrfs)
        green.append(brep)
 
# process all ways
for way in root.findall('way'):
    if way.find("tag[@k='leisure']") is not None:

        pts = pts_from_way(way)
        brep = pts2srf(pts)
        green.append(brep)

green = th.list_to_tree(green)
