import psycopg2 as dbapi2
import sys
import os
import time



def getall(q):
        rs = {}
        cur.execute(q);
        rows = cur.fetchall()
        for k,v in enumerate(rows):
                rs[v[0]] = v[1]
        return rs

db = dbapi2.connect ("host='10.5.203.176' dbname='jira' user='gpadmin' password=
'EmcWorld2011'")
cur = db.cursor()

rs = getall('select * from qa_ana.prepared_data')

for i in rs:
	f = open(i,'w')
	
	f.write(rs[i])
	f.close()
	print 'write jira:'+i 
	time.sleep(5)

