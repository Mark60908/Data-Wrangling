import csv
import sqlite3

con = sqlite3.connect("edmonton.db")
cur = con.cursor()


def number_of_nodes():
    nodes = cur.execute('SELECT COUNT(*) FROM nodes')
    return nodes.fetchone()[0]


def number_of_ways():
    ways = cur.execute('SELECT COUNT(*) FROM ways')
    return ways.fetchone()[0]


def number_of_unique_users():
    users = cur.execute('SELECT COUNT(DISTINCT(a.uid))\
            FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) AS a')
    return users.fetchone()[0]


def Top_10_contributing_users():
    Top_10_users = []
    for user in cur.execute('SELECT a.user,  COUNT(*) AS num \
         FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) AS a\
         GROUP BY a.user\
         ORDER BY num DESC\
         LIMIT 10'):
        Top_10_users.append(user)
        
    return Top_10_users
    

def number_of_tags():
    #tags = []
    for tag in cur.execute('SELECT DISTINCT(key) FROM node_tags'):
        print tag
     #   tags.append(tag)
    #return tags


def contributings():
    users = []
    s =  cur.execute('SELECT  SUM(a.user) as num \
         FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) AS a')
        
    return s.fetchone()[0]


def top_10_appearing_amenities():
    amenities = []
    for amenity in cur.execute('SELECT value,  COUNT(*) AS num \
         FROM node_tags\
         WHERE key = "amenity"\
         GROUP BY value\
         ORDER BY num DESC\
         LIMIT 10'):
         amenities.append(amenity)
    return amenities
  

def most_popular_cuisines():
    cuisines = []
    for cuisine in cur.execute('SELECT node_tags.value ,COUNT(*) AS num\
         FROM node_tags\
              JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value = "restaurant") AS a\
              ON node_tags.id = a.id\
         WHERE node_tags.key = "cuisine"\
         GROUP BY node_tags.value\
         ORDER BY num DESC'):
         cuisines.append(cuisine)
    return cuisines


def most_popular_sport():
    sports = []
    for sport in cur.execute('SELECT node_tags.value ,COUNT(*) AS num\
         FROM node_tags\
         WHERE node_tags.key = "sport"\
         GROUP BY node_tags.value\
         ORDER BY num DESC'):
         sports.append(sport)
    return sports



#print 'number of nodes:', number_of_nodes()
#print 'number of ways:', number_of_ways()
#print 'number of unique users :' , number_of_unique_users()
#print 'Top 10 contributing users:' , Top_10_contributing_users()
#print 'number of tags:',
#number_of_tags() 
#print contributings()
#print top_10_appearing_amenities()
#print most_popular_cuisines()
print most_popular_sport()








