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
# tkinter를 사용하기 위한 import
from tkinter import *
from tkinter import ttk

# tkinter 객체 생성
window = Tk()

# 사용자 id와 password를 저장하는 변수 생성
user_id, password = StringVar(), StringVar()

# 사용자 id와 password를 비교하는 함수
def check_data():
    if user_id.get() == "Passing" and password.get() == "Story":
        print("Logged IN Successfully")
    else:
        print("Check your Usernam/Password")

# id와 password, 그리고 확인 버튼의 UI를 만드는 부분
ttk.Label(window, text = "Username : ").grid(row = 0, column = 0, padx = 10, pady = 10)
ttk.Label(window, text = "Password : ").grid(row = 1, column = 0, padx = 10, pady = 10)
ttk.Entry(window, textvariable = user_id).grid(row = 0, column = 1, padx = 10, pady = 10)
ttk.Entry(window, textvariable = password).grid(row = 1, column = 1, padx = 10, pady = 10)
ttk.Button(window, text = "Login", command = check_data).grid(row = 2, column = 1, padx = 10, pady = 10)

window.mainloop()



frm = Frame(window, width=1280, height=720)
frm.place(relx=.5, rely=.5, anchor=CENTER)


lbl1 = Label(frm)
lbl1.grid()

cap = cv.VideoCapture(path+'netflix_intro.mp4')

def video_play():
    ret, frame = cap.read()
    if not ret:
        cap.release() 
        frm.destroy()
        return
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    img = PIL.Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img) 
    
    lbl1.imgtk = imgtk
    lbl1.configure(image=imgtk)
    lbl1.after(5, video_play)
def searchPage():
    view()
    return
def myPage():
    open_mypage()
    return
def exitr():
    window.destroy()

searchBtn.config(command=searchPage)
mypageBtn.config(command=myPage)
exitBtn.config(command=exitr)
video_play()

window.mainloop()

