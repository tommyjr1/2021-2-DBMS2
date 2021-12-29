from sys import exit
import mysql.connector
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from tkinter import *


# Have to change password
def connect():
    global mydb
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='__________',
            database='teamproject')
        return mydb
        
    except:
        messagebox.showwarning('DB not connected', 'Your code is not connected to the database. Change the password in main_page1.py')
        return

# Loading Mypage
def open_mypage():
    conn = connect()
    c = conn.cursor()
    query1 = '''SELECT m.title AS TITLE FROM table_like l
    JOIN table_movie m ON m.show_id = l.show_id
    UNION SELECT t.title AS TITLE FROM table_like l
    JOIN table_tv t ON t.show_id = l.show_id'''
    query2 = '''SELECT m.title AS TITLE, c.comment as COMMENT, c.date as Date FROM table_comment c
    JOIN table_movie m ON m.show_id = c.show_id
    UNION SELECT t.title AS TITLE, c.comment as COMMENT, c.date as Date FROM table_comment c
    JOIN table_tv t ON t.show_id = c.show_id'''

    top = Toplevel()
    top.geometry("700x500")
    top_frame = Frame(top, bg="#ffd129")
    top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.3)
    label = Label(top_frame, text="My page")
    label['font'] = font.Font(family="Arial", size=15)
    label.place(relx=0.3, rely=0.3, relwidth=0.4)
    add_frame = Frame(top,bg="#ffd129" )
    add_frame.place(relx=0, rely=0.3, relwidth=0.05, relheight=0.7)


    like = Frame(top, bg="#ffd129")
    like.place(relx=0.05, rely=0.3, relwidth=0.35, relheight=0.7)
    expandframe3 = Frame(like, bg="#60b8eb")
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
    comment.place(relx=0.4, rely=0.3, relwidth=0.6, relheight=0.7)
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
    for i in range(len(result1)):
        for res in result1[i]:
            res_label1 = Label(like_frame, text=res, fg="white", bg="black")
            col_label1 = Label(like_frame, text="LIKE", bg="#ffd129")
            col_label1.grid(row=0, column=0)
            res_label1.grid(row=i + 1, column=0)

    c.execute(query2)
    result2 = c.fetchall()
    columns = c.column_names
    for i in range(len(columns)):
        res_label = Label(comment_frame, text=columns[i], bg="#ffd129")
        res_label.grid(row=0, column=i)
    for j in range(len(result2)):
        for i in range(len(result2[j])):
            res_label2 = Label(comment_frame, text=result2[j][i], fg="white", bg="#60b8eb")
            res_label2.grid(row=j + 1, column=i)
    conn.close()

