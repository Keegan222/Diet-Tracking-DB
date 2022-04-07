import mysql.connector
from tkinter import *

def login(email, password):
    global db, current_email
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

    # Set global email variable
    current_email = email

    #Change scene to user page
    change_page(user_page)

    return "Success"

def create(first_name, middle_name, last_name, email, password):
    global db, current_email
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
    current_email = email

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

#Create global email variable
current_email = ""

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
