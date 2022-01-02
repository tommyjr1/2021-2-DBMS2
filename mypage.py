from sys import exit
import mysql.connector
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from connect import *
# import tkinter as tk



# Loading Mypage
def open_mypage():
    conn = connect()
    c = conn.cursor()
    query1 = '''SELECT m.title AS TITLE FROM table_like l
    JOIN table_movie m ON m.show_id = l.show_id
    UNION SELECT t.title AS TITLE FROM table_like l
    JOIN table_tv t ON t.show_id = l.show_id'''
    query2 = '''SELECT m.title AS Title, c.comment as Comment, c.date as Date FROM table_comment c
    JOIN table_movie m ON m.show_id = c.show_id
    UNION SELECT t.title AS Title, c.comment as Comment, c.date as Date FROM table_comment c
    JOIN table_tv t ON t.show_id = c.show_id
    ORDER BY Date DESC'''

    top = Toplevel()
    top.geometry("1920x1080")
    top_frame = Frame(top, bg="#ffd129")
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    label = Label(top_frame, text="My page", fg='black', bg="#ffd129")
    label['font'] = font.Font(family='NanumBarunGothic', size=18, weight='bold')
    label.place(relx=0.3, rely=0.3, relwidth=0.4)
    # add_frame = Frame(top,bg="#ffd129" )
    # add_frame.place(relx=0, rely=0.3, relwidth=0.05, relheight=0.7)


    like = Frame(top, bg="#ffd129")
    like.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.8)
    expandframe3 = Frame(like, bg="#ffd129")
    expandframe3.pack(fill=BOTH, expand=1)

    details3 = Canvas(expandframe3, bg="#ffd129")
    details3.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar3 = ttk.Scrollbar(expandframe3, command=details3.yview)
    scrollbar3.pack(side=RIGHT, fill=Y)

    details3.configure(yscrollcommand=scrollbar3.set)
    details3.bind('<Configure>', lambda e: details3.configure(scrollregion=details3.bbox("all")))

    like_frame = Frame(details3, bg="#ffd129")
    details3.create_window((0, 0), window=like_frame, anchor=NW)


    comment= Frame(top, bg="#ffd129")
    comment.place(relx=0.5, rely=0.2, relwidth=0.6, relheight=0.8)
    expandframe2 = Frame(comment, bg="#ffd129")
    expandframe2.pack(fill=BOTH, expand=1)

    details2 = Canvas(expandframe2, bg="#ffd129")
    details2.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar2 = ttk.Scrollbar(expandframe2, command=details2.yview)
    scrollbar2.pack(side=RIGHT, fill=Y)

    details2.configure(yscrollcommand=scrollbar2.set)
    details2.bind('<Configure>', lambda e: details2.configure(scrollregion=details2.bbox("all")))

    comment_frame = Frame(details2, bg="#ffd129")
    details2.create_window((0, 0), window=comment_frame, anchor=NW)


    c.execute(query1)
    result1 = c.fetchall()

    fontbold= font.Font(family='NanumBarunGothic', size=16, weight="bold")
    fontnormal= font.Font(family='NanumBarunGothic', size=12)


    for i in range(len(result1)):
        for res in result1[i]:
            blank = Label(like_frame, text="", bg="#ffd129",width=40)
            blank.grid(column=0, row=0)
            res_label1 = Label(like_frame, text=res, fg="black", bg="#ffd129")
            col_label1 = Label(like_frame, text="Like", fg="black", bg="#ffd129")
            col_label1.grid(row=1, column=1, ipadx=3, ipady=1)
            blank2 = Label(like_frame, text="", bg="#ffd129")
            blank2.grid(column=1, row=2)
            res_label1.grid(row=i + 3, column=1, ipadx=3, ipady=1)
            col_label1.configure(font=fontbold)
            res_label1.configure(font=fontnormal)

    c.execute(query2)
    result2 = c.fetchall()
    columns = c.column_names
    for i in range(len(columns)):
        blank = Label(comment_frame, text="", bg="#ffd129",width=10)
        blank.grid(column=0, row=0)
        res_label = Label(comment_frame, text=columns[i], fg="black", bg="#ffd129")
        res_label.grid(row=1, column=i+1, ipadx=3, ipady=1)
        res_label.configure(font=fontbold)
        blank2 = Label(comment_frame, text="", bg="#ffd129")
        blank2.grid(column=i+1, row=2)
    for j in range(len(result2)):
        for i in range(len(result2[j])):
            res_label2 = Label(comment_frame, text=result2[j][i], fg="black", bg="#ffd129")
            res_label2.grid(row=j + 3, column=i+1, ipadx=3, ipady=1)
            res_label2.configure(font=fontnormal)

    conn.close()