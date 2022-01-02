from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from connect import *
from likes import *
from comments import *

### detail page ###

def detail(index, show_ids):
    global show_id
    show_id=show_ids[index]

    def getInfo():
        mydb = connect()
        myCursor = mydb.cursor()

        # Bring info
        global table, show_type
        table = ''
        show_type = ''
        try:
            sqlString = f""" 
            SELECT *
            FROM table_movie
            WHERE show_id='{show_id}';
            """

            myCursor.execute(sqlString)
            myResultList = myCursor.fetchall()
            myResult = myResultList[0]

            table = 'table_movie'
            show_type = 'Movie'
        except:
            sqlString = f""" 
            SELECT *
            FROM table_tv
            WHERE show_id='{show_id}';
            """

            myCursor.execute(sqlString)
            myResultList = myCursor.fetchall()
            myResult = myResultList[0]

            table = 'table_tv'
            show_type = 'TV Show'

        try:
            title = myResult[2]
            date_added = myResult[3]
            release_year = myResult[4]
            rating = myResult[5]
            duration = myResult[6]
            description = myResult[7]
        except:
            print('Missing')

        # Bring all casts
        sqlString = f""" 
        SELECT cast
        FROM table_cast
        WHERE show_id='{show_id}';
        """
        myCursor.execute(sqlString)
        myResultCast = myCursor.fetchall()

        casts = []
        if (len(myResultCast) != 0):

            for cast in myResultCast:
                casts.append(cast[0])
        else:
            casts.append('No information updated')

        # Bring all directors
        sqlString = f""" 
        SELECT director
        FROM table_director
        WHERE show_id='{show_id}';
        """
        myCursor.execute(sqlString)
        myResultDi = myCursor.fetchall()

        directors = []
        if (len(myResultDi) != 0):

            for di in myResultDi:
                directors.append(di[0])
        else:
            directors.append('No information updated')

        # Bring all country
        sqlString = f""" 
        SELECT country
        FROM table_country
        WHERE show_id='{show_id}';
        """
        myCursor.execute(sqlString)
        myResultCountry = myCursor.fetchall()

        countries = []
        if (len(myResultCountry) != 0):

            for c in myResultCountry:
                countries.append(c[0])
        else:
            countries.append('No information updated')

        # Bring all genre
        sqlString = f""" 
        SELECT genre
        FROM table_genre
        WHERE show_id='{show_id}';
        """
        myCursor.execute(sqlString)
        myResultGenre = myCursor.fetchall()

        genres = []
        if (len(myResultGenre) != 0):

            for c in myResultGenre:
                genres.append(c[0])
        else:
            genres.append('No information updated')

        mydb.close()

        return title, date_added, release_year, rating, duration, description, casts, directors, countries, genres

    global window_d
    window_d = Tk()
    window_d.title('Show Detail')
    window_d.geometry('800x600')
    addframe = Frame(window_d, bg="black")
    addframe.place(relwidth=0.3, relheight=0.1, relx=0.7, rely=0.9)

    movieframe = Frame(window_d, bg="#60b8eb")
    movieframe.place(relwidth=.7, relheight=.9, relx=0, rely=0)

    btnframe = Frame(window_d, bg="#60b8eb")
    btnframe.place(relwidth=.7, relheight=.1, relx=0, rely=.9)

    addcomFrame = Frame(window_d, bg="#000000")
    addcomFrame.place(relwidth=.3, relheight=.3, relx=.7, rely=0)

    commentframe = Frame(window_d, bg="#000000")
    commentframe.place(relwidth=.3, relheight=.6, relx=0.7, rely=.3)
    commentgridframe = Frame(commentframe, bg="#000000")
    commentgridframe.place(relx=.5, rely=0, anchor=N)

    expandframe = Frame(movieframe, bg="#60b8eb")
    expandframe.pack(fill=BOTH, expand=1)

    details = Canvas(expandframe, bg="#60b8eb")
    details.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar = ttk.Scrollbar(expandframe, command=details.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    details.configure(yscrollcommand=scrollbar.set)
    details.bind('<Configure>', lambda e: details.configure(scrollregion=details.bbox("all")))

    infos = Frame(details, bg="#60b8eb")
    details.create_window((0, 0), window=infos, anchor=NW)

    global result, columns
    result = getInfo()
    columns = ["title", "date_added", "release_year", "rating", "duration", "description", "casts", "directors",
                "countries", "genres"
                ]

    def showresult(result):
        for i in infos.winfo_children():
            i.destroy()
        for i in columns:
            Label(infos, text=i, bg="#60b8eb").grid(row=columns.index(i), column=0)
            Label(infos, text=str(result[columns.index(i)]), bg="#60b8eb",wraplength=300).grid(row=columns.index(i), column=1,padx=3,pady=3, ipady=10)

    
    showresult(result)
    bringComment(show_id, commentgridframe)
    likeBtn = Button(btnframe, text='Like')
    likeBtn.pack(side=LEFT, anchor=S)

    def remove():
        global window_r
        window_r = Tk()
        window_r.title('Delete show')
        window_r.geometry('300x200')

        frame = Frame(window_r, bg="black")
        frame.pack(side = LEFT, fill = BOTH, expand = 1)

        label = Label(frame, text='Do you want to really delete this movie?',fg="white",bg="black",anchor=CENTER)
        label.grid(row=0, column=0, columnspan=2)
        yesBtn = Button(frame, text='Yes', bg="#60b8eb")
        yesBtn.grid(row=1, column=0)
        noBtn = Button(frame, text='No', bg="#60b8eb")
        noBtn.grid(row=1, column=1)

        def yes():
            mydb = connect()
            myCursor = mydb.cursor()
            tables = [table, 'table_cast', 'table_director', 'table_country', 'table_genre', 'table_comment', 'table_comment', 'table_like']

            for i in tables:
                sqlString = f""" 
                DELETE FROM {i}
                WHERE show_id='{show_id}';
                """
                myCursor.execute(sqlString)
                mydb.commit()
            mydb.close()

            messagebox.showinfo("", "Show deleted!")
            window_r.destroy()
            window_d.destroy()

        def no():
            window_r.destroy()

        yesBtn.config(command=yes)
        noBtn.config(command=no)

        window_r.mainloop()

    def edit():
        global window_e
        window_e = Tk()
        window_e.title('Edit show')
        window_e.geometry('700x500')
        frame = Frame(window_e,bg="black")
        frame.pack(side = LEFT, fill = BOTH, expand = 1)

        for i in columns:
            Label(frame, text=i, fg="white",bg="black").grid(row=columns.index(i), column=0)
            e = Entry(frame, width=70, bg="white")
            e.insert(END, str(result[columns.index(i)]))
            e.grid(row=columns.index(i), column=1, padx=3, pady=5, ipady=7)

        saveBtn = Button(frame, text='Save change')
        saveBtn.grid(row=10, column=1, sticky='e', )

        def editSave():
            for i in range(10):
                if frame.winfo_children()[2*i +3 ].get()=="" or frame.winfo_children()[2*i +3 ].get()=="['']":
                    messagebox.showinfo("Error",'Write the '+frame.winfo_children()[2*(i+1)]["text"] +' of the show.')
                    return
            mydb = connect()
            myCursor = mydb.cursor()
            tables = [table, 'table_cast', 'table_director', 'table_country', 'table_genre']

            for i in tables:
                sqlString = f""" 
                DELETE FROM {i}
                WHERE show_id='{show_id}';
                """
                myCursor.execute(sqlString)
                mydb.commit()

            entrylist = []
            for i in range(10):
                entrylist.append(frame.winfo_children()[2 * i + 1].get())
                if i == 6:
                    # cast
                    string = entrylist[i][1:-1]
                    listt = string.split(',')

                    for cast in listt:
                        myCursor.execute(f"INSERT INTO table_cast(show_id, cast) VALUES('{show_id}',{cast})")
                        mydb.commit()
                if i == 7:
                    string = entrylist[i][1:-1]
                    listt = string.split(',')

                    for director in listt:
                        myCursor.execute(
                            f"INSERT INTO table_director(show_id, director) VALUES('{show_id}',{director})")
                        mydb.commit()
                if i == 8:
                    string = entrylist[i][1:-1]
                    listt = string.split(',')

                    for country in listt:
                        myCursor.execute(
                            f"INSERT INTO table_country(show_id, country) VALUES('{show_id}',{country})")
                        mydb.commit()
                if i == 9:
                    string = entrylist[i][1:-1]
                    listt = string.split(',')

                    for genre in listt:
                        myCursor.execute(f"INSERT INTO table_genre(show_id, genre) VALUES('{show_id}',{genre})")
                        mydb.commit()
                if i == 5:
                    sqlString = f'INSERT INTO {table}(show_id, type, title, date_added, release_year, rating, duration, description) VALUES("{show_id}","{option.get()}","{entrylist[0]}","{entrylist[1]}","{entrylist[2]}","{entrylist[3]}","{entrylist[4]}","{entrylist[5]}")'
                    myCursor.execute(sqlString)
                    mydb.commit()
            mydb.close()
            messagebox.showinfo("", "Show edited!")
            window_e.destroy()
            global result
            result = getInfo()
            showresult(result)

        saveBtn.config(command=editSave)

        window_e.mainloop()

    

    getlike(show_id, likeBtn)
    
    likeBtn.config(command=lambda :like(show_id, likeBtn))

    editBtn = Button(btnframe, text='Edit')
    editBtn.pack(side=RIGHT, anchor=S)
    editBtn.config(command=edit)

    removeBtn = Button(btnframe, text='Delete')
    removeBtn.pack(side=RIGHT, anchor=S)
    removeBtn.config(command=remove)

    def addComment():
        if entry.get() =="":
            messagebox.showinfo("Error",'Write comment.')
            return
        mydb = connect()
        myCursor = mydb.cursor()
        try:
            sqlString = f""" 
            INSERT INTO table_comment(show_id,`comment`, `date`) VALUES ('{show_id}',"{entry.get()}", NOW());
            """

            myCursor.execute(sqlString)
            mydb.commit()
            mydb.close()
            bringComment(show_id, commentgridframe)
            entry.delete(0,END)
            entry.insert(0, '')
        except:
            messagebox.showwarning('Error', 'Write shorter comment.')
            mydb.close()

        

    entry = Entry(addcomFrame)
    entry.place(relx=0.1, rely=0.25, relwidth=.8, relheight=.25)

    addBtn = Button(addcomFrame, text='Comment')
    addBtn.place(relx=.5, rely=.7, relwidth=.4)
    addBtn.config(command=addComment)
    window_d.mainloop()