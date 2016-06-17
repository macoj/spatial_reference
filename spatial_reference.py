__author__ = 'marcos'
import re
import urllib2
from osgeo import osr
from osgeo import ogr
from nominatim import Nominatim


class SpatialReference:
    meter_to_feet = 0.3048
    feet_to_meter = 1/meter_to_feet

    def __init__(self):
        pass

    @staticmethod
    def guess_the_projection(points, state=None, spatial_reference_query=None, city=None, conversion=None):
        epsgs_hits = []
        if spatial_reference_query is None:
            spatial_reference_query = state
        epsgs = SpatialReference.epsg_search(spatial_reference_query)
        y_min, y_max, x_min, x_max = Nominatim.nominatim_get_bounding_box_of(state=state, city=city)
        for epsg in epsgs:
            epsg_hit = 0
            for p in points:
                try:
                    x, y = SpatialReference.convert_spatial_reference(p[0], p[1], epsg[0], 4326, conversion=conversion)
                except:
                    print "Could not find EPSG:'%s'" % epsg[0]
                    break
                # print x, x_min, x_max
                if y_min < y < y_max and x_min < x < x_max:
                    epsg_hit += 1
            epsgs_hits.append((epsg[0], epsg_hit))
        epsgs_hits.sort(key=lambda x: x[1], reverse=True)
        return epsgs_hits
    """
    execfile("spatial_reference.py")
    points = [(7647409.02929, 686790.02595000004), (7647471.0159499999, 688344.44999999995),  (7645653.23905, 684826.79570999998), (7645656.2857100004, 684567.37809999997)]
    epsgs = SpatialReference.guess_the_projection(points, state="Oregon")
    for epsg, hits in epsgs[:5]:
        print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
    points = [(2514332.03903053, 7018364.6881987797), (2503623.9508441598, 6974201.6616298398), (2499328.3021238302, 6939465.4717225898), (2499328.3021238302, 6939465.4717225898), (2499328.3021238302, 6939465.4717225898)]
    epsgs = SpatialReference.guess_the_projection(points, state="Texas")
    for epsg, hits in epsgs[:5]:
        print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
    points = [(894672.5, 995003.69999999995), (900456.30000000005, 1017035.0), (900456.30000000005, 1017035.0), (882164.59999999998, 999102.19999999995), (891889.30000000005, 1034635.0), (898334.0, 1022420.0), (894343.0, 1005425.0), (893510.30000000005, 1033772.0), (883747.80000000005, 1004093.0), (877404.59999999998, 1027557.0)]
    epsgs = SpatialReference.guess_the_projection(points, state="Missouri", city="St. Louis", conversion=SpatialReference.meter_to_feet)
    for epsg, hits in epsgs[:5]:
        print "[EPSG:%d] %.0f%% hit" % (epsg, float(hits)/len(points)*100.0)
    """

    @staticmethod
    def epsg_search(query, page=None):
        results = []
        page_str = ""
        if page is not None:
            page_str = "&page=%d" % page
        query = re.sub(" ", "+", query)
        spatial_reference_url = "http://spatialreference.org/ref/epsg/?search=%s&srtext=Search%s" % (query, page_str)
        query_result = SpatialReference.load_url_content(spatial_reference_url)
        epsgs = re.findall('<li><a href="/ref/epsg/[0-9]*/">[A-Za-z\/\:\>\< 0-9\(\)]*</li>', query_result)
        for epsg_html in epsgs:
            epsg = re.search("/ref/epsg/[0-9]*", epsg_html).group()
            epsg = int(epsg[10:])
            description = re.search(": [A-Za-z/:>< 0-9]*", epsg_html).group()[2:-5]
            results.append((epsg, description))
        if re.search("Next Page", query_result):
            if page is None:
                page = 0
            page += 1
            results += SpatialReference.epsg_search(query, page)
        return results
    """
execfile("spatial_reference.py")
SpatialReference.epsg_search("Missouri")
SpatialReference.epsg_search("Texas")
    """

    @staticmethod
    def load_url_content(url):
        opener = urllib2.urlopen
        request = urllib2.Request
        req = request(url)
        handle = opener(req)
        content = handle.read()
        load_content = content
        return load_content

    @staticmethod
    def convert_spatial_reference(point_longitude, point_latitude, source, target, conversion=None):
        if conversion:
            point_latitude *= conversion
            point_longitude *= conversion
        source_reference = osr.SpatialReference()
        source_reference.ImportFromEPSG(source)
        target_reference = osr.SpatialReference()
        target_reference.ImportFromEPSG(target)
        point_transform = osr.CoordinateTransformation(source_reference, target_reference)
        transformed_point = ogr.CreateGeometryFromWkt("POINT (%f %f)" % (point_longitude, point_latitude))
        transformed_point.Transform(point_transform)
        return transformed_point.GetX(), transformed_point.GetY()
    """
    execfile("spatial_reference.py")
    point_latitude = 686790.02595000004
    point_longitude = 7647409.02929
    SpatialReference.convert_spatial_reference(point_longitude, point_latitude, 2269, 4326)
    point_latitude = 1028833.0
    point_longitude = 888708.3
    SpatialReference.convert_spatial_reference(point_longitude, point_latitude, 2815, 4326, conversion=SpatialReference.meter_to_feet)
    """