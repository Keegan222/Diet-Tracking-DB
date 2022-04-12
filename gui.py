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

def create_account(first_name, middle_name, last_name, email, password):
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
    createButton = Button(page, text="Create", bg="white", command=lambda: set_error_label(error_label, create_account(first_name.get(), middle_name.get(), last_name.get(), email.get(), password.get())))
    createButton.grid(column = 3, row = 3, sticky="w")

def create_food(food_name, food_category, calories, sugars, fats, food_ids):
    global db
    cursor = db.cursor()

    # Submit SQL command to add this food
    sql = "INSERT INTO food (food_name, food_category, calories, sugars, fats) VALUES (%s, %s, %s, %s, %s)"
    values = (food_name, food_category, calories, sugars, fats)
    cursor.execute(sql, values)
    db.commit()

    #Get the food id and add to list
    cursor.execute("SELECT @@identity")
    food_ids.append(cursor.fetchone()[0])

def create_food_record(date, time, duration, mealType, foodIds, listBox):
    global db
    cursor = db.cursor()

    # Convert food id list to comma seperated list
    id_list = ",".join(map(str, foodIds))

    # Submit SQL command to add this food record
    sql = "INSERT INTO food_records (owner_email, date, start_time, duration, meal_type, food_ids) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (userEmail, date, time, duration, mealType, id_list)
    cursor.execute(sql, values)
    db.commit()

    # Reset food ids and update records
    foodIds.clear()
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

def toggle_premium():
    global premium
    premium = not premium
    change_page(user_page)

def analyze_food(food_list, analysis_label):
    global db
    cursor = db.cursor()
    
    #Get the id of the currently selected food record
    record_id = food_list.get(food_list.curselection())[0]

    #Check if analysis already exists for food record
    #If so, just display the record
    cursor.execute("SELECT calories, fats, sugars FROM food_analysis WHERE record_id = %s", (record_id,))
    if (result := cursor.fetchone()):
        print(result)
        label_text = "Calories: " + str(result[0]) + "g Fats: " + str(result[1]) + "g Sugars: " + str(result[2]) + "g"
        analysis_label.config(text = label_text)
        return

    #Get the food entries from the food record
    cursor.execute("SELECT food_ids FROM food_records WHERE id_number = %s", (record_id,))
    food_ids = cursor.fetchall()

    #Calculate the totals for each food id
    calories = 0
    fats = 0
    sugars = 0
    for food_id in food_ids:
        cursor.execute("SELECT calories, fats, sugars FROM food WHERE id_number = %s", food_id)
        result = cursor.fetchone()

        calories += result[0]
        fats += result[1]
        sugars += result[2]
        
    #Create the analysis entry
    sql = "INSERT INTO food_analysis (record_id, calories, fats, sugars) VALUES (%s, %s, %s, %s)"
    values = (record_id, calories, fats, sugars)
    cursor.execute(sql, values)
    db.commit()

    #Display the entry
    label_text = "Calories: " + str(calories), + "Fats: " + str(fats) + "Sugars" + str(sugars)
    analysis_label.config(text = label_text)    

def user_page(root):
    global db, premium
    page = Frame(root)
    page.grid()

    cursor = db.cursor()

    #maybe create different pages for these sections / users

    #user:

    #View normal food intake record
    foodListLabel = Label(page, text="Food Intake Records")
    foodListLabel.grid(row=0, column=0, sticky="ew")
    foodList = Listbox(page, width=150, bg="white")
    foodList.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Refresh once initially
    get_food_records(foodList)

    #Create food id list
    foodIds = []

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
    intakeButton = Button(page, text="Create Food Intake Record", command=lambda:create_food_record(date.get(), time.get(), duration.get(), typeOptions.get(), foodIds, foodList))
    intakeButton.grid(row=7, column=1, sticky="w")

    #Create food record
    foodLabel = Label(page, bg="white", text="Add Food Record")
    foodLabel.grid(row=8, column=0, sticky="w")

    foodNameLabel = Label(page, text="Food Name:")
    foodNameLabel.grid(row=9, column=0, sticky="w")    
    foodName = Entry(page)
    foodName.grid(row=9, column=1, sticky="w")

    foodCategoryLabel = Label(page, text="Food Category:")
    foodCategoryLabel.grid(row=10, column=0, sticky="w")
    foodCategories = ["Vegetables and Fruit", "Grain Products", "Milk Products", "Meat and Alternatives", "Fats, Oils, and Sweets"]
    foodOptions = StringVar()
    foodOptions.set(foodCategories[4])
    foodMenu = OptionMenu(page, foodOptions, *foodCategories)
    foodMenu.grid(row=10, column=1, sticky="w")

    caloriesLabel = Label(page, text="Calories (g):")
    caloriesLabel.grid(row=11, column=0, sticky="w")
    calories = Entry(page)
    calories.grid(row=11, column=1, sticky="w")

    sugarsLabel = Label(page, text="Sugars (g):")
    sugarsLabel.grid(row=12, column=0, sticky="w")
    sugars = Entry(page)
    sugars.grid(row=12, column=1, sticky="w")

    fatsLabel = Label(page, text="Fats (g):")
    fatsLabel.grid(row=13, column=0, sticky="w")
    fats = Entry(page)
    fats.grid(row=13, column=1, sticky="w")

    foodButton = Button(page, text="Add Food Record", command=lambda:create_food(foodName.get(), foodOptions.get(), calories.get(), sugars.get(), fats.get(), foodIds))
    foodButton.grid(row=14, column=1, sticky="w")

    if premium:
        # Enable goal button
        goalButton = Button(page, text="Goals", bg="white", command=lambda:change_page(goal_page))
        goalButton.grid(row=16, column=0, sticky="w")

        #Create analysis label
        analysisLabel = Label(page, text="")
        analysisLabel.grid(row=17, column=1, sticky="w")

        #Enable food analysis
        analysisButton = Button(page, text="Analyze", bg="white", command=lambda:analyze_food(foodList, analysisLabel))
        analysisButton.grid(row=16, column=1, sticky="w")

        

        

        

    # Sign out of account
    signOutButton = Button(page, text="Sign Out", bg="white", command=lambda:change_page(login_page))
    signOutButton.grid(row=17, column=0, sticky="w")

    #Create toggle premium button
    premiumButton = Button(page, text="Toggle Premium", bg="white", command=lambda:toggle_premium())
    premiumButton.grid(row=15, column=0, sticky="w")

