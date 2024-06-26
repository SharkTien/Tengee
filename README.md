# TENGEE 

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-blue?style=flat-square)](https://sharktien.github.io/tengee/)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](#LICENSE)

## illustrate


**⚠️ This project has been suspended for maintenance, and the archived code is for education purpose only and may not be used for commercial purposes**

**⚠️ This project has been suspended for demo idea. There is no any database systems**

The courses search solution supports searching and register to courses from the following data: (https://github.com/SharkTien/tengee/data)

The data is not called to API interface of any website.

## Download & Installation

[📦 Download the development version]()

**Setup graphic library**
```
pip install pyqt5
```

## demo & Features

If there is anything that needs to be improved, please submit a [Pull Requests](https://github.com/SharkTien/tengee/pulls)

### Week1 
### Day 1: 
#### ✨ PYQT5 (tools for combine python + html/css(.ui, .qrc)) tools for graphic
##### [Link Document](https://pypi.org/project/PyQt5/)
#### ✨ Loading screen
##### +   There is no event load during this stage (J4F😂) because of the lack of database.
#### ✨ Login/Register Screen
##### +   Login Screen: check login requirements.
##### +   Register Screen: check register requirements. Users can choose between 2 roles: Student/ Teacher
#####        
######   Data format: {'accountname':'password','username','1 (teacher) / 0 (student)'}
######   Data file: data_users.dat, users.dat
######
#####   This data can be easily organized with a database
#####
### Day 2:
#### ✨ Home Screen:
##### +   Home page <- 'Home' button
##### +   Account page <- 'Account settings' button
######    Users are allowed to change username, password
######    Creditcard: comming soon
##### +   'Logout' button -> Login Screen
### Week 2:
#### ✨ Improve Class Diagram and Data Structures. 
##### + Add [data_init.py](https://github.com/SharkTien/Tengee/blob/main/data_init.py) storing data structures
### Week 3:
### Day 1:
#### ✨ Home Screen update - Courses management system: 
##### + Add Courses Management page <- 'Courses management' button
#####   Show created courses
#####   Edit Courses page <- 'Edit' button on Cards
### Day 2: 
##### + Add Courses Management Function
#####   1. Add custom image source from user's directory with shutil library
#####   2. Create new course <- 'Add course' button on Courses Management tab
##### ✨ Details Course Screen
##### + Add details view <- 'Enroll' button on Cards
##### + Add data structure storing Bank information
#### Day 3:
##### ✨ Purchasing Screen
##### + Add Purchasing Page to show Bank information of authors <- Buy now
##### + Require Student to type Cardholdername in Purchasing form in order to convenience in detecting banking bill for Teacher
##### ✨ Notifications Screen
##### + Add an information card design
##### + Teacher can accept and reject students' registration through notifications  
##### + Students are notified that their orders are accepted or rejected
##### ✨ YourCourses Screen
##### + Display accepted courses for students
##### + Enrolled courses displaying in Home Screen will be marked as 'Enrolled'

## disclaimer

1. The mp3 files of this site are from Youtube, and the code of this project is only for academic exchange.
2. The video copyright comes from Youtube, and this site only provides data query services, and does not provide any video storage and sales services.
3. This project shall not be used for commercial purposes, and any infringement has nothing to do with the code contributors

## Open-source protocol

The MIT License (MIT)
