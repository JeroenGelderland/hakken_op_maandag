import mysql.connector

class Database:

    def __init__(self):
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        db="moodplaats"
        )

        self.cur = self.db.cursor()


    def query(self, query):
        self.cur.execute(query)
        raw = self.cur.fetchall()
        result = []
        for row in raw:
            obj = {}

            for i, field in enumerate(row):
                obj[self.cur.description[i][0]] = field
            
            result.append(obj)
        
        return result

    def execute(self, command):

        if(isinstance(command, list)):
            for query in command:
                self.cur.execute(command)

        else:
            self.cur.execute(command)
        
        self.db.commit()

