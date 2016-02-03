#!/usr/bin/env python
#coding=utf-8
import MySQLdb, sys, json

host = 'localhost'
user = 'djangodev'
password = 'djangodev'
dbname = 'djangodev'
charset = 'utf8'


def findHost(alias):
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    cursor.execute('select a.var_name,a.var_value from inventory_var a where a.host_id = (select id from inventory_host b where b.ansible_alias = \''+alias+'\')')
    data = cursor.fetchall()
    data = dict(data)
    dbconn.close()
    print json.dumps(data, sort_keys=True, indent=2)


def findAll():
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    sql = 'select ansible_alias from inventory_host'
    cursor.execute(sql)
    hostdata = cursor.fetchall()
    hostdata = [x[0] for x in hostdata]
    resultdata = {}
    for alias in hostdata:
        cursor.execute('select a.var_name,a.var_value from inventory_var a where a.host_id = (select id from inventory_host b where b.ansible_alias = \''+alias+'\')')
        data = cursor.fetchall()
        data = dict(data)
        resultdata[alias+'group'] = {'hosts':[alias],'vars':data}
    dbconn.close()
    print json.dumps(resultdata, sort_keys=True, indent=2)

args = sys.argv
if len(args) > 2 and args[1] == '--host':
    findHost(args[2])
if len(args) > 1 and args[1] == '--list':
    findAll()
