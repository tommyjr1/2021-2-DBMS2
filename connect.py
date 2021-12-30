from sys import exit
import mysql.connector
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox

# Have to change password
def connect():
    global mydb
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='Jewelmysql',
            database='teamproject')
        return mydb
        
    except:
        messagebox.showwarning('DB not connected', 'Your code is not connected to the database. Change the password in main_page1.py')
        return