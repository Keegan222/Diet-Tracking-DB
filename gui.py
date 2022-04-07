import mysql.connector
from tkinter import *

def connect(email, password):
    global db

    #Check if email and password exists
    #If not throw exception

    #Change scene to user page
    #This will only run if there are no exceptions
    change_page(user_page)

def create(email, password):
    global db

    # Check if the account already exists
    # If it does throw exception

    # Add row to the DB
    # Sign new user in automatically

    # Change scene to user page
    change_page(user_page)

def login_page(root):
    page = Frame(root)
    page.grid()

    #Create Email and Password labels
    email_label = Label(page, text ="Email: ")
    email_label.grid(column = 0, row = 0, sticky="ew")

    email = Entry(page)
    email.grid(column = 1, row = 0, columnspan=200, sticky="ew")

    password_label = Label(page, text ="Password: ")
    password_label.grid(column = 0, row = 1, sticky="ew")

    password = Entry(page)
    password.grid(column = 1, row = 1, sticky="ew")

    #Create submission button
    button = Button(page, text ="Login", bg ="white", command = lambda : connect(email.get(), password.get()))
    button.grid(column = 1, row = 2, sticky="w")

    # Create account creation button
    createButton = Button(page, text="Create", bg="white", command=lambda:create(email.get(), password.get()))
    createButton.grid(column = 1, row = 2, sticky="e")
    
    #Create label that displays login errors

def user_page(root):
    global db
    page = Frame(root)
    page.grid()

    cursor = db.cursor()

    #maybe create different pages for these sections / users

    #user:
    #Create normal food intake record

    #View normal food intake record


    #if premium user:
    #Create premium food intake record

    #View premium food intake record

    #Create goal

    #View goal

    #Create goal analysis

    #View goal analysis

def change_page(page):
    global root
    for widget in root.winfo_children():
        widget.destroy()
    page(root)

#Create global database variable and connect
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "rootpass",
    db = "comp_3753")

#Create GUI
root = Tk()
root.title("Diet Tracking Database")
root.geometry("720x480")
root.config(bg = "gray")

#Go to login page
login_page(root)

#Start main loop
root.mainloop()
