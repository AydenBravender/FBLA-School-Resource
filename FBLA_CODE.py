import customtkinter
from PIL import Image 
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Frame
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import time
import csv
from datetime import datetime

matplotlib.use("TkAgg")

# ------------------ Setting up SQL -----------------------
conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='resources'")
if not c.fetchone():
    c.execute("""CREATE TABLE resources (
          name text,
          type text,
          resource text,
          website text,
          gmail text,
          phone text  
          )""") 


# ------------------ Setting up google sheets API -----------------------           
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\Bravender\\Desktop\\FBLA\\data\\secret_key.json", scopes=scope)
client = gspread.authorize(creds)
spreadsheet = client.open("python_sheet")
worksheet = spreadsheet.sheet1


# Class for all school resources
class SchoolResource:

    def __init__(self, name='N/A', type='N/A', resource='N/A', website='N/A', gmail='N/A', phone='N/A'):
        self.name = name
        self.type = type
        self.resource = resource
        self.website = website
        self.gmail = gmail
        self.phone = phone

    def __repr__(self):
        return "SchoolResource('{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.name, self.type, self.resource, self.website, self.gmail, self.phone)




# -------------------------------- Window Settings ------------------------------

customtkinter.set_appearance_mode("dark")  
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk() 
app.title("FBLA FINDER")

# center the Gui on opening
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
# Adjust for the title bar height
title_bar_height = app.winfo_toplevel().winfo_height() - app.winfo_height()
x_coordinate = (screen_width - 1400) // 2
y_coordinate = (screen_height - 800 - title_bar_height) // 2
app.geometry(f"1500x800+{x_coordinate}+{y_coordinate-25}")


def on_closing():
    # Close Matplotlib figures
    if frame:
        frame.destroy()
        plt.close('all')
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)


# ----------------------------------- Images ------------------------------------




image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
# Resize and create a CTkImage instance
search_resized_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "9349901.png")), size=(25, 25))




# ----------------------------------- Functions ----------------------------------



def update_function():
    global conn  # making sure that all of the code can access variable conn
    scrollable_frame_function()
    conn.close()
    try:
        os.remove("C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db")  # remove file
    except PermissionError as e:
        print(f"PermissionError: {e}. The file is still in use by another process.")

    conn = sqlite3.connect("C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db")  # reopen the connection
    c = conn.cursor()
    c.execute("""CREATE TABLE resources (
          name text,
          type text,
          resource text,
          website text,
          gmail text,
          phone text  
          )""")  # adding table to database

    try:
        values = worksheet.get_all_values()  # Get all values from the google sheet
    except gspread.exceptions.APIError as e:
        print("APIError occurred:", e)
        print("too much data on google sheets, please pay for a higher API limit")


    # Skip the first row (the header)
    values = values[1:]
    for row in values:
        # checks for duplicates by searching in the SQL database for each value,
        c.execute("SELECT * FROM resources WHERE name=:name AND type=:type AND resource=:resource AND website=:website AND gmail=:gmail AND phone=:phone",
                  {'name': row[0],
                   'type': row[1],
                   'resource': row[2],
                   'website': row[3],
                   'gmail': row[4],
                   'phone': row[5]})

        # Fetch all matching rows
        rows = c.fetchall()
        # checks that the row we are adding isn't already present in the database
        if not rows:
            try:
                with conn:
                    c.execute("INSERT INTO resources VALUES (:name, :type, :resource, :website, :gmail, :phone)",
                              {'name': row[0],
                               'type': row[1],
                               'resource': row[2],
                               'website': row[3],
                               'gmail': row[4],
                               'phone': row[5]})
            except IndexError:
                print("Invalid data on google sheets, please make sure the data is correct")
    conn.commit()