def create_goal(start_date, end_date, goal_type, nutrition_category, lower_bound, upper_bound, list_box):
    global db, userEmail
    cursor = db.cursor()

    # Submit SQL command to add this goal record
    sql = "INSERT INTO goal_records (owner_email, start_date, end_date, goal_type, nutrition_category, lower_bound, upper_bound) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (userEmail, start_date, end_date, goal_type, nutrition_category, lower_bound, upper_bound)
    cursor.execute(sql, values)
    db.commit()

    # Update goal records
    get_goal_records(list_box)

def get_goal_records(goalList):
    global db
    cursor = db.cursor()

    goalList.delete(0, END)

    # Submit SQL command to get food records for signed in email.
    recordsList = []
    cursor.execute("SELECT * FROM goal_records WHERE owner_email = %s", (userEmail,))
    result = cursor.fetchone()
    while result != None:
        recordsList.append(result)
        result = cursor.fetchone()

    i = 1
    for record in recordsList:
        goalList.insert(i, record)
        i += 1
    
def goal_page(root):
    page = Frame(root)
    page.grid()

    #Create goal display
    goalListLabel = Label(page, text="Goal Records")
    goalListLabel.grid(row=0, column=0, sticky="ew")
    goalList = Listbox(page, width=150, bg="white")
    goalList.grid(row=1, column=0, columnspan=2, sticky="ew")

    #Update list
    get_goal_records(goalList)
    
    #Create goal
    goalLabel = Label(page, bg="white", text="Create Goal")
    goalLabel.grid(row=2, column=0, sticky="w")

    dateStartLabel = Label(page, text="Start Date (YYYY/MM/DD): ")
    dateStartLabel.grid(row=3, column=0, sticky="w")
    dateStart = Entry(page)
    dateStart.grid(row=3, column=1, sticky="w")

    dateEndLabel = Label(page, text="End Date (YYYY/MM/DD): ")
    dateEndLabel.grid(row=4, column=0, sticky="w")
    dateEnd = Entry(page)
    dateEnd.grid(row=4, column=1, sticky="w")

    goalTypeLabel = Label(page, text="Goal Type:")
    goalTypeLabel.grid(row=5, column=0, sticky="w")
    goalCategories = ['Total amount of a nutrition type under a value','Total amount of a nutrition type over a value','Total amount of a nutrition type within a range','Total occurrences of a food category in meals over a certain value','Total occurrences of a food category in meals under a certain value','Total occurrences of a food category in meals within a range']
    goalOptions = StringVar()
    goalOptions.set(goalCategories[5])
    goalMenu = OptionMenu(page, goalOptions, *goalCategories)
    goalMenu.grid(row=5, column=1, sticky="w")

    categoryLabel = Label(page, text="Goal Category:")
    categoryLabel.grid(row=6, column=0, sticky="w")
    categoryCategories = ['Vegetables and Fruit','Grain Products','Milk Products','Meat and Alternatives','Fats, Oils, and Sweets','Calories','Sugars','Fats']
    categoryOptions = StringVar()
    categoryOptions.set(categoryCategories[7])
    categoryMenu = OptionMenu(page, categoryOptions, *categoryCategories)
    categoryMenu.grid(row=6, column=1, sticky="w")

    lowerLabel = Label(page, bg="white", text="Lower Value:")
    lowerLabel.grid(row=7, column=0, sticky="w")
    lower = Entry(page)
    lower.grid(row=7, column=1, sticky="w")

    upperLabel = Label(page, bg="white", text="Upper Value:")
    upperLabel.grid(row=8, column=0, sticky="w")
    upper = Entry(page)
    upper.grid(row=8, column=1, sticky="w")

    #Create goal button
    goalButton = Button(page, text="Create Goal", bg="white", command=lambda:create_goal(dateStart.get(), dateEnd.get(), goalOptions.get(), categoryOptions.get(), lower.get(), upper.get(), goalList))
    goalButton.grid(row=9, column=0, sticky="w")

    #Create back button
    backButton = Button(page, text="Back", bg="white", command=lambda:change_page(user_page))
    backButton.grid(row=10, column=0, sticky="w")

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

# Declare signed in user's email and premium status
userEmail = ""
premium = False

#Create GUI
root = Tk()
root.title("Diet Tracking Database")
root.geometry("720x565")
root.config(bg = "gray")

#Go to login page
login_page(root)

#Start main loop
root.mainloop()
