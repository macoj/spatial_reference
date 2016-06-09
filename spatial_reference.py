__author__ = 'marcos'
import re
import urllib2


class SpatialReference:
    def __init__(self):
        pass

    @staticmethod
    def epsg_search(query, page=None):
        results = []
        page_str = ""
        if page is not None:
            page_str = "&page=%d" % page
        query = re.sub(" ", "+", query)
        spatial_reference_url = "http://spatialreference.org/ref/epsg/?search=%s&srtext=Search%s" % (query, page_str)
        query_result = SpatialReference.load_url_content(spatial_reference_url)
        epsgs = re.findall('<li><a href="/ref/epsg/[0-9]*/">[A-Za-z\/\:\>\< 0-9]*</li>', query_result)
        for epsg_html in epsgs:
            epsg = re.search("/ref/epsg/[0-9]*", epsg_html).group()
            epsg = epsg[10:]
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
SpatialReference.epsg_search("Florida West")

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
