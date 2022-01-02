from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from connect import *
from textwrap import *
from detailpage import *

# Loading Search
def view():

    #### GUI ####
    window = Tk()
    window.title("Search shows")
    window.geometry("1920x1080")

    frame1 = Frame(window, bg="#60b8eb")
    frame1.place(relx=0, rely=0, relwidth=0.2, relheight=1)

    frame2 = Frame(window)
    frame2.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

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
    Label(frame1, text='Type', bg="#60b8eb").place(relx=0.05, rely=0.15, relheight=0.05, relwidth=0.2, anchor=NW)
    option2 = StringVar(frame1)
    option2.set("ALL")
    op2list = ["ALL", "movie", "tv"]
    o2 = OptionMenu(frame1, option2, *op2list)
    o2.config(fg="#000000",bg="#ffffff")
    o2.place(relx=0.25, rely=0.15, relheight=0.05, relwidth=0.7, anchor=NW)
    

    # choose searching theme <title, director, cast>
    option = StringVar(frame1)
    option.set("Title")
    oplist = ["Title", "Director", "Cast"]
    o = OptionMenu(frame1, option,"Title", "Director", "Cast")
    o.config(fg="#000000",bg="#ffffff")
    o.place(relx=0.25, rely=0.25, relheight=0.05, relwidth=0.7, anchor=NW)
    Label(frame1, text=option.get(), bg="#60b8eb").place(relx=0.05, rely=0.25, relheight=0.05, relwidth=0.2, anchor=NW)



    Label(frame1, text='Keyword', bg="#60b8eb").place(relx=0.05, rely=0.35, relheight=0.05, relwidth=0.2, anchor=NW)
    e = Entry(frame1, fg='black', bg='white')
    e.place(relx=0.25, rely=0.35, relheight=0.05, relwidth=0.7, anchor=NW)
    
    global optionGenre, optionDirector

    optionGenre = StringVar(frame1)
    optionGenre.set('ALL')
    optionDirector = StringVar(frame1)
    optionDirector.set('ALL')


    global oglist, odlist
    oglist=['ALL']
    odlist=['ALL']

    global od, og
    Label(frame1, text='Country', bg="#60b8eb").place(relx=0.05, rely=0.6, relheight=0.05, relwidth=0.2, anchor=NW)
    od = OptionMenu(frame1, optionDirector, *odlist)
    od.config(foreground="black",background="white")
    od.place(relx=0.25, rely=0.6, relheight=0.05, relwidth=0.7, anchor=NW)

    Label(frame1, text='Genre', bg="#60b8eb").place(relx=0.05, rely=0.7, relheight=0.05, relwidth=0.2, anchor=NW)
    og = OptionMenu(frame1, optionGenre, *oglist)
    og.config(foreground="black",background="white")
    og.place(relx=0.25, rely=0.7, relheight=0.05, relwidth=0.7, anchor=NW)

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
                    query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year,  m.duration as Duration,c.country as Country
                                FROM table_{i} m
                                JOIN table_genre g on m.show_id = g.show_id
                                JOIN table_director d on m.show_id = d.show_id
                                JOIN table_cast ca on m.show_id = ca.show_id
                                JOIN table_country c on m.show_id = c.show_id
                                WHERE Genre LIKE '%{genre}%' and Country LIKE '%{country}%' and Cast LIKE %s'''
                    c.execute(query, ("%" + str(e.get()) + "%",))
                    result3 = c.fetchall()
                    result = result + result3
                    columns=['Title', 'Genre', 'Director','Release Year', 'Duration', 'Country']


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
                query = f'''SELECT  m.show_id, m.title as Title, g.genre as Genre, d.director as Director, m.release_year as Release_Year, m.duration as Duration,c.country as Country
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
                columns=['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Country']
                

        if len(result)==0:
            messagebox.showinfo('', 'No show found.')
            return

        k = 1
        for cols in columns:
            res_label = Label(scrollable_frame, text=cols, bg="#000000", fg="#ffffff")
            res_label['font'] = font.Font(family="NanumBarunGothic", size=10, weight='bold')
            res_label.grid(row=0, column=k)
            k = k + 1

        global btns,show_ids
        btns={}
        show_ids=[]
        genres = []
        directors=[]
        countries=[]
        indexs=[]

        before_res=result[0]

        each_gen=[]
        each_dir=[]
        each_con=[]

        for res in result:
            if (len(result)==1):
                show_ids.append(res[0])
                genres.append(res[2])
                if res[2] not in oglist:
                    oglist.append(res[2])
                directors.append(res[3])
                countries.append(res[6])
                if res[6] not in odlist:
                    odlist.append(res[6])
                indexs.append(result.index(res))
                break

            elif(before_res[0]!=res[0]):
                #이전꺼랑 지금꺼가 다름
                #이전꺼 넣어줘야함
                show_ids.append(before_res[0])
                genres.append(each_gen)
                directors.append(each_dir)
                countries.append(each_con)
                indexs.append(result.index(before_res))
                each_gen=[]
                each_con=[]
                each_dir=[]

            
            if res[2] not in each_gen:
                each_gen.append(res[2])
            if res[2] not in oglist:
                    oglist.append(res[2])
            if res[3] not in each_dir:
                each_dir.append(res[3])
            if res[6] not in each_con:
                each_con.append(res[6])
            if res[6] not in odlist:
                    odlist.append(res[6])
            before_res = res
            
            #이게 제일 마지막꺼일때
            if res==result[-1]:
                show_ids.append(res[0])
                genres.append(each_gen)
                directors.append(each_dir)
                countries.append(each_con)
                indexs.append(result.index(res))
                each_gen=[]
                each_con=[]
                each_dir=[]
                
        # for idx in indexs:
        for ind,d in enumerate(show_ids):
            txt = str(result[indexs[ind]][1])
            txtcon = fill(txt, width=20)
            res_label2 = Button(scrollable_frame, text=txtcon, bg="#000000", fg="white")
            res_label2['font'] = font.Font(family="NanumBarunGothic", size=1, weight='bold')
            res_label2.grid(row=ind+1, column=1, sticky=NSEW)
            res_label2.config(command=lambda e=ind: detail(e, show_ids))
            btns[ind]=res_label2
            
        for idx, ind in enumerate(indexs):
            #장르
            # for e_gen in genres:
            txt = str(genres[idx])
            if txt.startswith('['):
                txtcon = fill(txt[1:-1], width=20)
            else:
                txtcon = fill(txt, width=20)

            res_label2 = Label(scrollable_frame, text=txtcon, bg="#000000", fg="white")
            res_label2['font'] = font.Font(family="NanumBarunGothic", size=2, weight='bold')
            res_label2.grid(row=idx+1, column=2)
            #디렉터
            # for e_dir in directors:
            txt = str(directors[idx])
            if txt.startswith('['):
                txtcon = fill(txt[1:-1], width=20)
            else:
                txtcon = fill(txt, width=20)
            res_label2 = Label(scrollable_frame, text=txtcon, bg="#000000", fg="white")
            res_label2['font'] = font.Font(family="NanumBarunGothic", size=2, weight='bold')
            res_label2.grid(row=idx+1, column=3)

            for j in range(4,6):
                res_label2 = Label(scrollable_frame, text=result[ind][j], bg="#000000", fg="white")
                res_label2['font'] = font.Font(family="NanumBarunGothic", size=2, weight='bold')
                res_label2.grid(row=idx+1, column=j)
            #나라
            # for e_con in countries:
            txt = str(countries[idx])
            if txt.startswith('['):
                txtcon = fill(txt[1:-1], width=20)
            else:
                txtcon = fill(txt, width=20)
            res_label2 = Label(scrollable_frame, text=txtcon, bg="#000000", fg="white")
            res_label2['font'] = font.Font(family="NanumBarunGothic", size=2, weight='bold')
            res_label2.grid(row=idx+1, column=6)


        conn.close()

        od = OptionMenu(frame1, optionDirector, *odlist)
        od.config(fg="#000000",bg="#ffffff")
        od.place(relx=0.25, rely=0.6, relheight=0.05, relwidth=0.7, anchor=NW)

        og = OptionMenu(frame1, optionGenre, *oglist)
        og.config(fg="#000000",bg="#ffffff")
        og.place(relx=0.25, rely=0.7, relheight=0.05, relwidth=0.7, anchor=NW)
        pass

    def reset():
        optionGenre.set("ALL")
        optionDirector.set("ALL")
        option.set("Title")
        option2.set("ALL")
        e.delete(0,END)

    button1 = Button(frame1, text="Search", command=search)
    button1.config( bg='white', fg='black')
    button1.place(relx=0.05, rely=0.45, relheight=0.07, relwidth=0.4)

    button2 = Button(frame1, text="Reset", command=reset)
    button2.config( bg='white', fg='black')
    button2.place(relx=0.55, rely=0.45, relheight=0.07, relwidth=0.4)

    def add():
        global window_a
        columns = ["Title", "Date_added", "Release_year", "Rating", "Duration", "Description", "Casts", "Directors",
                   "Countries", "Genres"
                   ]
        window_a = Tk()
        window_a.title('Add show')
        window_a.geometry('650x500')
        

        frame = Frame(window_a, bg="black")
        frame.pack(side = LEFT, fill = BOTH, expand = 1)
        font2=font.Font(family="NanumBarunGothic",weight="bold")

        tableNm = Label(frame, text='Type', fg="white", bg="black")
        tableNm.grid(row=0, column=0)
        tableNm.configure(font=font2)

        option = StringVar(frame)
        option.set("Type")
        o3 = OptionMenu(frame, option, "TV Show", "Movie")
        o3.grid(row=0, column=1)

        for i in columns:
            font2=font.Font(family="NanumBarunGothic",weight="bold")
            label2 = Label(frame, text=i,fg="white", bg="black")
            label2.grid(row=columns.index(i) + 1, column=0)
            label2.configure(font=font2)
            e = Entry(frame, width=70)
            if (columns.index(i) > 5):
                e.insert(END, "['']")
            else:
                e.insert(END, '')
            e.grid(row=columns.index(i) + 1, column=1, padx=3, pady=5, ipady=7)

        saveBtn = Button(frame, text='Save',width=10)
        saveBtn.grid(row=11, column=1)


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
    button5.place(relx=0.05, rely=0.8, relheight=0.05, relwidth=0.9)
    window.mainloop()
