import sqlite3
import os

name_list = os.listdir('spider/database/')

def getSchema(name):
    path = 'spider/database/{0}/{1}.sqlite'.format(name, name)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    cursor.close()

# for name in name_list:
#     if name[0] != '.':
#         print(name)

print(len(name_list))
getSchema("voter_1")