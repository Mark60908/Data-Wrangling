import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    mytags = {}
    for event, child in ET.iterparse(filename):
        if child.tag in mytags:
            mytags[child.tag] += 1
        else:
             mytags[child.tag] = 1
    return mytags

print count_tags("edmonton_sample.osm")
