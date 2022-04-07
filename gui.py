import mysql.connector
from tkinter import *
from datetime import date, datetime, timedelta

def connect(email, password):
    global db
    global userEmail

    #Check if email and password exists
    #If not throw exception

    # Set the signed in user's email globally
    userEmail = email

    #Change scene to user page
    #This will only run if there are no exceptions
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
    createButton = Button(page, text="Create", bg="white", command=lambda:change_page(create_page))
    createButton.grid(column = 1, row = 2, sticky="e")

    #Create label that displays login errors

def create_page(root):
    global db
    page = Frame(root)
    page.grid()

    cursor = db.cursor()

    # Add name boxes
    # Email box
    # Password box
    # OK / cancel buttons


def create_food_record(time, duration, type, foodList):
    global db
    # Submit SQL command to add this food record
    cursor = db.cursor()

def get_food_records():
    global db
    cursor = db.cursor()

    # Submit SQL command to get food records for signed in email.

    recordsList = ["test1", "test2"]
    return recordsList

def user_page(root):
    global db
    page = Frame(root)
    page.grid()

    cursor = db.cursor()

    #maybe create different pages for these sections / users

    #user:

    #View normal food intake record
    foodListLabel = Label(page, text="Food Intake Records")
    foodListLabel.grid(row=0, column=0, sticky="ew")
    refreshButton = Button(page, text="Refresh", command=lambda:get_food_records())
    refreshButton.grid(row=0, column=1, stick="w")
    foodList = Listbox(page, bg="white")
    foodList.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Refresh once initially
    recordList = get_food_records()
    i = 1
    for record in recordList:
        foodList.insert(i, record)
        i += 1

    # Create food intake record
    createLabel = Label(page, bg="white", text="Create Food Intake Record")
    createLabel.grid(row=2, column=0, sticky="w")
    timeLabel = Label(page,  text="Time:")
    timeLabel.grid(row=3, column=0, sticky="w")
    time = Entry(page)
    time.grid(row=3, column=1, sticky="w")
    durationLabel = Label(page, text="Duration:")
    durationLabel.grid(row=4, column=0, sticky="w")
    duration = Entry(page)
    duration.grid(row=4, column=1, sticky="w")
    typeLabel = Label(page, text="Meal:")
    typeLabel.grid(row=5, column=0, sticky="w")
    mealTypes = ["Breakfast", "Lunch", "Dinner", "Other"]
    typeOptions = StringVar()
    typeOptions.set(mealTypes[3])
    typeMenu = OptionMenu(page, typeOptions, *mealTypes)
    typeMenu.grid(row=5, column=1, sticky="w")
    foodsLabel = Label(page, text="Foods:")
    foodsLabel.grid(row=6, column=0, sticky="w")
    foods = Entry(page)
    foods.grid(row=6, column=1, sticky="w")
    createButton = Button(page, text="Create", command=lambda:create_food_record(time.get(), duration.get(), typeOptions.get(), foods.get()))
    createButton.grid(row=2, column=1, sticky="w")

    #if premium user:
    #Create premium food intake record

    #View premium food intake record

    #Create goal

    #View goal

    #Create goal analysis

    #View goal analysis

    # Sign out of account
    signOutButton = Button(page, text="Sign Out", bg="white", command=lambda:change_page(login_page))
    signOutButton.grid(row=8, column=0, sticky="w")

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

# Declare signed in user's email
userEmail = ""

#Create GUI
root = Tk()
root.title("Diet Tracking Database")
root.geometry("720x480")
root.config(bg = "gray")

#Go to login page
login_page(root)

#Start main loop
root.mainloop()
