import mysql.connector
from tkinter import *
from datetime import date, datetime, timedelta

def login(email, password):
    global db, userEmail
    userEmail = ""
    cursor = db.cursor()

    #Get password
    cursor.execute("SELECT password_hash "
        "FROM user_data "
        "WHERE email_address = %s", (email,))
    result = cursor.fetchone()

    #Check if email exists
    if result == None:
        return "Account does not exist"

    #Check if password is correct
    if result[0] != password:
        return "Invalid password"

    # Set the signed in user's email globally
    userEmail = email

    #Change scene to user page
    change_page(user_page)

    return "Success"

def create(first_name, middle_name, last_name, email, password):
    global db, userEmail
    cursor = db.cursor()

    #Check if first name is valid
    if len(first_name) == 0 or len(first_name) > 256:
        return "Invalid first name"

    #check if middle name is valid
    if len(middle_name) > 256:
        return "Invalid middle name"

    #Check if last name is valid
    if len(last_name) == 0 or len(last_name) > 256:
        return "Invalid last name"

    #Check if email is valid
    if len(email) == 0:
        return "Invalid email"

    #Check if password is valid
    if len(password) == 0 or len(password) > 256:
        return "Invalid password"

    # Check if the account already exists
    cursor.execute("SELECT 1 "
        "FROM user_data "
        "WHERE email_address = %s", (email,))

    if len(cursor.fetchall()) != 0:
        return "Account already exists for this email"

    # Add row to the DB
    sql = "INSERT INTO user_data " \
        "(first_name, middle_name, last_name, email_address, premium, password_hash) " \
        "VALUES (%s, %s, %s, %s, %s, %s)"
    values = (first_name, middle_name, last_name, email, 0, password)
    cursor.execute(sql, values)
    db.commit()

    # Set global email variable
    userEmail = email

    # Change scene to user page
    change_page(user_page)

    return "Success"

def set_error_label(label, result):
    #Only set error label if result is not successful.
    #Otherwise it will throw errors if the label is changed after the page is changes
    if (result != "Success"):
        label.configure(text=result)

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

    #Create first name
    first_name_label = Label(page, text ="First name: ")
    first_name_label.grid(column = 2, row = 0, sticky="ew")
    first_name = Entry(page)
    first_name.grid(column = 3, row = 0, columnspan=200, sticky="ew")

    #Create middle name
    middle_name_label = Label(page, text ="Middle name: ")
    middle_name_label.grid(column = 2, row = 1, sticky="ew")
    middle_name = Entry(page)
    middle_name.grid(column = 3, row = 1, columnspan=200, sticky="ew")

    #Create last name
    last_name_label = Label(page, text ="Middle name: ")
    last_name_label.grid(column = 2, row = 2, sticky="ew")
    last_name = Entry(page)
    last_name.grid(column = 3, row = 2, columnspan=200, sticky="ew")

    #Create label that displays errors
    error_label = Label(page, text = "")
    error_label.grid(column = 0, row = 4, sticky="ew")

    #Create login button
    button = Button(page, text ="Login", bg ="white", command = lambda : set_error_label(error_label, login(email.get(), password.get())))
    button.grid(column = 1, row = 3, sticky="w")

    #Create account creation button
    createButton = Button(page, text="Create", bg="white", command=lambda: set_error_label(error_label, create(first_name.get(), middle_name.get(), last_name.get(), email.get(), password.get())))
    createButton.grid(column = 3, row = 3, sticky="w")

def create_food_record(date, time, duration, mealType, foodList, listBox):
    global db
    # Submit SQL command to add this food record
    cursor = db.cursor()

    sql = "INSERT INTO food_records (owner_email, date, start_time, duration, meal_type, foods) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (userEmail, date, time, duration, mealType, foodList)
    cursor.execute(sql, values)
    db.commit()

    get_food_records(listBox)

def get_food_records(foodList):
    global db
    cursor = db.cursor()

    foodList.delete(0, END)

    # Submit SQL command to get food records for signed in email.
    recordsList = []
    cursor.execute("SELECT * FROM food_records WHERE owner_email = %s", (userEmail,))
    result = cursor.fetchone()
    while result != None:
        recordsList.append(result)
        result = cursor.fetchone()

    i = 1
    for record in recordsList:
        foodList.insert(i, record)
        i += 1

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
    foodList = Listbox(page, bg="white")
    foodList.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Refresh once initially
    get_food_records(foodList)

    # Create food intake record
    createLabel = Label(page, bg="white", text="Create Food Intake Record")
    createLabel.grid(row=2, column=0, sticky="w")
    dateLabel = Label(page, text="Date (YYYY/MM/DD): ")
    dateLabel.grid(row=3, column=0, sticky="w")
    date = Entry(page)
    date.grid(row=3, column=1, sticky="w")
    timeLabel = Label(page,  text="Time (HH:MM:SS):")
    timeLabel.grid(row=4, column=0, sticky="w")
    time = Entry(page)
    time.grid(row=4, column=1, sticky="w")
    durationLabel = Label(page, text="Duration (Minutes):")
    durationLabel.grid(row=5, column=0, sticky="w")
    duration = Entry(page)
    duration.grid(row=5, column=1, sticky="w")
    typeLabel = Label(page, text="Meal:")
    typeLabel.grid(row=6, column=0, sticky="w")
    mealTypes = ["Breakfast", "Lunch", "Dinner", "Other"]
    typeOptions = StringVar()
    typeOptions.set(mealTypes[3])
    typeMenu = OptionMenu(page, typeOptions, *mealTypes)
    typeMenu.grid(row=6, column=1, sticky="w")
    foodsLabel = Label(page, text="Foods (comma list):")
    foodsLabel.grid(row=7, column=0, sticky="w")
    foods = Entry(page)
    foods.grid(row=7, column=1, sticky="w")
    createButton = Button(page, text="Create", command=lambda:create_food_record(date.get(), time.get(), duration.get(), typeOptions.get(), foods.get(), foodList))
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
