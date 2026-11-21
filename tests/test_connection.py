from database.connection import create_connection
db=None
cursor=None
try :
    db  =create_connection() 
    if(db.is_connected()):
        print("Connection successfull")
        cursor=db.cursor()
        query="select * from users"
        cursor.execute(query)
        rows = cursor.fetchall()
        print("Number of users:", len(rows))
except Exception as e: 
    print("Connection failed : ",e)
finally:
    if cursor:
        cursor.close()
    if db:
        db.close()
    print("cursor and database connection closed")
