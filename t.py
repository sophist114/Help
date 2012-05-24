import nltk
import re
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
import psycopg2 as dbapi2
import sys
import os
import time
from stemming.porter2 import stem

path = '/home/gpadmin/sophist/test/'
db = dbapi2.connect ("host='10.5.203.176' dbname='jira' user='gpadmin' password='EmcWorld2011'")
cur = db.cursor()

def getall(q):
	rs = {}
	cur.execute(q);
	rows = cur.fetchall()
	for k,v in enumerate(rows):
		rs[v[0]] = v[1]
	return rs
def getfirstone(q):
	rs = {}
        cur.execute(q);
        rows = cur.fetchall()
	return rows

def combine(o):
	rs = " ".join(str (x) for x in o);
	return rs; 

config = getall('select key,replacement from qa_ana.config')
#print config

r = getfirstone('select dict from qa_ana.dictionary')
if not r:
	dict = []
else:
	dict = r[0][0]
l = os.listdir(path)
jiras = {} 
for file in l:
	temp = open(path+file,'r').read()
	temp = re.sub(r'(\w)\1{3,}', r'\1', temp)	
	temp = re.sub('\n',' ',temp)
	temp = re.sub('(0x\w+)',' ',temp)
	temp = re.sub('(\d+)',' ',temp)
	temp = re.sub(r'[^\w]',' ',temp)	
	
	temp = re.sub('(\s+\w{0,4}\s+)',' ',temp) 
	jira_id = re.sub('MPP-','',file)
	jiras[jira_id]=temp


for ji in jiras:
	jira = jiras[ji]
	for i in config:
		jira = re.sub('('+i+')',config[i],jira)
		#print config[i]

	#replace block of code
	jira = re.sub('(<\w+(.*)</\w+>)', '',jira)

	jira = re.sub("'","",jira)
	bad = stopwords.words('english');

	all = wordpunct_tokenize(jira);
	all = [i.lower() for i in all]
	all = [stem(i) for i in all]
	
#	print all
#	time.sleep(3)
	temp = all
	good = []
	
	for v in temp:
			if bad.__contains__(v):
					print 'removed : '+v
			else:
					good.append(v)
	result=[]
	for w in good:
		if(w in dict):
			result.append(dict.index(w))
		else:
			dict.append(w)
			result.append(dict.index(w))		
#	print result
	
	rs = ','.join(str(k) for k in result)
	rs='{'+rs+'}'
	cur.execute('insert into qa_ana.corpus values (null,\'MPP-'+ji+'\',\''+rs+'\')')
	print 'insert jira '+ji

print dict
cur.execute('truncate table qa_ana.dictionary')
cur.execute('insert into qa_ana.dictionary values(array'+str(dict)+')')
db.commit()

