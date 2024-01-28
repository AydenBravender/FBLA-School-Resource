# FBLA-School-Resource

## Overview

For the 2024 FBLA Canadian Competition, the challenge was: 

"Create a program that allows your school’s Career and Technical Education Department to collect and store information about business and community partners. This program should include information on at least 25 different partners (real or fictional), with details such as, but not limited to, the type of organization, resources available, and direct contact information for an individual. The program should enable users to search and filter the information as needed." 

My response to this task was to create a GUI using customtkinter and Python. The database would be stored in two seperate locations, a google sheets and a SQL databse. I also included additional features such as generating a report, and displaying pie charts of the data and more.

## Data Storage

### Data Type

Each row of data is stored as an object of the ```SchoolResource``` class, which has the following properties ```name, type, resource, website, gmail, phone``` this row is then transfered into a list before being intergrated into google sheets, and it is transferred into a dictonary before being added to SQLITE3.
### Google Sheets

Google sheets makes a great backup data storage option due to it being saved to the cloud, and how it allows administrative priveliges to the owner account to share the sheets to other groups, ie student council. 

### SQLITE3

SQL is the main form of storage for this application. This is because of the ease and time it takes to find, append and remove objects from a SQL table. 

## User Interface

### Window

### Widgets


## Features

### Report

### Graphs
