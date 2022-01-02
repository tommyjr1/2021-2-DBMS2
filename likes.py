from connect import *


def unlike(show_id):
    mydb = connect()
    myCursor = mydb.cursor()
    sqlString = f""" 
        DELETE from table_like
        WHERE show_id='{show_id}';
        """
    myCursor.execute(sqlString)
    mydb.commit()
    mydb.close()


def like(show_id, likeBtn):
    mydb = connect()
    myCursor = mydb.cursor()
    try:
        sqlString = f""" 
        INSERT INTO table_like(show_id,`like`) VALUES ('{show_id}',1);
        """
        myCursor.execute(sqlString)
        mydb.commit()
    except:
        sqlString = f""" 
        DELETE from table_like
        WHERE show_id='{show_id}';
        """
        myCursor.execute(sqlString)
        mydb.commit()
    mydb.close()
    getlike(show_id, likeBtn)


def getlike(show_id, likeBtn):
    mydb = connect()
    myCursor = mydb.cursor()
    sqlString = f""" 
    SELECT `like`
    FROM table_like
    WHERE show_id = '{show_id}';
    """

    myCursor.execute(sqlString)
    status = myCursor.fetchall()
    mydb.close()

    print(status)
    try:
        if status[0][0] == 1:
            likeBtn.config(bg='#ff0000')
        else:
            likeBtn.config(bg='#ffffff')
    except:
        likeBtn.config(bg='#ffffff')
    