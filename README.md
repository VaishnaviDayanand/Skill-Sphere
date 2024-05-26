# Skill-Sphere
Skill Sphere is a Python desktop app for admin and user interactions with a user-friendly GUI. It uses `tkinter` for the interface and integrates with a MySQL database, offering secure login, signup, and user management. This application ensures a seamless and efficient user experience.

**Features:**

Admin Login: Secure access for administrators with password protection.
User Login/Signup: Easy user account creation and login capabilities.
Intuitive GUI: Clean and simple graphical user interface for ease of use.

**Technologies Used:**

Python: Core programming language used for the application logic.
tkinter: Python's standard GUI toolkit for creating the graphical interface.
Pillow: Python Imaging Library (PIL) for handling image resizing and manipulation.
MySQL: Relational database management system used for storing user data.

### Requirements

- Python 3.11
- Visual Studio Code (or any other code editor)
- MySQL Workbench

## Setup Instructions

### Step 1: Install Python 3.11

Make sure Python 3.11 is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Step 2: Install Visual Studio Code

Download and install Visual Studio Code from [here](https://code.visualstudio.com/).

### Step 3: Install Python extension in Visual Studio Code

Open Visual Studio Code and install the Python extension. You can find it in the Extensions view (Ctrl+Shift+X) and search for "Python".

### Step 4: Set up the MySQL database
Make sure MySQL is installed and running.
Create a database for the project:
  CREATE DATABASE skillsphere;
Update the database connection settings in the code (if necessary).

### Step 6: Import the database schema
Locate the schema.sql file included in the repository.
Import the schema into your MySQL database:
  mysql -u yourusername -p skillsphere < schema.sql
Replace yourusername with your MySQL username.

### Step 7: Ensure images are in place
Create an images folder in the root directory of the project.
Add the required background images to this folder. Ensure the images are named appropriately as referenced in your code.

### Step 8: Run the application
Run the following command in the terminal to start the application:
  main.py
