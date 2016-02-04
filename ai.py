#!/usr/bin/env python
# coding=utf-8
import MySQLdb
import sys
import json


# Mysqldb variables.
host = 'localhost'
user = 'djangodev'
password = 'djangodev'
dbname = 'djangodev'
charset = 'utf8'

# Defined the sqls would be used.
allhostsql = 'select ansible_alias from inventory_host'
findhostvarsql = 'select a.var_name,a.var_value from inventory_hostvar a where a.host_id = (select id from inventory_host b where b.ansible_alias = %s)'


def findHost(alias):
    '''
    When script is invoked with '--host <hostname>',
    return the host's variable json or Null.
    '''
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    cursor.execute(findhostvarsql, [alias])
    data = cursor.fetchall()
    data = dict(data)
    dbconn.close()
    print json.dumps(data, sort_keys=True, indent=2)


def findAll():
    '''
    When script is invoked with '--list',
    return all groups, hosts, variables json.
    '''
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    cursor.execute(allhostsql)
    hostdata = cursor.fetchall()
    hostdata = [x[0] for x in hostdata]
    resultdata = {}
    allhostvardata = {}
    allhostdata = {'hosts': hostdata}
    # the 'all' element.
    resultdata['all'] = allhostdata
    for alias in hostdata:
        cursor.execute(findhostvarsql, [alias])
        data = cursor.fetchall()
        data = dict(data)
        allhostvardata[alias] = data
    # for ansible 1.3 or higher, add the top element '_meta' for all hostvars.
    resultdata['_meta'] = {'hostvars': allhostvardata}
    dbconn.close()
    print json.dumps(resultdata, sort_keys=True, indent=2)

args = sys.argv
if len(args) > 2 and args[1] == '--host':
    findHost(args[2])
if len(args) > 1 and args[1] == '--list':
    findAll()
