import csv
import sqlite3

con = sqlite3.connect("edmonton.db")
con.text_factory = str
cur = con.cursor()


cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp)")
with open ('nodes.csv', 'rb') as table1:
    data1 = csv.DictReader(table1)
    to_db1 = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])\
             for i in data1]
cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp)\
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_db1)
con.commit()

cur.execute("CREATE TABLE way_tags (id, key, value, type);")
with open('way_tags.csv','rb') as table5:
    data5 = csv.DictReader(table5) 
    to_db5 = [(i['id'], i['key'], i['value'], i['type']) for i in data5]

cur.executemany("INSERT INTO way_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db5)
con.commit()


cur.execute("CREATE TABLE node_tags (id, key, value, type)")
with open('node_tags.csv', 'rb') as table2:
    data2 = csv.DictReader(table2)
    to_db2 = [(i['id'], i['key'], i['value'], i['type']) for i in data2]
cur.executemany("INSERT INTO node_tags (id, key, value, type) \
                VALUES (?, ?, ?, ?)", to_db2)
con.commit()



cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp)")
with open('ways.csv', 'rb') as table3:
     data3 = csv.DictReader(table3)
     to_db3 = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in data3]
cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) \
                VALUES (?, ?, ?, ?, ?, ?)", to_db3)
con.commit()



cur.execute("CREATE TABLE way_nodes (id, node_id, position)")
with open('way_nodes.csv') as table4:
    data4 = csv.DictReader(table4)
    to_db4 = [(i['id'], i['node_id'], i['position']) for i in data4]
cur.executemany("INSERT INTO way_nodes (id, node_id, position) \
                 VALUES (?, ?, ?)", to_db4)
con.commit()