def add_row_function():
    global conn  # making sure that all of the code can access variable conn
    obj = SchoolResource(name_entry.get(), 
                         optionmenu_type_add_row.get(), 
                         optionmenu_resources_add_row.get(), 
                         website_entry.get(), gmail_entry.get(), 
                         phone_entry.get())
    
    local_conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')
    c = local_conn.cursor()

    # check if the resource is already in google sheets
    try:
        records = worksheet.get_all_records()
    except gspread.exceptions.APIError as e:
        time.sleep(100)  # Sleep for 100 seconds
        records = worksheet.get_all_records()
    
    # Iterate over each record (row) in the worksheet
    for record in records:
        # Convert the record to a dictionary
        record_dict = dict(record)
        # Compare the record dictionary with the defined dictionary
        if record_dict == {'name': obj.name, 'Organization_type': obj.type, 
                           'resources_available': obj.resource, 
                           'website': obj.website, 
                           'gmail': obj.gmail, 
                           'phone': obj.phone}: 
            # Convert phone to int() if it doesn't contain '-' dashes.
            name_entry.delete(0, customtkinter.END)
            optionmenu_type_add_row.set("type")
            optionmenu_resources_add_row.set("resources")
            website_entry.delete(0, customtkinter.END)
            gmail_entry.delete(0, customtkinter.END)
            phone_entry.delete(0, customtkinter.END)
            local_conn.close()
            scrollable_frame_function()
            return
    
    with local_conn:
        c.execute("INSERT INTO resources VALUES (:name, :type, :resource, :website, :gmail, :phone)", 
                  {'name': obj.name, 'type': obj.type, 
                   'resource': obj.resource, 
                   'website': obj.website, 
                   'gmail': obj.gmail, 
                   'phone': obj.phone})
        
    try:
        # adding row to google sheets
        SQL_dict = {'name': obj.name, 'type': obj.type, 'resource': obj.resource, 'website': obj.website, 'gmail': obj.gmail, 'phone': obj.phone}
        # Append the list of values to the sheet
        worksheet.append_row(list(SQL_dict.values()))
    
    except gspread.exceptions.APIError as e:
        print("APIError occurred:", e)
        print("Sleeping for 100 seconds...")
        time.sleep(100)  # Sleep for 100 seconds
        print("Retrying to append the row...")
        # adding row to google sheets
        SQL_dict = {'name': obj.name, 'type': obj.type, 'resource': obj.resource, 'website': obj.website, 'gmail': obj.gmail, 'phone': obj.phone}
        # Append the list of values to the sheet
        worksheet.append_row(list(SQL_dict.values()))
    
    name_entry.delete(0, customtkinter.END)
    optionmenu_type_add_row.set("type")
    optionmenu_resources_add_row.set("resources")
    website_entry.delete(0, customtkinter.END)
    gmail_entry.delete(0, customtkinter.END)
    phone_entry.delete(0, customtkinter.END)
    scrollable_frame_function()
    local_conn.close()



def search_function():
    conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')  # reopen the connection
    c = conn.cursor()
    result_list = []  # Initialize an empty list to store results

    if optionmenu_resources.get() == 'All':
        if optionmenu_type.get() == 'All':
            c.execute(
                "SELECT * FROM resources WHERE (name LIKE ? OR website LIKE ? OR gmail LIKE ? OR phone LIKE ?)",
                ('%' + search_entry.get() + '%', '%' + search_entry.get() + '%', '%' + search_entry.get() + '%',
                 '%' + search_entry.get() + '%'))
        else:
            c.execute(
                "SELECT * FROM resources WHERE (name LIKE ? OR website LIKE ? OR gmail LIKE ? OR phone LIKE ?) AND type = ?",
                ('%' + search_entry.get() + '%', '%' + search_entry.get() + '%', '%' + search_entry.get() + '%',
                 '%' + search_entry.get() + '%', optionmenu_type.get()))
    elif optionmenu_type.get() == 'All':
        c.execute(
            "SELECT * FROM resources WHERE (name LIKE ? OR website LIKE ? OR gmail LIKE ? OR phone LIKE ?) AND resource = ?",
            ('%' + search_entry.get() + '%', '%' + search_entry.get() + '%', '%' + search_entry.get() + '%',
             '%' + search_entry.get() + '%', optionmenu_resources.get()))
    else:
        c.execute(
            "SELECT * FROM resources WHERE (name LIKE ? OR website LIKE ? OR gmail LIKE ? OR phone LIKE ?) AND resource = ? AND type = ?",
            ('%' + search_entry.get() + '%', '%' + search_entry.get() + '%', '%' + search_entry.get() + '%',
             '%' + search_entry.get() + '%', optionmenu_resources.get(), optionmenu_type.get()))

    result_list = c.fetchall()  # Fetch all the results and store in result_list
    # print("Search Results:", result_list)
    conn.close()
    return result_list  # Return the list of results


