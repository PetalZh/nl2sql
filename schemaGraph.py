import sqlite3
import os

class SchemaGraph:
    def __init__(self, db_name):
        self.db_name = db_name
        self.cur = self._getDBConnection(db_name)

    def _getDBConnection(self, db_name):
        path = 'spider/database/{0}/{1}.sqlite'.format(db_name, db_name)
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        return cur

    def __sql_identifier(self, s):
        return '"' + s.replace('"', '""') + '"'

    def getGraph(self):
        tables = self.getTableFromDB()
        # Use a dictionary to represent the graph
        # {table_name: {'to': [(ref_table_name, table.column_name), ...]
        #               'from': [ref_by_table_name, ...]}
        #   ...
        # }

        graph_dict = {}

        # init the dictionary with vertices
        for table in tables:
            graph_dict.update({table: {'to':[], 'from':[]}})

        # add edges
        for table in tables:
            fk_list = self.__getFK(table)
            for fk in fk_list:
                to = fk[2]
                column_name = fk[3]

                graph_dict[table]['to'].append((to, column_name))
                graph_dict[to]['from'].append(table)
        # print(graph_dict)
        return graph_dict


    def getTableFromDB(self):
        # path = 'spider/database/{0}/{1}.sqlite'.format(self.db_name, self.db_name)
        # conn = sqlite3.connect(path)
        # cur = conn.cursor()
        rows = self.cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = [row[0] for row in rows]

        return tables

    def __getFK(self, table):
        rows = self.cur.execute("PRAGMA foreign_key_list({})".format(self.__sql_identifier(table)))
        fk_list = rows.fetchall()
        # print(table + ": ", fk_list)
        return fk_list


# def getDbNameList(self):
#     db_list = os.listdir('spider/database/')
#     db_list.remove('.DS_Store')
#     # print(db_list)
#     return db_list

# graph = SchemaGraph('student_transcripts_tracking')
# graph.getGraph()


# db_list = getDbNameList()
# getTableFromDB(db_list)