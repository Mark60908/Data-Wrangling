import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from Data import *

#OSMFILE = "edmonton_sample1.osm"
OSMFILE = "edmonton_canada.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
#street_type_re = re.compile('^[A-Za-z_.-]+$', re.IGNORECASE)
postcode_type_re = re.compile(r'^[A-Z]\d[A-Z] \d[A-Z]\d$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard",  "Drive",  "Court", "Square", "Lane", "Road", 
            "Trail", "Parkway",  "Highway", "Freeway", "Southeast","Place", "Southwest",
            "South", 'Northwest', "North", "Northeast", "Way"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "NW": "Northwest",
            "North-West": "Northwest",
            "North-West": "Northwest",
            "NE": "Northeast",
            "North-west": "Northwest",
            "North-East": "Northeast",
            "SW": "Southwest",
            "South-west": "Southwest",
            "South-West": "Southwest",
            "SE": "Southeast",
            "South-east": "Southeast",
            "South-East": "Southeast",
            "Villa": "Village",
            "Villas": "Village"}


def audit_street_type(street_types, street_name):

    ''''''
    
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem): # Check if it is a street name
    return (elem.attrib['k'] == "addr:street")



def audit(osmfile):
    
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types
   
    

def get_types():
    
    ''' get street types in the osm data'''
    
    types = []
    for element in audit(OSMFILE):
        #pattern = re.compile('^[A-Za-z_.-]+$', re.IGNORECASE)
        pattern = re.compile(r'\b\S+\.?$', re.IGNORECASE)
        if pattern.search(element):
            types.append(element)
    
    return types




def update_name(name, mapping):
    
     m = street_type_re.search(name)
     if m :
         new_name = []
         for word in name.split():
             if word in mapping:
                 word = mapping[word]
             new_name.append(word)
             name = ' '.join(new_name)
     return name





postcodes = []
for element in get_element(OSMFILE, tags=('node', 'way')):
    for child in element:
        if child.tag == 'tag':
            if child.attrib['k'] == 'addr:postcode':
                postcodes.append(child.attrib['v'])
print set(postcodes)


def update_postcode(postcode):
    
  
  if  postcode_type_re.search(postcode):
          newpostcode = postcode
  else:
         
      if len(postcode) == 6 or len(postcode)== 3 :
              newpostcode = postcode[0:3] + ' ' + postcode[3:]
      elif len(postcode) == 7:
              newpostcode = postcode[0:3] + ' ' + postcode[4:]
      elif len(postcode) > 13:
              newpostcode = postcode[:7]
      elif len(postcode) == 11:
              newpostcode = postcode[9:]
      elif len(postcode) == 9:
              newpostcode = postcode[4:7] + ' ' + postcode[7:]
      elif len(postcode) == 8:
              newpostcode = postcode[0:8]
      elif len(postcode) == 5:
              newpostcode = None
      else:
             pass
          
  return newpostcode
          














    
    

if __name__ == '__main__':
    
    #updated_name = update_name(get_types(), mapping)
    #print  updated_name
    #print  get_types()
    print update_postcode(postcodes)













