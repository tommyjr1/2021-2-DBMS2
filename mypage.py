from sys import exit
import mysql.connector
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from connect import *

from likes import *
from comments import *

# Loading Mypage
def open_mypage():
    top = Toplevel()
    top.geometry("1920x1080")
    top_frame = Frame(top, bg="#ffd129")
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    label = Label(top_frame, text="My page", fg='black', bg="#ffd129")
    label['font'] = font.Font(family='NanumBarunGothic', size=18, weight='bold')
    label.place(relx=0.3, rely=0.3, relwidth=0.4)

    add_frame = Frame(top,bg="#ffd129" )
    add_frame.place(relx=0, rely=0.3, relwidth=0.05, relheight=0.7)
    freshBtn = Button(top_frame, text="새로고침")
    freshBtn['font'] = font.Font(family="Arial", size=10)
    freshBtn.pack(side='right', anchor=S)


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


    def destroy_display():
        for widget in like_frame.winfo_children():
            widget.destroy()
        for widget in comment_frame.winfo_children():
            widget.destroy()


    def get_mydata():
        destroy_display()

        conn = connect()
        c = conn.cursor()
        query1 = '''SELECT l.show_id AS ID, m.title AS TITLE 
        FROM table_like l
        JOIN table_movie m ON m.show_id = l.show_id
        UNION 
        SELECT l.show_id AS ID, t.title AS TITLE 
        FROM table_like l
        JOIN table_tv t ON t.show_id = l.show_id'''

        query2 = '''SELECT m.title AS TITLE, c.comment as COMMENT, c.date as Date, m.show_id as DEL
        FROM table_comment c
        JOIN table_movie m ON m.show_id = c.show_id
        UNION SELECT t.title AS TITLE, c.comment as COMMENT, c.date as Date, t.show_id as DEL
        FROM table_comment c
        JOIN table_tv t ON t.show_id = c.show_id'''

        #좋아요 영화들
        c.execute(query1)
        result1 = c.fetchall()
        c.execute(query2)
        result2 = c.fetchall()
        conn.close()


        fontbold= font.Font(family='NanumBarunGothic', size=16, weight="bold")
        fontnormal= font.Font(family='NanumBarunGothic', size=12)


        col_label1 = Label(like_frame, text="Like", fg="black", bg="#ffd129")
        col_label1.grid(row=1, column=1, ipadx=3, ipady=1)
        col_label1.configure(font=fontbold)
        blank = Label(like_frame, text="", bg="#ffd129",width=40)
        blank.grid(column=0, row=0)
        blank2 = Label(like_frame, text="", bg="#ffd129")
        blank2.grid(column=1, row=2)

        show_ids_like=[]
        for res in result1:
            show_ids_like.append(res[0])
        for ind, res in enumerate(result1):
            res_label1 = Button(like_frame, text=res[1], fg="black", bg="#ffd129")
            res_label1.grid(row=result1.index(res)+3, column=1,ipadx=3, ipady=1)
            res_label1.config(command=lambda e=ind:unlike(show_ids_like[e]))
            res_label1.configure(font=fontnormal)



        #댓글

        columns = c.column_names

        show_ids_com=[]
        comments=[]
        blank = Label(comment_frame, text="", bg="#ffd129",width=10)
        blank.grid(column=0, row=0)
        for i in range(len(columns)):
            res_label = Label(comment_frame, text=columns[i], fg='black', bg="#ffd129")
            res_label.grid(row=1, column=i+1, ipadx=3, ipady=1)
            res_label.configure(font=fontbold)
            blank2 = Label(comment_frame, text="", bg="#ffd129")
            blank2.grid(column=i+1, row=2)

        for j in range(len(result2)):
            for i in range(3):
                res_label2 = Label(comment_frame, text=result2[j][i], fg="black", bg="#ffd129")
                res_label2.grid(row=j + 3, column=i+1, ipadx=3, ipady=1)
                res_label2.configure(font=fontnormal)   
            show_ids_com.append(result2[j][3])
            comments.append(result2[j][1])
        print(comments)
        for ind, com in enumerate(result2):
            deleteBtn = Button(comment_frame, text='Del')
            deleteBtn.grid(row=ind+3, column=4)
            deleteBtn.config(command=lambda e=ind:delete_my(show_ids_com[e], comments[e]))

            

    get_mydata()
    freshBtn.config(command=get_mydata)
