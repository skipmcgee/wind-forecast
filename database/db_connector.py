# Citation for the following function: execute_query()
# Date: 05/25/2024
# Based on a StackOverflow solution provided by user "powdahound"
# I modified the class based StackOverflow solution to work with the existing execute_query() function provided by the Flask App Starter Code
# Source URL: https://stackoverflow.com/questions/207981/how-to-enable-mysql-client-auto-re-connect-with-mysqldb/982873#982873

# Date Accessed: 20240430
# Referenced and used: https://github.com/osu-cs340-ecampus/flask-starter-app/
import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv


# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

def connect_to_database(host=host, user=user, passwd=passwd, db=db):
    """
    connects to a database and returns a database objects
    """
    db_connection = MySQLdb.connect(host, user, passwd, db)
    return db_connection


def execute_query(db_connection=None, query=None, query_params=()):
    """
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query

    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.

    """

    if db_connection is None:
        print(
            "No connection to the database found! Have you called connect_to_database() first?"
        )
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    # Modified the class based version to fit within the existing functions

    # Try to execute query
    try:
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, query_params)
        db_connection.commit()

    # if connection has timed out then reconnect before executing the query
    except (AttributeError, MySQLdb.OperationalError):
        db_connection = connect_to_database(host=host, user=user, passwd=passwd, db=db)
        cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, query_params)
        db_connection.commit()

    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    # cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    # params = tuple()
    # create a tuple of paramters to send with the query
    # for q in query_params:
    #    params = params + (q)

    # TODO: Sanitize the query before executing it!!!
    # cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    # db_connection.commit()
    return cursor


if __name__ == "__main__":
    print("Executing a sample query on the database")
    db = connect_to_database()
    db2 = DBConnector()
    query = "SELECT * from sensors;"
    results1 = execute_query(db, query)
    sensorID = 1
    query = f"SELECT * from sensors WHERE sensorID = {sensorID};"
    results2 = db2._execute_query(query)
    print(f"Printing results of {query}")

    for r in results1.fetchall():
        print(r)
    print("######")
    for r in results2.fetchall():
        print(r)
