import sqlite3
import os
import json

name_list = os.listdir('spider/database/')

def initDBs():
    name_list = os.listdir('spider/database/')
    for name in name_list:
        if name[0] != '.':
            db_path = 'spider/database/{0}/{1}.sqlite'.format(name, name)
            db_schema = 'spider/database/{0}/{1}'.format(name, 'schema.sql')
            if os.path.exists(db_schema):
                print(name)
                with open(db_schema, 'r') as sql:
                    script = sql.read()
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.executescript(script)
                print(cursor.fetchall())
                conn.commit()
                conn.close()




    # path = 'spider/database/{0}/{1}.sqlite'.format(name, name)
    # conn = sqlite3.connect(path)
    # cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall())
    # cursor.close()



def processJsonInput():
    path = 'spider/dev.json'
    with open(path, 'r') as f:
        data = json.load(f)
    for record in data:
        db = record['db_id']
        query = record['query']
        db_path = 'spider/database/{0}/{1}.sqlite'.format(db, db)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        print(cursor.fetchall())
        conn.commit()
        conn.close()


# initDBs()
processJsonInput()

# for name in name_list:
#     if name[0] != '.':
#         print(name)

# print(len(name_list))
# getSchema("voter_1")