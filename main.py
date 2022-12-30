import sqlite3
import os


cwd = os.getcwd()
# Print the current working directory
print("Current working directory: {0}".format(cwd))



def sql_identifier(s):
    return '"' + s.replace('"', '""') + '"'

# table dict = {table_name: [# has_foreign_key, # being_ref]}
# to init = {table_name: [0, 0]}
def initTableDict(tables):
    dict = {}
    for table in tables:
        dict.update({table: [0, 0]})
    return dict

def getTableDict(tables, table_dict, cur):
    for table in tables:
        # print("table: " + table)
        # rows = cur.execute("PRAGMA table_info({})".format(sql_identifier(table)))
        # print(rows.fetchall())
        rows = cur.execute("PRAGMA foreign_key_list({})".format(sql_identifier(table)))
        foreign_list = rows.fetchall()
        if len(foreign_list) != 0:
            table_dict[table][0] = len(foreign_list)
            for item in foreign_list:
                ref_table_name = item[2]
                table_dict[ref_table_name][1] = table_dict[ref_table_name][1] + 1
    return table_dict

def getDBStatistics(table_dict, name):
    statistics = []
    sort_by_fk = sorted(table_dict.items(), key = lambda x: x[1][0], reverse=True)
    sort_by_ref = sorted(table_dict.items(), key = lambda x: x[1][1], reverse=True)
    #print(sort_by_ref)

    statistics.append(name)
    statistics.append(len(table_dict))
    statistics.append(sort_by_fk[0][1][0])
    statistics.append(sort_by_ref[0][1][1])
    #print(statistics)

    return statistics

def getForeignKeys(name):
    path = 'spider/database/{0}/{1}.sqlite'.format(name, name)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    rows = cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = [row[0] for row in rows]
    #print(tables)

    table_dict = initTableDict(tables)
    table_dict = getTableDict(tables, table_dict, cur)

    #print(table_dict)
    cur.close()
    return getDBStatistics(table_dict, name)


name_list = os.listdir('spider/database/')
sta_list = []
for name in name_list:
    if name[0] != '.':
        sta_list.append(getForeignKeys(name))

#1: number of table; 2: max number of fk; 3: max number of ref
sta_list = sorted(sta_list, key = lambda x: x[2], reverse=True)
print(len(sta_list))
print(sta_list)

# cur.execute("select sql from sqlite_master")
# for r in cur.fetchall():
#     if r[0] != None:
#         print(r[0])
# cur.close()