def delete(obj):
    conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')
    c = conn.cursor()
    with conn:
        c.execute("""DELETE FROM resources WHERE name = :name AND type = :type AND 
                resource = :resource AND website = :website AND 
                gmail = :gmail AND phone = :phone""", 
                {'name': obj.name, 
                'type': obj.type, 
                'resource': obj.resource, 
                'website': obj.website, 
                'gmail': obj.gmail, 
                'phone': obj.phone})
    
    records = worksheet.get_all_records()

    # Define the content to match
    # ensure they are the same data type ex. '5' != 5
    content_to_match = {'name': obj.name, 'Organization_type': obj.type, 
            'resources_available': obj.resource, 
            'website': obj.website, 
            'gmail': obj.gmail, 
            'phone': str(obj.phone)}

    # List to store the indices of the rows to delete
    rows_to_delete = []

    # Iterate over each record (row) in the worksheet
    for i, record in enumerate(records, start=1):  # Change start to 1
        # If the content to match is in the record, add the index to the list
        # print(record, content_to_match)
        if record == content_to_match:
            rows_to_delete.append(i)

    # Delete the rows in reverse order (to avoid changing the indices of the remaining rows)
    for i in reversed(rows_to_delete):
        worksheet.delete_rows(i+1)
    conn.close()


def delete_function():
    list_to_delete = []
    # Identify selected items
    for i in range(len(checkbox_vars)):
        if checkbox_vars[i].get():
            list_to_delete.append(i)

    # print("LIST_TO_DELETE:", list_to_delete)
    result_list = scrollable_frame_function()

    # Delete selected items from the GUI
    for i in range(len(list_to_delete)):
        tuple_list = result_list[list_to_delete[i]]
        obj_delete = SchoolResource(*tuple_list)
        delete(obj_delete)


    # Update the displayed data after deletion
    scrollable_frame_function()

    
# Custom function to calculate the total number of characters in a nested list
# needed to calc reciprocal relation between character size and spacing in widget
def total_characters(nested_list):
    return sum(len(s) for s in nested_list)


def clear_scrollable_frame(scrollable_frame):
    # Destroy all widgets in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
        

def scrollable_frame_function(*args):
    graph()
    global checkbox_vars
    # Clear the existing content of the scrollable frame
    try:
        clear_scrollable_frame(scrollable_frame)
    except NameError:
        pass

    results = search_function()
    checkbox_vars = []

    # finding the relation between the longest data row, and the padding it requires

    # Find the nested list with the maximum total number of characters
    try:
        max_nested_list = max(results, key=total_characters)
        max_total_characters = total_characters(max_nested_list)
    except ValueError or TypeError:
        max_total_characters = 0
        
    # Calculate the total number of characters in the max_nested_list
    

    first = (-26/140)*max_total_characters + 148.37
    major = (-36/140)*max_total_characters + 200.16
    mid =  (-30/140)*max_total_characters + 170.67
    # print(f"first {first} major {major} mid {mid} char {max_total_characters}")
    # Set custom width for each column
    column_widths = {0: 40, 1: first, 2: major, 3: major, 4: major, 5: mid, 6: major}

    for col, width in column_widths.items():
        scrollable_frame.columnconfigure(col, minsize=width)

    for i in range(len(results)):
        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][0], anchor="w")
        label.grid(row=i, column=1, padx=0, pady=5, sticky="ew")

        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][1], anchor="w")
        label.grid(row=i, column=2, padx=0, pady=5, sticky="ew")

        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][2], anchor="w")
        label.grid(row=i, column=3, padx=0, pady=5, sticky="ew")

        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][3], anchor="w")
        label.grid(row=i, column=4, padx=0, pady=5, sticky="ew")

        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][4], anchor="w")
        label.grid(row=i, column=5, padx=0, pady=5, sticky="ew")

        label = customtkinter.CTkLabel(scrollable_frame, text=results[i][5], anchor="w")
        label.grid(row=i, column=6, padx=0, pady=5, sticky="ew")

        checkbox_var = customtkinter.BooleanVar()
        checkbox_vars.append(checkbox_var)

        checkbox = customtkinter.CTkCheckBox(scrollable_frame, text="", variable=checkbox_var)
        checkbox.grid(row=i, column=0, padx=0, pady=0, sticky="w")

    conn.close()
    return results


