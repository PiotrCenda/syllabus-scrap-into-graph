from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


def connect():
    conn = Neo4jConnection(uri="bolt://localhost:7687", user="admin", pwd="admin")
    

def query(search_input:str, connection:Neo4jConnection):
    query_input = """MATCH (a)-[r]-(b) 
WHERE toLower(a.name) CONTAINS toLower('{}')
RETURN a, r, b, labels(a), TYPE(r), labels(b)""".format(search_input)
    query = connection.query(query_input)
    return query


if __name__ == '__main__':
    query('al', Neo4jConnection(uri="bolt://localhost:7687", user="admin", pwd="admin"))