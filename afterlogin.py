from tkinter import *
from tkinter import Scrollbar
from tkinter import ttk
from PIL import ImageTk
import PIL.Image
import cv2 as cv
from searchpage import *
from mypage import *

path = 'C:/Users/user/Documents/2021-2학기/데이터베이스관리2_가야나다라잔/팀프로젝트/final/PBL/src/'
window = Tk()

window.title("Show")
window.geometry("1280x720")
window.resizable(False, False)

frameBlack = Frame(window, bg='black')
frameBlack.pack(fill=BOTH, expand=1)

frame = Frame(frameBlack, bg='black')
frame.place(relx=.5, rely=.5, anchor=CENTER)

searchBtn = Button(frame,bg='black')
ii1 = PIL.Image.open(path+'img1.png')
re1 = ii1.resize((150,150),PIL.Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(re1)
searchBtn.config(image=img1,borderwidth=0, highlightthickness=0)
searchBtn.grid(row=0, column=0,padx=60)
Label(frame, text='Search',bg='black', fg='white').grid(row=1, column=0)

mypageBtn = Button(frame,bg='black')
ii2 = PIL.Image.open(path+'img2.png')
re2 = ii2.resize((150,150),PIL.Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(re2)
mypageBtn.config(image=img2,borderwidth=0, highlightthickness=0)
mypageBtn.grid(row=0, column=1,padx=60)
Label(frame, text='My Page',bg='black', fg='white').grid(row=1, column=1)

exitBtn = Button(frame,bg='black')
ii3 = PIL.Image.open(path+'img3.png')
re3 = ii3.resize((150,150),PIL.Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(re3)
exitBtn.config(image=img3,borderwidth=0, highlightthickness=0)
exitBtn.grid(row=0, column=2,padx=60)
Label(frame, text='Exit',bg='black', fg='white').grid(row=1, column=2)