def create_report(): # creates a report that can be printed
    # backend
    conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')
    c = conn.cursor()
    # Execute a query to get all rows from the table
    c.execute("SELECT * FROM resources")
    # Fetch all rows as a list of tuples
    rows = c.fetchall()

    now = datetime.now()
    # Save the date and year into variables
    date = now.strftime("%Y-%m-%d")  # format: YYYY-MM-DD
    year = now.year

    # frontend
    dialog = customtkinter.CTkInputDialog(text="Type in the Directory You Want to Save the Report In:", title="Report")
    text = dialog.get_input()  # waits for input
    if text:
        with open(text, 'w', newline='') as file:
            file.write(f"Date: {date} Year: {year}\n\n")
            writer = csv.writer(file)
            writer.writerows(rows)

# ------------------------------------ Graphs -------------------------------------

# The graph function displays 2 pie chart showing which types of business, and resources available

def graph():
    frame = None  # Initialize frame to None
    conn = sqlite3.connect('C:\\Users\\Bravender\\Desktop\\FBLA\\FBLA-School-Resource\\schoolresources.db')  # reopen the connection
    c = conn.cursor()

    # first pie chart
    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'Other';")
    other_result = c.fetchone()[0] # counting total of each category to display data on the pie chart

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'N/A';")
    na_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'Organization';")
    organization_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'Careers';")
    careers_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'Company';")
    company_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE type = 'Non-Profit';")
    nonprofit_result = c.fetchone()[0]

    # second pie chart
    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'Other';")
    other_resource_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'N/A';")
    na_resource_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'Certification';")
    certification_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'Internship';")
    internship_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'Funding';")
    funding_result = c.fetchone()[0]

    c.execute("SELECT COUNT(*) AS total_count FROM resources WHERE resource = 'Courses';")
    courses_result = c.fetchone()[0]

    conn.close() # close the connection


    def create_frame_resources():
        global frame
        frame = Frame(app)
        frame.place(x=1160, y=100, height=300, width=300)  # placing the graph at a certain position

        fig = plt.Figure(facecolor='#2b2b2b')  # Set the background color of the figure using hexcode
        ax = fig.add_subplot(111)

        # Data for the pie chart
        labels = ['Funding', 'Internship', 'Courses', 'N/A', 'Other', 'Certification']
        sizes = [funding_result+1, internship_result+1, courses_result+1, na_resource_result+1, other_resource_result+1, certification_result+1]  # Make sure the sizes list has the same length as the labels list
        colors = ['#1f6aa5', '#265f8f', '#1a466f', '#1d4f7e', '#1b3e68']  # Set colors for pie chart slices using hexcodes
        try: 
            # Create a pie chart on the Axes
            ax.pie(sizes, labels=labels, startangle=90, colors=colors, textprops={'color': 'white', 'fontsize': 6})

            # Title of the pie chart
            ax.set_title('Distribution of Resources', color='white', fontsize=12)  # Set title color and fontsize
            # Embed the Matplotlib plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        except ValueError:
            pass


    def create_frame_type():
        global frame
        frame = Frame(app)
        frame.place(x=1160, y=400, height=300, width=300)  # Adjust the height and width as needed

        # Create a Figure and Axes directly without using plt.subplots
        fig = plt.Figure(facecolor='#2b2b2b')  # Set the background color of the figure using hexcode
        ax = fig.add_subplot(111)

        # Data for the pie chart
        labels = ['Company', 'Non-Profit', 'Careers', 'N/A', 'Other', 'Organization']
        sizes = [company_result+1, nonprofit_result+1, careers_result+1, na_result+1, other_result+1, organization_result+1]  # Make sure the sizes list has the same length as the labels list
        colors = ['#1f6aa5', '#265f8f', '#1a466f', '#1d4f7e', '#1b3e68']  # Set colors for pie chart slices using hexcodes
        try:  # error handling if there is no data to begin with
            # Create a pie chart on the Axes
            ax.pie(sizes, labels=labels, startangle=90, colors=colors, textprops={'color': 'white', 'fontsize': 6})

            # Title of the pie chart
            ax.set_title('Distribution of Types', color='white', fontsize=12)  # Set title color and fontsize
            # Embed the Matplotlib plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1)
        except ValueError:
            pass # it will display white rectangle where graphs used to be

    create_frame_type()
    create_frame_resources()

