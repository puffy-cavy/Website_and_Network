import MySQLdb as mdb
from bottle import FormsDict
from hashlib import md5
from os import path

f = open("../dbrw.secret")
ps = f.read()
f.close()

ps = ps.rstrip()
# connection to database project2
def connect():
    """makes a connection to MySQL database.
    @return a mysqldb connection
    """

    #TODO: fill out function parameters. Use the user/password combo for the user you created in 2.1.2.1

    return mdb.connect(host="localhost",
                       user="zzhu39",
                       passwd=ps,
                       db="project2");

def createUser(username, password):
    """ creates a row in table named users
    @param username: username of user
    @param password: password of user
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query creates a row in table user
    insert_state = ("INSERT INTO project2.users (username, password, passwordhash) VALUES (%s, %s, %s)")
    user_data = (username, password, md5(password.encode()))
    cur.execute(insert_state, user_data)
    db_rw.commit()

def validateUser(username, password):
    """ validates if username,password pair provided by user is correct or not
    @param username: username of user
    @param password: password of user
    @return True if validation was successful, False otherwise.
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects a row from table user
    fetch_state = ("SELECT * FROM  project2.users WHERE username = %s AND password = %s")
    fetch_data = (username, password)
    cur.execute(fetch_state, fetch_data)
    if cur.rowcount < 1:
        return False
    return True

def fetchUser(username):
    """ checks if there exists given username in table users or not
    if user exists return (id, username) pair
    if user does not exist return None
    @param username: the username of a user
    @return The row which has username is equal to provided input
    """

    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    print username
    #TODO: Implement a prepared statement so that this query selects a id and username of the row which has column username = username
    fetch_user_state = ("SELECT id, username FROM project2.users WHERE username = %s")
    fetch_user_data = (username)
    cur.execute(fetch_user_state, fetch_user_data)
    if cur.rowcount < 1:
        return None
    return FormsDict(cur.fetchone())

def addHistory(user_id, query):
    """ adds a query from user with id=user_id into table named history
    @param user_id: integer id of user
    @param query: the query user has given as input
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statment using cur.execute() so that this query inserts a row in table history
    add_state = ("INSERT INTO project2.history (user_id, query) VALUES(%s, %s)")
    add_data = (user_id, query)
    cur.execute(add_state, add_data)
    db_rw.commit()

#grabs last 15 queries made by user with id=user_id from table named history
def getHistory(user_id):
    """ grabs last 15 distinct queries made by user with id=user_id from
    table named history
    @param user_id: integer id of user
    @return a first column of a row which MUST be query
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects 15 distinct queries from table history
    hist_state = ("SELECT query FROM project2.history WHERE id = %s LIMIT 15")
    cur.execute(hist_state, user_id)
    rows = cur.fetchall();
    return [row[0] for row in rows]