# Loading Search
def view():

    #### GUI ####
    window = Tk()
    window.title("Search shows")
    window.geometry("1280x720")

    frame1 = Frame(window, bg="#60b8eb")
    frame1.place(relx=0, rely=0, relwidth=0.24, relheight=1)

    frame2 = Frame(window)
    frame2.place(relx=0.24, rely=0, relwidth=0.76, relheight=1)

    mid_frame2 = Frame(frame2)
    mid_frame2.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(mid_frame2, bg="black")
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = Scrollbar(mid_frame2, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    scrollable_frame = Frame(my_canvas, bg="black")
    my_canvas.create_window((0, 0), window=scrollable_frame, anchor=NW)

    def close_display():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

    # choose show type
    Label(frame1, text='Type', bg="#60b8eb").place(relx=0.05, rely=0.25, relheight=0.05, relwidth=0.2, anchor=NW)
    option2 = StringVar(frame1)
    option2.set("ALL")
    op2list = ["ALL", "movie", "tv"]
    o2 = OptionMenu(frame1, option2, *op2list)
    o2.config(fg="#000000",bg="#ffffff")
    o2.place(relx=0.25, rely=0.25, relheight=0.05, relwidth=0.7, anchor=NW)
    

    # choose searching theme <title, director, cast>
    option = StringVar(frame1)
    option.set("Title")
    oplist = ["Title", "Director", "Cast"]
    o = OptionMenu(frame1, option,"Title", "Director", "Cast")
    o.config(fg="#000000",bg="#ffffff")
    o.place(relx=0.25, rely=0.35, relheight=0.05, relwidth=0.7, anchor=NW)
    Label(frame1, text=option.get(), bg="#60b8eb").place(relx=0.05, rely=0.35, relheight=0.05, relwidth=0.2, anchor=NW)



    Label(frame1, text='Keyword', bg="#60b8eb").place(relx=0.05, rely=0.45, relheight=0.05, relwidth=0.2, anchor=NW)
    e = Entry(frame1, fg='black', bg='white')
    e.place(relx=0.25, rely=0.45, relheight=0.05, relwidth=0.7, anchor=NW)
    
    global optionGenre, optionDirector

    optionGenre = StringVar(frame1)
    optionGenre.set('ALL')
    optionDirector = StringVar(frame1)
    optionDirector.set('ALL')


    global oglist, odlist
    oglist=['ALL']
    odlist=['ALL']

    global od, og
    Label(frame1, text='Country', bg="#60b8eb").place(relx=0.05, rely=0.65, relheight=0.05, relwidth=0.2, anchor=NW)
    od = OptionMenu(frame1, optionDirector, *odlist)
    od.config(foreground="black",background="white")
    od.place(relx=0.25, rely=0.65, relheight=0.05, relwidth=0.7, anchor=NW)

    Label(frame1, text='Genre', bg="#60b8eb").place(relx=0.05, rely=0.75, relheight=0.05, relwidth=0.2, anchor=NW)
    og = OptionMenu(frame1, optionGenre, *oglist)
    og.config(foreground="black",background="white")
    og.place(relx=0.25, rely=0.75, relheight=0.05, relwidth=0.7, anchor=NW)

    def search():
        close_display()

        oglist=['ALL']
        odlist=['ALL']
        conn = connect()
        c = conn.cursor()

        genre = optionGenre.get()
        country=optionDirector.get()
        if genre=='ALL':
            genre=''
        if country=='ALL':
            country=''
        if option2.get() == "ALL":
            result = []
            table_list = ['movie', 'tv']
            for i in table_list:
                if option.get() == "Title":
                    query = f'''SELECT m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year, m.duration as Duration, c.country as Country
                                FROM table_{i} m
                                JOIN table_genre g on m.show_id = g.show_id
                                JOIN table_director d on m.show_id = d.show_id
                                JOIN table_country c on m.show_id = c.show_id
                                WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Title LIKE %s'''
                    c.execute(query, ("%" + str(e.get()) + "%",))
                    result1 = c.fetchall()
                    result = result + result1
                    columns=['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Country']

                if option.get() == "Director":
                    query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year, m.duration as Duration, c.country as Country
                                FROM table_{i} m
                                JOIN table_genre g on m.show_id = g.show_id
                                JOIN table_director d on m.show_id = d.show_id
                                JOIN table_country c on m.show_id = c.show_id
                                WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Director LIKE %s'''
                    c.execute(query, ("%" + str(e.get()) + "%",))
                    result2 = c.fetchall()
                    result = result + result2
                    columns=['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Country']

                if option.get() == "Cast":
                    query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, ca.cast as Cast, m.release_year as Release_Year, c.country as Country, m.duration as Duration
                                FROM table_{i} m
                                JOIN table_genre g on m.show_id = g.show_id
                                JOIN table_director d on m.show_id = d.show_id
                                JOIN table_cast ca on m.show_id = ca.show_id
                                JOIN table_country c on m.show_id = c.show_id
                                WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Cast LIKE %s'''
                    c.execute(query, ("%" + str(e.get()) + "%",))
                    result3 = c.fetchall()
                    result = result + result3
                    columns=['Title', 'Genre', 'Director', 'Cast','Release Year', 'Duration', 'Country']


        else:
            if option.get() == "Title":
                query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year, m.duration as Duration, c.country as Country
                            FROM table_{option2.get()} m
                            JOIN table_genre g on m.show_id = g.show_id
                            JOIN table_director d on m.show_id = d.show_id
                            JOIN table_country c on m.show_id = c.show_id
                            WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Title LIKE %s'''
                c.execute(query, ("%" + str(e.get()) + "%",))
                result = c.fetchall()

                genrequery = f'''
                SELECT g.genre as Genre
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE Genre LIKE '%{genre}%' and c.country LIKE '%{country}%' and m.title LIKE '%{e.get()}%'
                GROUP BY Genre;
                '''
                c.execute(genrequery)
                resultgenre = c.fetchall()
                for i in resultgenre:
                    oglist.append(i[0])

                countryquery = f'''
                SELECT c.country as Country
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE g.genre LIKE '%{genre}%' and Country LIKE '%{country}%' and  m.title LIKE '%{e.get()}%'
                GROUP BY Country;
                '''
                c.execute(countryquery)
                resultcountry = c.fetchall()
                for i in resultcountry:
                    odlist.append(i[0])
                columns=['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Country']
                

            if option.get() == "Director":
                query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year, m.duration as Duration, c.country as Country
                            FROM table_{option2.get()} m
                            JOIN table_genre g on m.show_id = g.show_id
                            JOIN table_director d on m.show_id = d.show_id
                            JOIN table_country c on m.show_id = c.show_id
                            WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Director LIKE %s'''
                c.execute(query, ("%" + str(e.get()) + "%",))
                result = c.fetchall()

                genrequery = f'''
                SELECT g.genre as Genre
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE Genre LIKE '%{genre}%' and c.country LIKE '%{country}%' and d.director LIKE '%{e.get()}%'
                GROUP BY Genre;
                '''
                c.execute(genrequery)
                resultgenre = c.fetchall()
                for i in resultgenre:
                    oglist.append(i[0])

                countryquery = f'''
                SELECT c.country as Country
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE g.genre LIKE '%{genre}%' and Country LIKE '%{country}%' and d.director LIKE '%{e.get()}%'
                GROUP BY Country;
                '''
                c.execute(countryquery)
                resultcountry = c.fetchall()
                for i in resultcountry:
                    odlist.append(i[0])
                columns=['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Country']
                

            if option.get() == "Cast":
                query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, ca.cast as Cast, m.release_year as Release_Year, c.country as Country, m.duration as Duration
                            FROM table_{option2.get()} m
                            JOIN table_genre g on m.show_id = g.show_id
                            JOIN table_director d on m.show_id = d.show_id
                            JOIN table_cast ca on m.show_id = ca.show_id
                            JOIN table_country c on m.show_id = c.show_id
                            WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Cast LIKE %s'''
                c.execute(query, ("%" + str(e.get()) + "%",))
                result = c.fetchall()

                genrequery = f'''
                SELECT g.genre as Genre
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_cast ca on m.show_id = ca.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE Genre LIKE '%{genre}%' and c.country LIKE '%{country}%' and ca.cast LIKE '%{e.get()}%'
                GROUP BY Genre;
                '''
                c.execute(genrequery)
                resultgenre = c.fetchall()
                for i in resultgenre:
                    oglist.append(i[0])

                countryquery = f'''
                SELECT c.country as Country
                FROM table_{option2.get()} m
                JOIN table_genre g on m.show_id = g.show_id
                JOIN table_director d on m.show_id = d.show_id
                JOIN table_cast ca on m.show_id = ca.show_id
                JOIN table_country c on m.show_id = c.show_id
                WHERE g.genre LIKE '%{genre}%' and Country LIKE '%{country}%' and ca.cast LIKE '%{e.get()}%'
                GROUP BY Country;
                '''
                c.execute(countryquery)
                resultcountry = c.fetchall()
                for i in resultcountry:
                    odlist.append(i[0])
                columns=['Title', 'Genre', 'Director', 'Cast','Release Year', 'Duration', 'Country']
                

        if len(result)==0:
            messagebox.showinfo('', 'No show found.')
            return
        k = 1
        for cols in columns:
            res_label = Label(scrollable_frame, text=cols, bg="#000000", fg="#ffffff")
            res_label['font'] = font.Font(family="Roboto", size=10, weight='bold')
            res_label.grid(row=0, column=k)
            k = k + 1

        global btns,show_ids
        btns={}
        show_ids=[]
        for res in result:
            show_ids.append(res[0])
        result_index=0
        for ind,d in enumerate(show_ids):
            res_label2 = Button(scrollable_frame, text=result[result_index][1], bg="#000000", fg="white")
            res_label2['font'] = font.Font(family="Roboto", size=8, weight='bold')
            res_label2.grid(row=ind+1, column=1, sticky=NSEW)
            res_label2.config(command=lambda e=ind: detail(e))
            btns[ind]=res_label2
            result_index+=1

        i = 1
        for res in result:
            for j in range(2,len(res)):
                res_label2 = Label(scrollable_frame, text=res[j], bg="#000000", fg="white")
                res_label2['font'] = font.Font(family="Roboto", size=8, weight='bold')
                res_label2.grid(row=i, column=j, sticky=NSEW)

                if option2.get() == "ALL":
                    if j==2:
                        # genre
                        if(res[2] not in oglist):
                            oglist.append(res[2])
                    if j==3:
                        if(res[6] not in odlist):
                            odlist.append(res[6])
            i = i + 1
        conn.close()

        od = OptionMenu(frame1, optionDirector, *odlist)
        od.config(fg="#000000",bg="#ffffff")
        od.place(relx=0.25, rely=0.65, relheight=0.05, relwidth=0.7, anchor=NW)

        og = OptionMenu(frame1, optionGenre, *oglist)
        og.config(fg="#000000",bg="#ffffff")
        og.place(relx=0.25, rely=0.75, relheight=0.05, relwidth=0.7, anchor=NW)
        pass

    def reset():
        optionGenre.set("ALL")
        optionDirector.set("ALL")
        option.set("Title")
        option2.set("ALL")
        e.delete(0,END)

    button1 = Button(frame1, text="Search", command=search)
    button1.config( bg='white', fg='black')
    button1.place(relx=0.05, rely=0.53, relheight=0.07, relwidth=0.4)

    button2 = Button(frame1, text="Reset", command=reset)
    button2.config( bg='white', fg='black')
    button2.place(relx=0.55, rely=0.53, relheight=0.07, relwidth=0.4)

    ### detail page ###

    def detail(index):
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

        def bringComment():
            mydb = connect()

            myCursor = mydb.cursor()

            sqlString = f""" 
            SELECT `comment`, `date`
            FROM table_comment
            WHERE show_id='{show_id}'
            ORDER BY `date`;
            """
            myCursor.execute(sqlString)
            myResult = myCursor.fetchall()

            mydb.close()

            for i in myResult:
                Label(commentgridframe, text=i[0], bg="#60b8eb").grid(row=myResult.index(i), column=0 )
                Label(commentgridframe, text=i[1], bg="#60b8eb").grid(row=myResult.index(i), column=1, padx=3, pady=3, ipady=4)

        showresult(result)
        bringComment()
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
                if option.get() == 'Type':
                    messagebox.showinfo("Error",'Choose the type of the show.')
                    return
                else:
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

        def like():
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
            getlike()

        def getlike():
            mydb = connect()
            myCursor = mydb.cursor()
            sqlString = f""" 
            SELECT `like`
            FROM table_like
            WHERE show_id = '{show_id}';
            """

            myCursor.execute(sqlString)
            status = myCursor.fetchall()
            print(status)
            try:
                if status[0][0] == 1:
                    likeBtn.config(bg='#ff0000')
                else:
                    likeBtn.config(bg='#ffffff')
            except:
                likeBtn.config(bg='#ffffff')
            mydb.close()

        getlike()
        likeBtn.config(command=like)

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
                for i in commentgridframe.winfo_children():
                    i.destroy()

                bringComment()
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


    def add():
        global window_a
        columns = ["title", "date_added", "release_year", "rating", "duration", "description", "casts", "directors",
                   "countries", "genres"
                   ]
        window_a = Tk()
        window_a.title('Add show')
        window_a.geometry('700x500')

        frame = Frame(window_a, bg="black")
        frame.pack(side = LEFT, fill = BOTH, expand = 1)

        tableNm = Label(frame, text='Type', fg="white", bg="black")
        tableNm.grid(row=0, column=0)

        option = StringVar(frame)
        option.set("Type")
        o3 = OptionMenu(frame, option, "TV Show", "Movie")
        o3.grid(row=0, column=1)

        for i in columns:
            Label(frame, text=i,fg="white", bg="black").grid(row=columns.index(i) + 1, column=0)
            e = Entry(frame, width=70)
            if (columns.index(i) > 5):
                e.insert(END, "['']")
            else:
                e.insert(END, '')

            e.grid(row=columns.index(i) + 1, column=1, padx=3, pady=5, ipady=7)

        saveBtn = Button(frame, text='Save')
        saveBtn.grid(row=11, column=1, sticky='e', )

        def editSave():
            if option.get() == 'Type':
                messagebox.showinfo("Error",'Choose the type of the show.')
                return

            else:
                for i in range(10):
                    if frame.winfo_children()[2*i +3 ].get()=="" or frame.winfo_children()[2*i +3 ].get()=="['']":
                        messagebox.showinfo("Error",'Write the '+frame.winfo_children()[2*(i+1)]["text"] +' of the show.')
                        return
            mydb = connect()

            myCursor = mydb.cursor()
            # myCursor.execute("USE teamProject")

            entrylist=[]
            if option.get()=='TV Show':
                table='table_tv'
            else:
                table='table_movie'
            
            sqlShow = f"""
            SELECT show_id
            FROM table_movie
            ORDER BY show_id DESC
            LIMIT 1;
            """
            myCursor.execute(sqlShow)
            myResult = myCursor.fetchall()
            show_id = myResult[0][0]

            sqlShow = f"""
            SELECT show_id
            FROM table_tv
            ORDER BY show_id DESC
            LIMIT 1;
            """
            myCursor.execute(sqlShow)
            myResult = myCursor.fetchall()
            if(show_id<myResult[0][0]):
                show_id = myResult[0][0]

            show_id+=1
            for i in range(10):
                entrylist.append(frame.winfo_children()[2 * i + 3].get())
                if i == 6:
                    # cast
                    string = entrylist[i][1:-1]
                    listt = string.split(',')

                    for cast in listt:
                        print(cast)
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
                        myCursor.execute(f"INSERT INTO table_country(show_id, country) VALUES('{show_id}',{country})")
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
            messagebox.showinfo("", "Show Added!")
            window_a.destroy()

        saveBtn.config(command=editSave)
        window_a.mainloop()

    button5 = Button(frame1, text="Add", command=add)
    button5.place(relx=0.45, rely=0.9, relheight=0.05, relwidth=0.4)

    window.mainloop()
