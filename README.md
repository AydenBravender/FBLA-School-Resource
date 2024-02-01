# FBLA-Finder

## Overview

This project was developed for the 2024 FBLA Canadian Competition. The challenge was to create a program that enables the Career and Technical Education Department of a school to collect and store information about business and community partners. The program was required to include information on at least 25 different partners, either real or fictional. The details included, but were not limited to, the type of organization, resources available, and direct contact information for an individual. Additionally, the program needed to provide users with the ability to search and filter the information as needed.

In response to this task, I created a Graphical User Interface (GUI) using customtkinter and Python. The data for this application is stored in two separate locations: Google Sheets and a SQL database. The application also includes additional features such as generating a report and displaying pie charts of the data.

// Image //

## Data Storage

### Data Type

Each row of data is stored as an object of the ```SchoolResource``` class, which has the following properties ```name```, ```type```, ```resource```, ```website```, ```gmail```, and  ```phone``` this row is then transfered into a list before being intergrated into google sheets, and it is transferred into a dictonary before being added to SQLITE3.

```name```: A string containing the organizations name

```type```: A string with the type of organization (Company, Non-Profit, Careers, N/A, Other, Organization)

```resource```: A string with the resources available via the organization (Funding, Internship, Courses, N/A, Other, Certification)

```website```: A string contaning the website

```gmail```: A string contaning the gmail

```phone```: A string contaning the phone number (Not an Integer)

### Data Storage In Google Sheets

Google Sheets serves as a backup data storage option due to its cloud-based nature and the ability to share the sheets with other groups, such as the student council, through administrative privileges of the owner account. In order to use this service I used the API availiable to sync the SQL database and the sheets.


### Data Storage In SQLITE3

SQLITE3 is the primary form of storage for this application. It was chosen for its efficiency and ease in finding, appending, and removing objects from a SQL table. SQL requests were made to prohibit the use of SQL intections through the use of place holders ```?```.

## Functions

### Update
Update the SQL database with data from google sheets. It removes duplicates in database.

### Add Row
The user can add a row to both the SQL database and google sheets in one step.

### Delete Row
checkboxes are found on each row of data, you can click which rows you want to delete, click the delete button and they are removed from both the SQL database as well as google sheets.

### Search
Using the search bar along side 2 filters for ```type``` and ```resource``` the user can effeciently search the entire database.

### Generating Report

The application can generate a custom report that outlines the date and details about business/community partners. This report is created as a .txt file in the user’s choice of directory.

### Data Visualization

The application provides data visualization in the form of two pie charts, created using matplotlib. These charts display the distribution of resources and types of organizations available to the school. This feature allows users to gain a quick understanding of the data at a glance.

## Advanced Features for FBLA Finder

FBLA Finder strongly encourages you to include advanced features such as:
### Gmail Linked Sign-in Page
To ensure a secure and personalized user experience, our platform could feature a sign-in/sign-up page linked to Gmail. This would allow users to create an account using their existing Gmail credentials. If a user does not have an account, an authorization request would be sent to the career center. Upon approval from the career center, the user would be able to sign in and access the platform’s resources.

### Large Language Model (LLM) FAQ Page
To further assist our users, we propose the implementation of a Frequently Asked Questions (FAQ) page. This page would feature a chatbot powered by a Large Language Model (LLM). The chatbot would be capable of answering a wide range of questions, providing instant support to students and teachers. This feature would not only enhance the user experience but also reduce the workload of the support team.

### Resource Specific Notes
Companies often have additional information that users may find useful. However, this data might not fit within the constraints of a scrollable widget. To address this, we suggest making each resource name a link that opens a new window containing editable information about the resource. This feature would allow users to access more detailed information about a company and customize the content according to their needs. This would be a valuable extension to the platform, providing users with a more comprehensive understanding of the resources available to them.