# ------------------------------------- Buttons -------------------------------------


update_button = customtkinter.CTkButton(master=app, text="UPDATE", command=update_function)
update_button.place(x=1250, y=30)

delete_button = customtkinter.CTkButton(master=app, text="DELETE", command=delete_function)
delete_button.place(x=1100, y=30)

add_row_button = customtkinter.CTkButton(master=app, text="ADD ROW", height=40, width=200, command=add_row_function)
add_row_button.place(x=10, y=745)

create_report_button = customtkinter.CTkButton(master=app, text="CREATE REPORT", height=30, width=150, command=create_report)
create_report_button.place(x=1300, y=750)

search_button = customtkinter.CTkButton(app, image=search_resized_image, command=scrollable_frame_function, text="", width=20, height=40)
search_button.place(x=40, y=20)


# ---------------------------------------- Labels ---------------------------------------


filter_label = customtkinter.CTkLabel(app, text="FILTER:", font=("Helvetica", 18, 'bold'))
filter_label.place(x=600, y=30)

type_label = customtkinter.CTkLabel(app, text="Type:", font=("Helvetica", 14))
type_label.place(x=800, y=5)

resources_label = customtkinter.CTkLabel(app, text="Resources:", font=("Helvetica", 14))
resources_label.place(x=900, y=5)

column_names_label = customtkinter.CTkLabel(app, text="NAME:                           TYPE:                             RESOURCES:                            WEBSITE:                              GMAIL:                               PHONE:", 
                                            font=("Helvetica", 16))
column_names_label.place(x=110, y = 80)


# ------------------------------------- Option Menus -------------------------------------

type_list_add = ['Company', 'Non-Profit', 'Careers', 'Organization', 'Other', 'N/A']
resources_list_add = ['Funding', 'Internship', 'Courses', 'Certification', 'Other', 'N/A']

type_list = ['Company', 'Non-Profit', 'Careers', 'Organization', 'Other', 'N/A', 'All']
resources_list = ['Funding', 'Internship', 'Courses', 'Certification', 'Other', 'N/A', 'All']


optionmenu_type = customtkinter.CTkOptionMenu(app, values=type_list, command=scrollable_frame_function)
optionmenu_type.set("All")
optionmenu_type.place(x=750, y=30)

optionmenu_resources = customtkinter.CTkOptionMenu(app, values=resources_list, command=scrollable_frame_function)
optionmenu_resources.set("All")
optionmenu_resources.place(x=900, y=30)

optionmenu_resources_add_row = customtkinter.CTkOptionMenu(app, values=resources_list_add)
optionmenu_resources_add_row.set("resources")
optionmenu_resources_add_row.place(x=540, y=750)

optionmenu_type_add_row = customtkinter.CTkOptionMenu(app, values=type_list_add)
optionmenu_type_add_row.set("type")
optionmenu_type_add_row.place(x=380, y=750)


# ----------------------------------------- Entrys ---------------------------------------


search_entry = customtkinter.CTkEntry(app, placeholder_text="Search", height=40, width=300, font=("Helvetica", 18))
search_entry.place(x=80, y=20)

name_entry = customtkinter.CTkEntry(app, placeholder_text="name", height=30, width=150, font=("Helvetica", 14))
name_entry.place(x=220, y=750)

website_entry = customtkinter.CTkEntry(app, placeholder_text="website", height=30, width=150, font=("Helvetica", 14))
website_entry.place(x=700, y=750)

gmail_entry = customtkinter.CTkEntry(app, placeholder_text="gmail", height=30, width=150, font=("Helvetica", 14))
gmail_entry.place(x=860, y=750)

phone_entry = customtkinter.CTkEntry(app, placeholder_text="phone", height=30, width=150, font=("Helvetica", 14))
phone_entry.place(x=1020, y=750)


# --------------------------------- Scrollable Frame/Widgets -------------------------------


scrollable_frame = customtkinter.CTkScrollableFrame(app, width=1120, height=600)
scrollable_frame.place(x=10, y=125)
checkbox_vars = []
scrollable_frame_function() # Initial call to populate the scrollable frame

app.mainloop()