from connect import *
from tkinter import *

def bringComment(show_id, commentgridframe):
    for widget in commentgridframe.winfo_children():
        widget.destroy()
    mydb = connect()
    myCursor = mydb.cursor()

    sqlString = f""" 
    SELECT `comment`, `date`, show_id
    FROM table_comment
    WHERE show_id='{show_id}'
    ORDER BY `date`;
    """
    myCursor.execute(sqlString)
    myResult = myCursor.fetchall()

    mydb.close()

    show_ids=[]
    comments=[]

    for i in myResult:
        Label(commentgridframe, text=i[0], bg="#60b8eb").grid(row=myResult.index(i), column=0 ,sticky=NSEW)
        Label(commentgridframe, text=i[1], bg="#60b8eb").grid(row=myResult.index(i), column=1, padx=3, sticky=NSEW)
        show_ids.append(i[2])
        comments.append(i[0])
    
    for i, r in enumerate(myResult):
        deleteBtn = Button(commentgridframe, text='Del')
        deleteBtn.grid(row=i, column=2)
        deleteBtn.config(command=lambda e=i:delete(show_ids[e], comments[e],commentgridframe))

def delete(show_id, comment,commentgridframe):
    query=f'''
    DELETE from table_comment
    WHERE show_id='{show_id}' and `comment` LIKE '%{comment}%';
    '''
    mydb = connect()
    myCursor = mydb.cursor()
    myCursor.execute(query)
    mydb.commit()
    mydb.close()

    bringComment(show_id, commentgridframe)
    return

def delete_my(show_id, comment):
    query=f'''
    DELETE from table_comment
    WHERE show_id='{show_id}' and `comment` LIKE '%{comment}%';
    '''
    mydb = connect()
    myCursor = mydb.cursor()
    myCursor.execute(query)
    mydb.commit()
    mydb.close()
    return

