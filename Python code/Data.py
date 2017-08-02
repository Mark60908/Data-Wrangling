import csv
import codecs
import re
import xml.etree.cElementTree as ET
import schema
import cerberus
import pprint
from audit import *

OSM_PATH = "edmonton_canada.osm"
SAMPLE_PATH = "edmonton_sample.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "node_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "way_nodes.csv"
WAY_TAGS_PATH = "way_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type="regular"):
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []

    if element.tag == 'node':
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]

        for node_tag in element:
            node_tags = {}
            if LOWER_COLON.match(node_tag.attrib['k']):
                node_tags['type'] = node_tag.attrib['k'].split(':',1)[0]
                node_tags['key'] = node_tag.attrib['k'].split(':',1)[1]
                node_tags['value'] = node_tag.attrib['v']
                node_tags['id'] = element.attrib['id']
                if node_tag.attrib['k'] == 'addr:street':
                   # print node_tag.attrib['v']
                    node_tags['value'] = update_name(node_tag.attrib['v'], mapping)
                    #node_tags['value'] 
                else:
                    node_tags['value'] = node_tag.attrib['v']

                
                if node_tag.attrib['k'] == 'addr:postcode':
                    #print node_tag.attrib['v']
                    node_tags['value'] = update_postcode(node_tag.attrib['v'])
                
                
                tags.append(node_tags)
                
            elif PROBLEMCHARS.match(node_tag.attrib['k']):
                continue
            else:
                node_tags['type'] = 'regular'
                node_tags['id'] = element.attrib['id']
                node_tags['key'] = node_tag.attrib['k'] 
                node_tags['value'] = node_tag.attrib['v']
                tags.append(node_tags)
                
        
        return {'node': node_attribs, 'node_tags': tags}


    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]

        position = 0        
        for child in element:
            way_node = {}
            way_tag = {}

            if  child.tag == 'tag':
                if LOWER_COLON.match(child.attrib['k']):
                   way_tag['id'] = element.attrib['id']
                   way_tag['type'] = child.attrib['k'].split(':',1)[0]
                   way_tag['key'] = child.attrib['k'].split(':',1)[1]
                   way_tag['value'] = child.attrib['v']
                   if child.attrib['k'] == 'addr:street':
                       #print child.attrib['v']
                       way_tag['value'] = update_name(child.attrib['v'], mapping)
                       #print way_tag['value']
                   else:
                       way_tag['value'] = child.attrib['v']
                   tags.append(way_tag)

                   if child.attrib['k'] == 'addr:postcode':
                    way_tag['value'] = update_postcode(node_tag.attrib['v'])

                   
                elif PROBLEMCHARS.match(child.attrib['k']):
                       continue

                else:
                        way_tag['type'] = 'regular'
                        way_tag['id'] = element.attrib['id']
                        way_tag['key'] = child.attrib['k']
                        way_tag['value'] = child.attrib['v']
                        tags.append(way_tag)

            elif  child.tag == 'nd':
                  way_node['id'] = element.attrib['id']
                  way_node['node_id'] = child.attrib['ref']
                  way_node['position'] = position
                  position += 1
                  way_nodes.append(way_node)
                
        

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def get_element(osm_file, tags=('node', 'way', 'relation')):

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)




















       
