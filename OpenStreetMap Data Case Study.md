# OpenStreetMap Data Case Study

------

By: Mark Lin

## Map Area
Edmonton AB Canada
[OpenStreetMap](https://www.openstreetmap.org/search?query=edmonton#map=10/53.5562/-113.4926)
[Metro Extract Edmonton](https://mapzen.com/data/metro-extracts/metro/edmonton_canada/)
![Edmonton][1]

------
# Problems Encountered in the Map

```python
def get_types():
    types = []
    for element in audit(OSMFILE):
        pattern = re.compile('^[A-Za-z_.-]+$', re.IGNORECASE)
        if pattern.search(element):
            types.append(element)
    return types
```
After printing out the street types in this city, I found two main problems in the data, which I would discuss in the follow.

> **Street Name**:

>* Abbreviations 
>* Inconsistent Names

> **Postcode:**
> ######Inconsistent format
>* Lowercase and uppercase
>* Missing a space or using line in between
>* Incomplete postcode or Incorrect format




## Abbreviations problem
There is some overabbreviated directions in the data, such as, "NE" and "SW", which represent Northeast and Southwest.

## Inconsistency problem
Some places or street names have different expressions, for example, both "Villa" and "Villas" are standing for "Village". 

To fix the two problems, I use the update_name function to map the old names with the preffered name.
``` python
def update_name(name, mapping):
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
        else:
            pass
    return name
```


  
## Lowercase and uppercase
Most of the letters are in uppercase, however, a small proportion has used lowercase, such as this one. 
```
t6e 2g9

```
## Missing a space or using line in between
This is the main problem of this type of data, many postcodes are missing a space, or using some other symbol instead of space. 

``` 
T7Z1V5
T6W0W8
T5C3C8
T5J-1J4
```


## Incomplete postcode or Incorrect format
There is a few postcodes are incomplete or in a wrong format, examples are given below.
```
Alberta T6G
AB T5J
AB T6E4S6
T8N 3V4,
85027
```

The fisrt piece of code, ``newpostcode = postcode[0:3] + ' ' + postcode[3:]``, we insert a space into the postcode, and keep the postcode that has only half proportion. ``` newpostcode = postcode[0:3] + ' ' + postcode[4:]``` replace the middle symplol, for example, dash line '-' to a space. The rest of the code are using to clean several indivisual case, there are only couple unique postcodes in the data, for instance, ``` T6E 4R9 Commute to Downtown Edmonton   4 min  24 min  8 min  30 min View Routes Check Availability Favorite Map Nearby Apartments ``` or ``` T6A 2E9 Phone: (780) 969-8496```.
```
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
```

------
# Data Overview
## File sizes
>edmonton_canada.osm -------- 783 MB
>edmonton.db -------------------- 583MB
> nodes.csv -------------------------311MB
> node_tags.csv --------------------21.1MB
> ways.csv---------------------------28.2MB
way_tags.csv ---------------------32.3MB
way_nodes.csv --------------------102MB

## Number of nodes
``` sqlite
sqlite> SELECT COUNT(*) FROM nodes;
```
11309016

## Number of ways
``` sqlite
sqlite> SELECT COUNT(*) FROM ways
```
1439451
## Number of unique users
``` sqlite
sqlite> SELECT COUNT(DISTINCT(a.uid)) 
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) AS a 
```
823

## Top 10 contributing users
``` sqlite
sqlite> SELECT a.user,  COUNT(*) AS num 
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) AS a
GROUP BY a.user
ORDER BY num DESC
LIMIT 10
```

| user   | posts   |  
| ------   | -----:  | 
| edmontongeo      | 7160385 |  
| charrois        |  2637003   | 
| Sundance         |    431403    |  
|xixi           |366006|
|Mesowhite         |323628|
|alester       | 238683|
|geobase_stevens   | 213660| 
|VE6SRV |  189177| 
|Viajero Perdido| 90411|
|yegbin| 77688|

# Additional Ideas
## Users' contributing statistics

Total contributing in the data, 
``` sqlite
sqlite> SELECT  SUM(a.user) as num 
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) AS a'
```
23260488 

>* The top one contribution percentage 30.78%
>* The top ten contribution percentage 50.42%

The top ten contributors only take 50% of all the works, which is good, since we want the contributors to be diversified so that the data would be more acurate and bias free.

## Additional data exploration
* Top 10 appearing amenities
``` sqlite
sqlite>  SELECT value,  COUNT(*) AS num 
         FROM node_tags
         WHERE key = "amenity"
         GROUP BY value
         ORDER BY num DESC
         LIMIT 10
```
```python
restaurant                   999
fast_food                    993
place_of_worship             819
cafe                         477
fuel                         450
bench                        396
bank                         243
parking                      228
pharmacy                     201
toilets                      156)
```

* Most popular cuisines
``` sqlite
SELECT node_tags.value ,COUNT(*) AS num
FROM node_tags
    JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value =                    "restaurant") AS a
    ON node_tags.id = a.id
WHERE node_tags.key = "cuisine"
GROUP BY node_tags.value
ORDER BY num DESC
LIMIT 5
```
|cuisine|number|
| ------   | -----:  | 
|chinese | 72 |
|pizza | 48|
|vietnamese| 48|
|american| 39|
|italian| 33|


* Most popular sport
``` sqlite
sqlite> SELECT node_tags.value ,COUNT(*) AS num\
         FROM node_tags\
         WHERE node_tags.key = "sport"\
         GROUP BY node_tags.value\
         ORDER BY num DESC
         LIMIT 5
```
```python
soccer              33
baseball            24
hockey              21
swimming            18
yoga                15
```
------

# Conclusion
The OpenStreetMap data of Edmonton has surprisingly high quality. There is only a few human typo and inconsistencies in the data set, probably machines such as GPS contributed a lot to the data set. However, the information is incomplete and old,  it could be improved by containing more detailed information, for example, the ratings of a restaurant.   

## Improving suggestion and idea 
* preseting a data schema for inputing data. This would be a good way to avoid human typo and create a consistent data in terms of data format. However, this might create complexity for the algorithm and reducing the efficiency. 
* Using third party tools like goolge map API to provide more information. By doing this, it would enrich the dataset, however, google map itself has some unclean data as well.
* Inducing more users to help. The top 10 contributors made more than 50% of the data. If more users are engaged in this program, the dataset will be more complete and helpful. The con is it might need more effort to get more users involved, maybe financially. 
* Cleaning the data periodically. This method is eficient in terms of cost, however, since it does not update the data timely, users might get inaccurate data.  

 


  [1]: http://www.brookfieldresidential.com/_Global/71/img/content/Edmonton_AB_Map_Website_400x700---No-Stars.jpg