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
allhostsql = 'select id,ansible_alias from inventory_host'
findhostvarsql = 'select a.var_name,a.var_value from inventory_hostvar a where a.host_id = %s'
allgroupsql = 'select id,ansible_group from inventory_group'
findgroupvarsql = 'select a.var_name,a.var_value from inventory_groupvar a where a.group_id  = %s'
findgrouphostssql = 'select a.host_id from inventory_group_ansible_hosts a where a.group_id = %s'
findgroupchildrensql = 'select a.to_group_id from inventory_group_ansible_children a where a.from_group_id = %s'


def findHost(alias):
    '''
    When script is invoked with '--host <hostname>',
    return the host's variable json or Null.
    '''
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    cursor.execute(findhostvarsql, [alias])
    vardata = cursor.fetchall()
    vardata = dict(vardata)
    dbconn.close()
    print json.dumps(data, indent=2)


def findAll():
    '''
    When script is invoked with '--list',
    return all groups, hosts, variables json.
    '''
    dbconn = MySQLdb.Connect(host=host, user=user, passwd=password, db=dbname, charset=charset)
    cursor = dbconn.cursor()
    cursor.execute(allhostsql)
    hostdata = cursor.fetchall()
    hostids = [x[0] for x in hostdata]
    hosts = [x[1] for x in hostdata]
    hostdata = dict(hostdata)
    result = {}
    allhostvar = {}
    allhostdata = {'hosts': hosts}
    # the 'all' element contains every host alias.
    result['all'] = allhostdata
    for i in range(0, len(hostids)):
        cursor.execute(findhostvarsql, [hostids[i]])
        vardata = cursor.fetchall()
        vardata = dict(vardata)
        allhostvar[hosts[i]] = vardata
    # for ansible 1.3 or higher, add the top element '_meta' for all hostvars.
    result['_meta'] = {'hostvars': allhostvar}
    # group elements
    # prepare datas
    cursor.execute(allgroupsql)
    groupdata = cursor.fetchall()
    groupids = [x[0] for x in groupdata]
    groups = [x[1] for x in groupdata]
    groupdata = dict(groupdata)
    for i in range(0, len(groupids)):
        # vars in group
        cursor.execute(findgroupvarsql, [groupids[i]])
        vardata = cursor.fetchall()
        vars = dict(vardata)
        # hosts in group
        cursor.execute(findgrouphostssql, [groupids[i]])
        hostsiddata = cursor.fetchall()
        hosts = [hostdata[x[0]] for x in hostsiddata]
        # children in group
        cursor.execute(findgroupchildrensql, [groupids[i]])
        groupchildreniddata = cursor.fetchall()
        groupchildren = [groupdata[x[0]] for x in groupchildreniddata]
        if len(vars) == 0 and len(groupchildren) == 0:
            if len(hosts) > 0:
                result[groups[i]] = hosts
            else:
                continue
        else:
            thisgroupdata = {}
            if len(hosts) > 0:
                thisgroupdata['hosts'] = hosts
            if len(vars) > 0:
                thisgroupdata['vars'] = vars
            if len(groupchildren) > 0:
                thisgroupdata['children'] = groupchildren
            result[groups[i]] = thisgroupdata
    dbconn.close()
    print json.dumps(result, indent=2)

args = sys.argv
if len(args) > 2 and args[1] == '--host':
    findHost(args[2])
if len(args) > 1 and args[1] == '--list':
    findAll()
