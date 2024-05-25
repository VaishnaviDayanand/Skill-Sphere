import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import ImageTk
from PIL import Image
import mysql.connector
import random

# Add a global variable to store the current user_id
current_user_id = None
admin_window = None

def resize_image(event):
    # Resize the image to fit the new window size
    new_width = event.width
    new_height = event.height
    resized_image = original_image.resize((new_width, new_height))
    # Update the label with the resized image
    img = ImageTk.PhotoImage(resized_image)
    label.config(image=img)
    label.image = img  # Keep a reference to avoid garbage collection

def generate_sid():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    while True:
        Sid = random.randint(100,999) # Generate a random 4-digit number for Sid
        query = "SELECT * FROM student WHERE Sid = %s"
        cursor.execute(query, (Sid,))
        result = cursor.fetchone()
        if not result: # If Sid doesn't exist in the database, break the loop
            break

    cursor.close()
    connection.close() 
    
    return Sid

def check_login(MailId, Pwd):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    query = "SELECT Sid FROM student WHERE MailId = %s AND Pwd = %s"
    cursor.execute(query, (MailId, Pwd))

    result = cursor.fetchone()


    cursor.close()
    connection.close()

    return result


def fetch_user_id(mail_id):
    # Add your logic to fetch the user_id from the database using the mail_id
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    query = "SELECT Sid FROM student WHERE MailId = %s"
    cursor.execute(query, (mail_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]
    else:
        return None
    # For now, return a placeholder value (replace it with your actual logic)
    return 1

def create_account_clicked(Name, Gender, Age, MailId, PhoneNo, CollegeName, Branch, Year, Semester, Pwd):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()
    Sid = generate_sid()
    query = "INSERT INTO student (Sid, Name, Gender, Age, MailId, PhoneNo, CollegeName, Branch, Year, Semester, Pwd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (Sid, Name.get(), Gender.get(), Age.get(), MailId.get(), PhoneNo.get(), CollegeName.get(), Branch.get(), Year.get(), Semester.get(), Pwd.get())
    
    try:
        cursor.execute(query, values)
        connection.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        global current_user_id
        current_user_id = fetch_user_id(MailId.get()) # Replace fetch_user_id with your logic

        on_successful_login()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    cursor.close()
    connection.close()
    
def login_clicked(MailId, Pwd, on_successful_login):
    result = check_login(MailId, Pwd)
    if result:
        user_id = result[0] # Assuming the user_id is the first column in the result
        messagebox.showinfo("Login Successful", "Welcome back!")
        on_successful_login(user_id)
    else:
        messagebox.showerror("Login Failed", "Invalid mail id or password")

#age validation       
def is_positive_integer(input_str):
    try:
        value = int(input_str)
        if value < 0:
            return False
        return True
    except ValueError:
        return False
    
def validate_phone_number(phone_number):
    # Remove any whitespace from the phone number
    phone_number = phone_number.replace(" ", "")
    
    # Check if the phone number contains only digits and is of length 10
    if phone_number.isdigit() and len(phone_number) <= 10:
        return True
    else:
        return False
            
def signup_clicked():
    def resize_bg_image(event):
            # Retrieve the updated window size
            window_width = signup_window.winfo_width()
            window_height = signup_window.winfo_height()

            # Resize the image to fit the window size
            resized_image = bg_image.resize((window_width, window_height))
            new_img = ImageTk.PhotoImage(resized_image)
            bg_label.configure(image=new_img)
            bg_label.image = new_img  # Keep a reference to the PhotoImage to prevent garbage collection

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry(full_screen_size)

    try:
        # Set background image
        path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\2.png"  # Change the path to your image
        bg_image = Image.open(path)

        # Place the label containing the image
        bg_label = tk.Label(signup_window)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Update the window to ensure it's fully initialized
        signup_window.update()

        # Bind the resize_bg_image function to the window's Configure event
        signup_window.bind("<Configure>", resize_bg_image)

        # Initially resize the background image to fit the window size
        resize_bg_image(None)

    except Exception as e:
        print(f"Error loading image: {e}")
        messagebox.showerror("Error", f"Failed to load image: {e}")


    frame = tk.Frame(signup_window)
    frame.pack(padx=20, pady=150)
    frame.configure(bg="light green")
    tk.Label(frame, text="Enter your details", font=("Helvetica", 14)).grid(row=0, column=1, columnspan=2, pady=10)

    tk.Label(frame, text="Full Name:").grid(row=1, column=0, pady=5)
    Name = tk.Entry(frame)
    Name.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="Gender:").grid(row=2, column=0, pady=5)
    var_gender = tk.StringVar(value="Male")
    tk.Radiobutton(frame, text="Male", variable=var_gender, value="M").grid(row=2, column=1, pady=5)
    tk.Radiobutton(frame, text="Female", variable=var_gender, value="F").grid(row=2, column=2, pady=5)
    tk.Radiobutton(frame, text="Other", variable=var_gender, value="Oth").grid(row=2, column=3, pady=5)

    tk.Label(frame, text="Age:").grid(row=3, column=0, pady=5)
    vcmd=(frame.register(is_positive_integer),"%P")
    Age=tk.Entry(frame, validate="key",validatecommand=vcmd)
    Age.grid(row=3, column=1, pady=5)

    tk.Label(frame, text="Mail ID:").grid(row=4, column=0, pady=5)
    MailId = tk.Entry(frame)
    MailId.grid(row=4, column=1, pady=5)

    tk.Label(frame, text="Phone Number:").grid(row=5, column=0, pady=5)
    vcmd = (frame.register(validate_phone_number), "%P")
    PhoneNo = tk.Entry(frame, validate="key", validatecommand=vcmd)
    PhoneNo.grid(row=5, column=1, pady=5)

    tk.Label(frame, text="College Name:").grid(row=6, column=0, pady=5)
    CollegeName = tk.Entry(frame)
    CollegeName.grid(row=6, column=1, pady=5)

    tk.Label(frame, text="Branch:").grid(row=7, column=0, pady=5)
    Branch = tk.Entry(frame)
    Branch.grid(row=7, column=1, pady=5)

    tk.Label(frame, text="Year:").grid(row=8, column=0, pady=5)
    year_var = tk.StringVar()
    year_combo = ttk.Combobox(frame, textvariable=year_var, values=["1", "2", "3", "4"])
    year_combo.grid(row=8, column=1, pady=5)

    tk.Label(frame, text="Semester:").grid(row=9, column=0, pady=5)
    semester_var = tk.StringVar()
    semester_combo = ttk.Combobox(frame, textvariable=semester_var, values=["1", "2", "3", "4", "5", "6", "7", "8"])
    semester_combo.grid(row=9, column=1, pady=5)


    tk.Label(frame, text="Password:").grid(row=10, column=0, pady=5)
    Pwd = tk.Entry(frame, show="*")
    Pwd.grid(row=10, column=1, pady=5)

    signupButton = tk.Button(frame, text="Sign Up",
                            command=lambda: create_account_clicked(
                                Name, var_gender, Age, MailId, PhoneNo, CollegeName, Branch, year_var, semester_var, Pwd
                            ))
    signupButton.grid(row=11, column=0, columnspan=2, pady=10)

    signup_window.mainloop()
    
def open_login_window():
    def on_successful_login(user_id):
        global current_user_id
        current_user_id = user_id
        root.withdraw()  # Hide the root window
        open_home_page()

    def resize_bg_image(event):
        try:
            # Resize the image to fit the window
            window_width = login_window.winfo_width()
            window_height = login_window.winfo_height()
            resized_bg = bg_image.resize((window_width, window_height))

            # Display the resized image as background
            bg_photo = ImageTk.PhotoImage(resized_bg)
            bg_label.config(image=bg_photo)
            bg_label.image = bg_photo
        except Exception as e:
            print(f"Error resizing background image: {e}")

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry(full_screen_size)
    login_window.configure(bg="dark blue")
    

    # Load the background image
    bg_path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\3.png"  # Update with your image path
    bg_image = Image.open(bg_path)
    print("Background image loaded successfully")

    # Display the image as background
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Bind the resize function to the window's Configure event
    login_window.bind("<Configure>", resize_bg_image)

    def increase_font(widget):
        widget.config(font=("roboto", 16))
    # Other login window elements
    main_frame = tk.Frame(login_window)
    main_frame.pack(pady=250)  # Adding padding to the main frame
    main_frame.configure(bg="dark blue")
    
    #main_frame.pack(anchor="center") 
    

    # MailId Label and Entry
    mailid_label = tk.Label(main_frame, text="Mail Id")
    mailid_label.pack(pady=(30, 5))  # Adding vertical padding
    increase_font(mailid_label)
    

    mailid_entry = tk.Entry(main_frame)
    mailid_entry.pack(pady=5)
    increase_font(mailid_entry)

    # Password Label and Entry
    password_label = tk.Label(main_frame, text="Password")
    password_label.pack(pady=5)
    increase_font(password_label)

    password_entry = tk.Entry(main_frame, show="*")
    password_entry.pack(pady=5)
    increase_font(password_entry)


    login_button = tk.Button(main_frame, text="Login",
                             command=lambda: login_clicked(mailid_entry.get(), password_entry.get(), on_successful_login))
    login_button.pack(pady=10)


    # Other login window elements



def open_home_page():
    global home_window  # Declare home_window as a global variable
    
    def on_close():
        home_window.destroy()

    def logout():
        global current_user_id
        current_user_id = None
        home_window.destroy()
        root.deiconify()

    if current_user_id is not None:
        home_window = tk.Toplevel(root) # Use Toplevel instead of Tk
        home_window.title("Skill Sphere")
        home_window.geometry(full_screen_size)
        home_window.resizable(False, False)  # Allow resizing both horizontally and vertically
        
        try:
            # Set background image
            path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\4.png"
            bg_image = Image.open(path)
            print("Image loaded successfully")
            
            # Create a label for the background image
            bg_label = tk.Label(home_window)
            bg_label.place(relwidth=1, relheight=1)

            # Function to resize the image
            def resize_image(event=None):
                # Retrieve the updated window size
                window_width = home_window.winfo_width()
                window_height = home_window.winfo_height()

                # Resize the image to fit the window size
                resized_image = bg_image.resize((window_width, window_height))
                img = ImageTk.PhotoImage(resized_image)
                bg_label.config(image=img)
                bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
            
            # Bind the resize_image function to the window resizing event
            home_window.bind("<Configure>", resize_image)

            # Call resize_image initially to set the image size
            resize_image()

        except Exception as e:  # Use a generic Exception to catch all errors
            messagebox.showerror("Error", f"Failed to load image: {e}")
        

        # Create a frame for buttons
        buttons_frame = tk.Frame(home_window)
        buttons_frame.pack(pady=(250, 8))  # Adjust the top padding
        buttons_frame.configure(bg="dark blue")
        # Create and configure buttons for different pages
        courses_button = tk.Button(buttons_frame, text="Courses",  font=("Garamond", 20, "bold"),command=open_courses_page, width=15, height=2, cursor="hand2")
        courses_button.grid(row=9, column=1, padx=40)
        courses_button.configure(bg="dark green")

        trainers_button = tk.Button(buttons_frame, text="Trainers",   font=("Garamond", 20, "bold"),command=open_trainers_page, width=15, height=2, cursor="hand2")
        trainers_button.grid(row=10, column=1, padx=40)
        trainers_button.configure(bg="dark green")

        billing_button = tk.Button(buttons_frame, text="Billing",  font=("Garamond", 20, "bold"),command=open_billing_page, width=15, height=2, cursor="hand2")
        billing_button.grid(row=11, column=1, padx=40)
        billing_button.configure(bg="dark green")
        MyCourses_button = tk.Button(buttons_frame, text="View Courses",  font=("Garamond", 20, "bold"),command=lambda:display_my_courses(home_window), width=15, height=2, cursor="hand2")
        MyCourses_button .grid(row=12, column=1, padx=40)
        MyCourses_button.configure(bg="dark green")
        # Add logout button
        logout_button = tk.Button(home_window, text="Logout", font=("Garamond", 15), command=logout)
        logout_button.pack( padx=20, pady=10)

        home_window.protocol("WM_DELETE_WINDOW", on_close)    
        root.iconify()

        home_window.mainloop()
    else:
        messagebox.showerror("Error", "User not logged in.")

def on_home_page_close():
    global root # Ensure root is accessible globally

    # Deiconify the root window when the home page is closed
    root.deiconify()
def prompt_admin_password():
    password_entry = simpledialog.askstring("Admin Login", "Enter Admin Password:", show='*')
    return password_entry

def is_admin_password_correct():
    hardcoded_admin_password = "admin123"
    entered_password = prompt_admin_password()
    return entered_password == hardcoded_admin_password

def on_admin_close():
    admin_window.destroy()
    root.deiconify()
# Global variable for the database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vaishu02",
    database="training_management_db",
    port=3306
)

def open_admin_page():
    global admin_window, course_id_entry, course_name_entry, course_price_entry, course_duration_entry, add_course_window

    def on_admin_close():
        admin_window.destroy()

    def logout():
        global current_user_id
        current_user_id = None
        admin_window.destroy()
        root.deiconify()

    if is_admin_password_correct():
        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Page")
        admin_window.geometry(full_screen_size)

        def add_logout_button():
            logout_button = tk.Button(admin_window, text="Logout", command=logout)
            logout_button.pack(side="top", padx=10)

        add_logout_button()

        try:
            # Set background image
            path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\admin.png"
            bg_image = Image.open(path)
            print("Image loaded successfully")
            
            # Create a label for the background image
            bg_label = tk.Label(admin_window)
            bg_label.place(relwidth=1, relheight=1)

            # Function to resize the image
            def resize_image(event=None):
                # Retrieve the updated window size
                window_width = admin_window.winfo_width()
                window_height = admin_window.winfo_height()

                # Resize the image to fit the window size
                resized_image = bg_image.resize((window_width, window_height))
                img = ImageTk.PhotoImage(resized_image)
                bg_label.config(image=img)
                bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
            
            # Bind the resize_image function to the window resizing event
            admin_window.bind("<Configure>", resize_image)

            # Call resize_image initially to set the image size
            resize_image()

        except Exception as e:  # Use a generic Exception to catch all errors
            messagebox.showerror("Error", f"Failed to load image: {e}")
        

        admin_notebook = ttk.Notebook(admin_window, width=780,height=520)


        def view_courses_tab():
            def fetch_courses():
                try:
                    cursor = db_connection.cursor()
                    cursor.execute("SELECT cd.CrsId, cd.CrsName, cd.CPrice, cd.Duration, t.TName FROM coursedetails cd INNER JOIN Trainers t ON cd.CrsId = t.CrsId")
                    courses = cursor.fetchall()
                    cursor.close()
                    return courses

                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
                    return []

            def save_course():
                crs_id = course_id_entry.get()
                crs_name = course_name_entry.get()
                crs_price = course_price_entry.get()
                crs_duration = course_duration_entry.get()

                if not crs_id or not crs_name or not crs_price or not crs_duration:
                    messagebox.showerror("Error", "Please fill in all fields")
                    return

                try:
                    cursor = db_connection.cursor()
                    insert_query = "INSERT INTO coursedetails (CrsId, CrsName, CPrice, Duration) VALUES (%s, %s, %s, %s)"
                    course_data = (crs_id, crs_name, crs_price, crs_duration)
                    cursor.execute(insert_query, course_data)
                    db_connection.commit()
                    cursor.close()

                    add_course_window.destroy()
                    refresh_courses_treeview()

                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error inserting course details: {e}")


                
            def add_course():
                global course_id_entry, course_name_entry, course_price_entry, course_duration_entry, add_course_window

                   
                add_course_window = tk.Toplevel(admin_window)
                add_course_window.title("Add Course")
                add_course_window.geometry(full_screen_size)
                add_course_window.resizable(True, True)

                try:
                    # Set background image
                    path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\bg.png"
                    bg_image = Image.open(path)
                    print("Image loaded successfully")
                    
                    # Create a label for the background image
                    bg_label = tk.Label(add_course_window)
                    bg_label.place(relwidth=1, relheight=1)

                    # Function to resize the image
                    def resize_image(event=None):
                        # Retrieve the updated window size
                        window_width = add_course_window.winfo_width()
                        window_height = add_course_window.winfo_height()

                        # Resize the image to fit the window size
                        resized_image = bg_image.resize((window_width, window_height))
                        img = ImageTk.PhotoImage(resized_image)
                        bg_label.config(image=img)
                        bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
                    
                    # Bind the resize_image function to the window resizing event
                    add_course_window.bind("<Configure>", resize_image)

                    # Call resize_image initially to set the image size
                    resize_image()

                except Exception as e:  # Use a generic Exception to catch all errors
                    messagebox.showerror("Error", f"Failed to load image: {e}")
             
                course_id_label = tk.Label(add_course_window, text="Course ID:")
                course_id_label.pack(pady=10)
                course_id_entry = tk.Entry(add_course_window)
                course_id_entry.pack(pady=5)

                course_name_label = tk.Label(add_course_window, text="Course Name:")
                course_name_label.pack(pady=10)
                course_name_entry = tk.Entry(add_course_window)
                course_name_entry.pack(pady=5)

                course_price_label = tk.Label(add_course_window, text="Price:")
                course_price_label.pack(pady=10)
                course_price_entry = tk.Entry(add_course_window)
                course_price_entry.pack(pady=5)

                course_duration_label = tk.Label(add_course_window, text="Duration:")
                course_duration_label.pack(pady=10)
                course_duration_entry = tk.Entry(add_course_window)
                course_duration_entry.pack(pady=5)

                
                # Create a "Save" button
                save_button = tk.Button(add_course_window, text="Save", command=save_course)
                save_button.pack(pady=10)

            def refresh_courses_treeview():
                courses_treeview.delete(*courses_treeview.get_children())
                courses_data = fetch_courses()

                for course in courses_data:
                    courses_treeview.insert("", "end", values=course)

            def remove_course():
                # Function to open a new window for removing a course
                remove_course_window = tk.Toplevel(admin_window)
                remove_course_window.title("Remove Course")
                remove_course_window.geometry("300x150")  # Adjust the size according to your needs
                remove_course_window.resizable(False, False)

                # Label and entry widget for course ID
                course_id_label = tk.Label(remove_course_window, text="Course ID:")
                course_id_label.pack(pady=10)
                course_id_entry = tk.Entry(remove_course_window)
                course_id_entry.pack(pady=5)

                # Function to remove the course based on the entered ID
                def remove_course_from_db():
                    course_id = course_id_entry.get()

                    # Validate that the course ID is provided
                    if not course_id:
                        messagebox.showerror("Error", "Please enter the Course ID")
                        return

                    try:
                        cursor = db_connection.cursor()
                        delete_query = "DELETE FROM coursedetails WHERE CrsId = %s"
                        cursor.execute(delete_query, (course_id,))
                        db_connection.commit()
                        cursor.close()

                        remove_course_window.destroy()
                        refresh_courses_treeview()

                    except mysql.connector.Error as e:
                        messagebox.showerror("Database Error", f"Error removing course: {e}")

                # Create a "Remove" button
                remove_button = tk.Button(remove_course_window, text="Remove", command=remove_course_from_db)
                remove_button.pack(pady=20)


            view_courses_tab_frame = ttk.Frame(admin_notebook)
            admin_notebook.add(view_courses_tab_frame, text="View Courses")

            courses_treeview = ttk.Treeview(view_courses_tab_frame, columns=("CrsId", "CrsName", "CPrice", "Duration"), show="headings")
            courses_treeview.heading("CrsId", text="Course ID")
            courses_treeview.heading("CrsName", text="Course Name")
            courses_treeview.heading("CPrice", text="Price")
            courses_treeview.heading("Duration", text="Duration")

            courses_data = fetch_courses()

            for course in courses_data:
                courses_treeview.insert("", "end", values=course)


            courses_treeview.pack(fill="x", expand=True, padx=10, pady=10)
            courses_treeview.column("CrsId", width=80)
            courses_treeview.column("CrsName", width=150)
            courses_treeview.column("CPrice", width=80)
            courses_treeview.column("Duration", width=80)

            add_button = tk.Button(view_courses_tab_frame, text="Add Course", command=add_course)
            add_button.pack(side="left", padx=10)

            remove_button = tk.Button(view_courses_tab_frame, text="Remove Course", command=remove_course)
            remove_button.pack(side="left", padx=10)

        def trainers_tab():
            def fetch_trainers():
                try:
                    cursor = db_connection.cursor()
                    cursor.execute("SELECT Tid, TName, TGender, Qualification, Trainers.CrsId, T_exp, Rating, CrsName FROM trainers INNER JOIN coursedetails ON trainers.CrsId = coursedetails.CrsId")
                    trainers = cursor.fetchall()
                    cursor.close()
                    return trainers
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
                    return []

            def add_trainer():
                # Function to open a new window for adding a trainer
                add_trainer_window = tk.Toplevel(admin_window)
                add_trainer_window.title("Add Trainer")
                add_trainer_window.geometry(full_screen_size)  # Adjust the size according to your needs
                add_trainer_window.resizable(False, False)

                try:
                    # Set background image
                    path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\bg.png"
                    bg_image = Image.open(path)
                    print("Image loaded successfully")
                    
                    # Create a label for the background image
                    bg_label = tk.Label(add_trainer_window)
                    bg_label.place(relwidth=1, relheight=1)

                    # Function to resize the image
                    def resize_image(event=None):
                        # Retrieve the updated window size
                        window_width = add_trainer_window.winfo_width()
                        window_height = add_trainer_window.winfo_height()

                        # Resize the image to fit the window size
                        resized_image = bg_image.resize((window_width, window_height))
                        img = ImageTk.PhotoImage(resized_image)
                        bg_label.config(image=img)
                        bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
                    
                    # Bind the resize_image function to the window resizing event
                    add_trainer_window.bind("<Configure>", resize_image)

                    # Call resize_image initially to set the image size
                    resize_image()

                except Exception as e:  # Use a generic Exception to catch all errors
                    messagebox.showerror("Error", f"Failed to load image: {e}")
                

                # Labels and entry widgets for trainer details
                trainer_id_label = tk.Label(add_trainer_window, text="Trainer ID:")
                trainer_id_label.pack(pady=10)
                trainer_id_entry = tk.Entry(add_trainer_window)
                trainer_id_entry.pack(pady=5)

                trainer_name_label = tk.Label(add_trainer_window, text="Trainer Name:")
                trainer_name_label.pack(pady=10)
                trainer_name_entry = tk.Entry(add_trainer_window)
                trainer_name_entry.pack(pady=5)

                tk.Label(add_trainer_window, text="Gender:").pack(pady=10)
                trainer_gender_var = tk.StringVar(value="Male")  # Default to "Male"
                tk.Radiobutton(add_trainer_window, text="Male", variable=trainer_gender_var, value="M").pack()
                tk.Radiobutton(add_trainer_window, text="Female", variable=trainer_gender_var, value="F").pack()
                tk.Radiobutton(add_trainer_window, text="Others", variable=trainer_gender_var, value="Oth").pack()

                qualification_label = tk.Label(add_trainer_window, text="Qualification:")
                qualification_label.pack(pady=10)
                qualification_entry = tk.Entry(add_trainer_window)
                qualification_entry.pack(pady=5)

                crs_id_label = tk.Label(add_trainer_window, text="Course ID:")
                crs_id_label.pack(pady=10)
                crs_id_entry = tk.Entry(add_trainer_window)
                crs_id_entry.pack(pady=5)

                t_exp_label = tk.Label(add_trainer_window, text="Experience:")
                t_exp_label.pack(pady=10)
                t_exp_entry = tk.Entry(add_trainer_window)
                t_exp_entry.pack(pady=5)

                rating_label = tk.Label(add_trainer_window, text="Rating:")
                rating_label.pack(pady=10)
                rating_entry = tk.Entry(add_trainer_window)
                rating_entry.pack(pady=5)
            
                # Function to save the entered trainer details
                def save_trainer():
                    tr_id = trainer_id_entry.get()
                    tr_name = trainer_name_entry.get()
                    tr_gender = trainer_gender_var.get()
                    qualification = qualification_entry.get()
                    crs_id = crs_id_entry.get()
                    t_exp = t_exp_entry.get()
                    rating = rating_entry.get()

                    if not tr_id or not tr_name or not tr_gender or not qualification or not crs_id or not t_exp or not rating:
                        messagebox.showerror("Error", "Please fill in all fields")
                        return

                    try:
                        cursor = db_connection.cursor()
                        insert_query = "INSERT INTO trainers (Tid, TName, TGender, Qualification, CrsId, T_exp, Rating) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        trainer_data = (tr_id, tr_name, tr_gender, qualification, crs_id, t_exp, rating)
                        cursor.execute(insert_query, trainer_data)
                        db_connection.commit()
                        cursor.close()

                        add_trainer_window.destroy()
                        refresh_trainers_treeview()

                    except mysql.connector.Error as e:
                        messagebox.showerror("Database Error", f"Error inserting trainer details: {e}")

                # Create a "Save" button
                save_button = tk.Button(add_trainer_window, text="Save", command=save_trainer)
                save_button.pack(pady=20)

            def refresh_trainers_treeview():
                trainers_treeview.delete(*trainers_treeview.get_children())

                trainers_data = fetch_trainers()

                for trainer in trainers_data:
                    trainers_treeview.insert("", "end", values=trainer)

            def remove_trainer():
                # Function to open a new window for removing a trainer
                remove_trainer_window = tk.Toplevel(admin_window)
                remove_trainer_window.title("Remove Trainer")
                remove_trainer_window.geometry("300x150")  # Adjust the size according to your needs
                remove_trainer_window.resizable(False, False)

                # Label and entry widget for trainer ID
                trainer_id_label = tk.Label(remove_trainer_window, text="Trainer ID:")
                trainer_id_label.pack(pady=10)
                trainer_id_entry = tk.Entry(remove_trainer_window)
                trainer_id_entry.pack(pady=5)

                # Function to remove the trainer based on the entered ID
                def remove_trainer_from_db():
                    trainer_id = trainer_id_entry.get()

                    # Validate that the trainer ID is provided
                    if not trainer_id:
                        messagebox.showerror("Error", "Please enter the Trainer ID")
                        return

                    try:
                        cursor = db_connection.cursor()
                        delete_query = "DELETE FROM trainers WHERE Tid = %s"
                        cursor.execute(delete_query, (trainer_id,))
                        db_connection.commit()
                        cursor.close()

                        remove_trainer_window.destroy()
                        refresh_trainers_treeview()

                    except mysql.connector.Error as e:
                        messagebox.showerror("Database Error", f"Error removing trainer: {e}")

                # Create a "Remove" button
                remove_button = tk.Button(remove_trainer_window, text="Remove", command=remove_trainer_from_db)
                remove_button.pack(pady=20)

            # Create a Treeview for displaying trainers
            trainers_tab_frame = ttk.Frame(admin_notebook)
            admin_notebook.add(trainers_tab_frame, text="Trainers")

            trainers_treeview = ttk.Treeview(trainers_tab_frame, columns=("Tid", "TName", "TGender", "Qualification", "CrsId", "T_exp", "Rating", "CrsName"), show="headings")
            trainers_treeview.heading("Tid", text="Trainer ID")
            trainers_treeview.heading("TName", text="Trainer Name")
            trainers_treeview.heading("TGender", text="Gender")
            trainers_treeview.heading("Qualification", text="Qualification")
            trainers_treeview.heading("CrsId", text="Course ID")
            trainers_treeview.heading("T_exp", text="Experience")
            trainers_treeview.heading("Rating", text="Rating")
            trainers_treeview.heading("CrsName", text="Course Name")

            trainers_data = fetch_trainers()

            for trainer in trainers_data:
                trainers_treeview.insert("", "end", values=trainer)

            style = ttk.Style()
            style.configure("Treeview", background="lightgrey")

            trainers_treeview.pack(fill="x", expand=True, padx=10, pady=10)
            trainers_treeview.column("Tid", width=80)
            trainers_treeview.column("TName", width=150)
            trainers_treeview.column("TGender", width=80)
            trainers_treeview.column("Qualification", width=100)
            trainers_treeview.column("CrsId", width=80)
            trainers_treeview.column("T_exp", width=80)
            trainers_treeview.column("Rating", width=80)
            trainers_treeview.column("CrsName", width=150)

            add_button = tk.Button(trainers_tab_frame, text="Add Trainer", command=add_trainer)
            add_button.pack(side="left", padx=10)

            remove_button = tk.Button(trainers_tab_frame, text="Remove Trainer", command=remove_trainer)
            remove_button.pack(side="left", padx=10)


        def billing_tab():
            # Function to fetch billing details from the database
            def fetch_billing_details():
                try:
                    cursor = db_connection.cursor()
                    cursor.execute("SELECT Bill_id, Sid, Tid, BCrsId, CPrice, Discount, TotalPrice FROM billing ORDER BY Sid")
                    billing_details = cursor.fetchall()
                    cursor.close()
                    return billing_details
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
                    return []
                
            # Function to fetch course name from the coursedetails table based on the course ID
            def fetch_course_name(course_id):
                try:
                    cursor = db_connection.cursor()
                    cursor.execute("SELECT CrsName FROM coursedetails WHERE CrsId = %s", (course_id,))
                    course_name = cursor.fetchone()[0]
                    cursor.close()
                    return course_name
                except mysql.connector.Error as e:
                    messagebox.showerror("Database Error", f"Error fetching course name: {e}")
                    return None
                
            # Function to sort billing details by SID
            def sort_by_sid():
                billing_treeview.delete(*billing_treeview.get_children())  # Clear existing data
                sorted_billing_data = sorted(fetch_billing_details(), key=lambda x: x[1])  # Sort by SID
                for billing_entry in sorted_billing_data:
                    course_name = fetch_course_name(billing_entry[3])
                    billing_treeview.insert("", "end", values=(billing_entry[0], billing_entry[1], billing_entry[2], billing_entry[3], course_name, billing_entry[4], billing_entry[5], billing_entry[6]))
            # Create a Treeview for displaying billing details
            billing_tab_frame = ttk.Frame(admin_notebook)
            admin_notebook.add(billing_tab_frame, text="Billing Details")

            billing_treeview = ttk.Treeview(billing_tab_frame, columns=("Bill_id", "Sid", "Tid", "BCrsId", "CrsName", "CPrice", "Discount", "TotalPrice"), show="headings")
            billing_treeview.heading("Bill_id", text="Bill ID")
            billing_treeview.heading("Sid", text="Student ID", command=lambda: sort_by_sid(billing_treeview, "Sid"))
            billing_treeview.heading("Tid", text="Trainer ID")
            billing_treeview.heading("BCrsId", text="Course ID")
            billing_treeview.heading("CrsName", text="Course Name")
            billing_treeview.heading("CPrice", text="Course Price")
            billing_treeview.heading("Discount", text="Discount")
            billing_treeview.heading("TotalPrice", text="Total Price")

            billing_data = fetch_billing_details()

            for billing_entry in billing_data:
                # Fetch course name based on course ID
                course_name = fetch_course_name(billing_entry[3])
                billing_treeview.insert("", "end", values=(billing_entry[0], billing_entry[1], billing_entry[2], billing_entry[3], course_name, billing_entry[4], billing_entry[5], billing_entry[6]))

            style = ttk.Style()
            style.configure("Treeview", background="lightgrey")

            billing_treeview.pack(fill="both", expand=True, padx=10, pady=10)
            billing_treeview.column("Bill_id", width=80)
            billing_treeview.column("Sid", width=80)
            billing_treeview.column("Tid", width=80)
            billing_treeview.column("BCrsId", width=80)
            billing_treeview.column("CrsName", width=150)  # Adjust the width as needed
            billing_treeview.column("CPrice", width=80)
            billing_treeview.column("Discount", width=80)
            billing_treeview.column("TotalPrice", width=80)

        view_courses_tab()
        trainers_tab()
        billing_tab()

        admin_notebook.pack(expand=1, fill="x")

        admin_window.protocol("WM_DELETE_WINDOW", on_admin_close)
    else:
        messagebox.showerror("Authentication Error", "Incorrect admin password. Access denied.")

def display_my_courses(window):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    # Retrieve billing information for the current user
    query = """
        SELECT b.Bill_id, c.CrsName, c.Cprice, t.Tname
        FROM billing b
        JOIN coursedetails c ON b.BCrsId = c.Crsid
        JOIN trainers t ON b.Tid = t.Tid
        WHERE b.Sid = %s
    """
    cursor.execute(query, (current_user_id,))
    my_courses = cursor.fetchall()

    cursor.close()
    connection.close()

    MyCourses_window = tk.Toplevel()
    MyCourses_window.title("My Courses")
    MyCourses_window.geometry(full_screen_size)
    MyCourses_window.resizable(True, True)

    # Load and display the background image
    try:
        # Set background image
        path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\bg.png"
        bg_image = Image.open(path)
        print("Image loaded successfully")
        
        # Create a label for the background image
        bg_label = tk.Label(MyCourses_window)
        bg_label.place(relwidth=1, relheight=1)

        # Function to resize the image
        def resize_image(event=None):
            # Retrieve the updated window size
            window_width = MyCourses_window.winfo_width()
            window_height = MyCourses_window.winfo_height()

            # Resize the image to fit the window size
            resized_image = bg_image.resize((window_width, window_height))
            img = ImageTk.PhotoImage(resized_image)
            bg_label.config(image=img)
            bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
        
        # Bind the resize_image function to the frame resizing event
        MyCourses_window.bind("<Configure>", resize_image)

        # Call resize_image initially to set the image size
        resize_image()

    except Exception as e:  # Use a generic Exception to catch all errors
        messagebox.showerror("Error", f"Failed to load image: {e}")

    my_courses_frame= tk.Frame(MyCourses_window)
    my_courses_frame.pack(pady=20)

    # Create a frame for My Courses section
    

    # Display My Courses heading
    tk.Label(my_courses_frame, text="My Courses", font=("Helvetica", 16, "bold")).pack(pady=10)

    if not my_courses:
        tk.Label(my_courses_frame, text="You haven't chosen any courses yet.").pack(pady=5)
    else:
        # Create a Treeview to display the courses and trainer details
        tree_frame = ttk.Frame(my_courses_frame)
        tree_frame.pack(side=tk.LEFT, padx=20, pady=20, fill="both", expand=True)

        tree = ttk.Treeview(tree_frame)
        tree["columns"] = ("Bill ID", "Course Name", "Course Price", "Trainer Name")

        tree.heading("#0", text="", anchor="w")
        tree.heading("Bill ID", text="Bill ID", anchor="w")
        tree.heading("Course Name", text="Course Name", anchor="w")
        tree.heading("Course Price", text="Course Price", anchor="w")
        tree.heading("Trainer Name", text="Trainer Name", anchor="w")

        for course in my_courses:
            tree.insert("", tk.END, values=course)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
def open_courses_page():
    def on_courses_page_close():
        courses_window.destroy()

    courses_window = tk.Toplevel(root)
    courses_window.title("Courses Page")
    courses_window.geometry(full_screen_size)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    # Use a JOIN query to fetch course details along with the trainer's name
    query = """
        SELECT c.Crsid, c.CrsName, c.Cprice, c.Duration, t.Tname
        FROM coursedetails c
        LEFT JOIN trainers t ON c.Crsid = t.CrsId
    """
    cursor.execute(query)
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    main_frame = ttk.Frame(courses_window)
    main_frame.pack(fill="both", expand=True)

    # Load and display the background image
    try:
        # Set background image
        path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\5.png"
        bg_image = Image.open(path)
        print("Image loaded successfully")
        
        # Create a label for the background image
        bg_label = tk.Label(main_frame)
        bg_label.place(relwidth=1, relheight=1)

        # Function to resize the image
        def resize_image(event=None):
            # Retrieve the updated window size
            window_width = main_frame.winfo_width()
            window_height = main_frame.winfo_height()

            # Resize the image to fit the window size
            resized_image = bg_image.resize((window_width, window_height))
            img = ImageTk.PhotoImage(resized_image)
            bg_label.config(image=img)
            bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
        
        # Bind the resize_image function to the frame resizing event
        main_frame.bind("<Configure>", resize_image)

        # Call resize_image initially to set the image size
        resize_image()

    except Exception as e:  # Use a generic Exception to catch all errors
        messagebox.showerror("Error", f"Failed to load image: {e}")

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

    tree = ttk.Treeview(tree_frame)
    tree["columns"] = ("Course ID", "Course Name", "Course Price", "Duration", "Trainer Name")

    tree.heading("Course ID", text="Course ID", anchor="w")
    tree.heading("Course Name", text="Course Name", anchor="w")
    tree.heading("Course Price", text="Course Price", anchor="w")
    tree.heading("Duration", text="Duration in Months", anchor="w")
    tree.heading("Trainer Name", text="Trainer Name", anchor="w")

    for course in courses:
        tree.insert("", tk.END, values=course)

    # Adjust the height of the treeview based on the number of items
    tree_height = min(len(courses), 10)  # Set a maximum height of 10 items
    tree.config(height=tree_height)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    if not courses:
        tk.Label(main_frame, text="No courses available.").pack(pady=5)

    courses_window.protocol("WM_DELETE_WINDOW", on_courses_page_close)

    courses_window.geometry(full_screen_size)

def open_trainers_page():
    def on_trainers_page_close():
        trainers_window.destroy()

    trainers_window = tk.Toplevel(root)
    trainers_window.title("Trainers Page")
    trainers_window.geometry(full_screen_size)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaishu02",
        database="training_management_db",
        port=3306
    )
    cursor = connection.cursor()

    query = "SELECT Tid, Tname, Qualification, CrsId, T_exp, Rating FROM trainers"
    cursor.execute(query)
    trainers = cursor.fetchall()

    cursor.close()
    connection.close()

    main_frame = ttk.Frame(trainers_window)
    main_frame.pack(fill="both", expand=True)

    # Load and display the background image
    try:
        # Set background image
        path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\6.png"
        bg_image = Image.open(path)
        print("Image loaded successfully")
        
        # Create a label for the background image
        bg_label = tk.Label(main_frame)
        bg_label.place(relwidth=1, relheight=1)

        # Function to resize the image
        def resize_image(event=None):
            # Retrieve the updated window size
            window_width = main_frame.winfo_width()
            window_height = main_frame.winfo_height()

            # Resize the image to fit the window size
            resized_image = bg_image.resize((window_width, window_height))
            img = ImageTk.PhotoImage(resized_image)
            bg_label.config(image=img)
            bg_label.image = img  # Keep a reference to the PhotoImage to prevent garbage collection
        
        # Bind the resize_image function to the frame resizing event
        main_frame.bind("<Configure>", resize_image)

        # Call resize_image initially to set the image size
        resize_image()

    except Exception as e:  # Use a generic Exception to catch all errors
        messagebox.showerror("Error", f"Failed to load image: {e}")

    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

    tree = ttk.Treeview(tree_frame)
    tree["columns"] = ("Trainer ID", "Trainer Name", "Qualification", "Course ID", "Experience", "Rating")

    tree.heading("Trainer ID", text="Trainer ID", anchor="w")
    tree.heading("Trainer Name", text="Trainer Name", anchor="w")
    tree.heading("Qualification", text="Qualification", anchor="w")
    tree.heading("Course ID", text="Course ID", anchor="w")
    tree.heading("Experience", text="Experience", anchor="w")
    tree.heading("Rating", text="Rating", anchor="w")

    for trainer in trainers:
        tree.insert("", tk.END, values=trainer)

# Adjust the height of the treeview based on the number of items
    tree_height = min(len(trainers), 10)  # Set a maximum height of 10 items
    tree.config(height=tree_height)
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    if not trainers:
        tk.Label(main_frame, text="No trainers available.").pack(pady=5)

    trainers_window.protocol("WM_DELETE_WINDOW", on_trainers_page_close)
def open_billing_page():
    if current_user_id is not None:
        BillingPage(current_user_id)
    else:
        messagebox.showerror("Error", "User not logged in.")

class BillingPage:
    def __init__(self, user_id):
        self.user_id = user_id
        self.selected_courses = []

        self.billing_window = tk.Toplevel()
        self.billing_window.title("Billing Page")
        self.billing_window.geometry(full_screen_size)
        self.course_tree = ttk.Treeview(self.billing_window, columns=("Course Name", "Course Price"), show="headings")

        # Load and display background image
        try:
            bg_path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\7.png"  # Update with your image path
            bg_image = Image.open(bg_path)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.billing_window, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {e}")

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vaishu02",
            database="training_management_db",
            port=3306
        )
        self.cursor = self.connection.cursor()

        self.create_ui()

    def create_ui(self):
        tk.Label(self.billing_window, text="Billing Page", font=("Helvetica", 30, "bold")).pack(pady=10)

        self.course_var = tk.StringVar()
        tk.Label(self.billing_window, text="Select Course:",font=("Garamond", 20, "bold")).pack(pady=5)
        self.course_dropdown = ttk.Combobox(self.billing_window, textvariable=self.course_var,font=("Garamond", 25, "bold"))
        self.course_dropdown.pack(pady=5)

        # Refresh the dropdown list with available courses
        self.refresh_courses_dropdown()

        tk.Button(self.billing_window, text="Add to Cart", command=self.add_to_cart,font=("Garamond", 20, "bold")).pack(pady=10)
        tk.Button(self.billing_window, text="View Cart", command=self.view_cart,font=("Garamond", 20, "bold")).pack(pady=10)
        tk.Button(self.billing_window, text="Generate Bill", command=self.calculate_and_display_bill,font=("Garamond", 20, "bold")).pack(pady=10)
        tk.Button(self.billing_window, text="Remove from Cart", command=self.remove_from_cart,font=("Garamond", 20, "bold")).pack(pady=10)

        self.billing_window.protocol("WM_DELETE_WINDOW", self.on_billing_page_close)

    def refresh_courses_dropdown(self):
        query = "SELECT CrsId, CrsName FROM coursedetails"
        self.cursor.execute(query)
        courses = self.cursor.fetchall()
        course_names = [course[1] for course in courses]
        self.course_dropdown["values"] = course_names

    def add_to_cart(self):
        selected_course_name = self.course_var.get()
        if not selected_course_name:
            messagebox.showwarning("Warning", "Please select a course.")
            return

        # Get the course details from the database
        query = "SELECT CrsId, CrsName, CPrice FROM coursedetails WHERE CrsName = %s"
        self.cursor.execute(query, (selected_course_name,))
        course = self.cursor.fetchone()

        if course:
            self.selected_courses.append(course)
            messagebox.showinfo("Added to Cart", f"{selected_course_name} added to your cart.")
            # Refresh the dropdown list with available courses after adding to cart
            self.refresh_courses_dropdown()
        else:
            messagebox.showwarning("Warning", "Selected course not found in the database.")
        
       

    def view_cart(self):
        # Create a new window to display the cart details
        cart_window = tk.Toplevel()
        cart_window.title("View Cart")
        cart_window.geometry("400x300")

        tk.Label(cart_window, text="Your Cart", font=("Helvetica", 16, "bold")).pack(pady=10)

        if not self.selected_courses:
            tk.Label(cart_window, text="Your cart is empty.").pack(pady=5)
        else:
            # Create a Treeview with columns
            tree = ttk.Treeview(cart_window, columns=("Course Name", "Course Price"), show="headings")

            # Set column headings
            tree.heading("Course Name", text="Course Name")
            tree.heading("Course Price", text="Course Price")

            for course in self.selected_courses:
                course_name = course[1]
                course_price = float(course[2])  # Convert to float
                tree.insert("", tk.END, values=(course_name, f"Rs.{course_price:.2f}"))

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(cart_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Pack the Treeview and scrollbar
            tree.pack(side=tk.LEFT, fill="both", expand=True)
            scrollbar.pack(side=tk.RIGHT, fill="y")

        tk.Button(cart_window, text="Close", command=cart_window.destroy).pack(pady=10)

    def calculate_and_display_bill(self):
        if not self.selected_courses:
            messagebox.showwarning("Warning", "Your cart is empty. Please add courses.")
            return

        original_price = sum(float(course[2]) for course in self.selected_courses)
        discount = 0

        if len(self.selected_courses) >= 2:
            discount = 0.05 * original_price

        total_price = original_price - discount

        self.display_bill(original_price, discount, total_price)
        self.store_billing_information(original_price, discount, total_price)

    def store_billing_information(self, original_price, discount, total_price):
        try:
            # Generate a random Bill_id using random function
            bill_id = random.randint(1000, 2000)

            # Get the Trainer ID (Tid) for the selected course
            selected_course_id = self.selected_courses[0][0]
            query = "SELECT Tid FROM trainers WHERE CrsId = %s"
            self.cursor.execute(query, (selected_course_id,))
            trainer_id = self.cursor.fetchone()[0]

            # Get the student's name based on the user_id
            query = "SELECT Name FROM student WHERE Sid = %s"
            self.cursor.execute(query, (self.user_id,))
            student_name = self.cursor.fetchone()[0]

            # Store billing information in the database
            query = "INSERT INTO billing (Bill_id, Sid, Tid, BCrsId, CPrice, Discount, TotalPrice) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (bill_id, self.user_id, trainer_id, self.selected_courses[0][0], original_price, discount, total_price)
            self.cursor.execute(query, values)

            self.connection.commit()
            messagebox.showinfo("Billing Information Stored", "Billing information has been successfully stored.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to store billing information: {err}")

    def display_bill(self, original_price, discount, total_price):
        # Create a new window for displaying the bill details
        bill_details_window = tk.Toplevel()
        bill_details_window.title("Bill Details")
        bill_details_window.geometry("400x300")

        tk.Label(bill_details_window, text="Bill Details", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Label(bill_details_window, text=f"Original Price: Rs.{original_price:.2f}").pack(pady=5)
        tk.Label(bill_details_window, text=f"Discount: Rs.{discount:.2f}").pack(pady=5)
        tk.Label(bill_details_window, text=f"Total Price: Rs.{total_price:.2f}").pack(pady=5)

        tk.Button(bill_details_window, text="Close", command=bill_details_window.destroy).pack(pady=10)

    def remove_from_cart(self):
        if not self.selected_courses:
            messagebox.showwarning("Warning", "Your cart is empty. Nothing to remove.")
            return

        selected_course_name = self.course_dropdown.get()

        if not selected_course_name:
            messagebox.showwarning("Warning", "Please select a course to remove.")
            return

        for course in self.selected_courses:
            if course[1] == selected_course_name:
                self.selected_courses.remove(course)
                messagebox.showinfo("Removed from Cart", f"{selected_course_name} removed from your cart.")
                return

        messagebox.showwarning("Warning", f"{selected_course_name} not found in your cart.")

        # Refresh the cart view
        self.view_cart()


    def on_billing_page_close(self):
        # Implement any cleanup or confirmation logic here
        self.selected_courses = []
        self.billing_window.destroy()

def on_successful_login(user_id):
    print(f"User with ID {user_id} logged in successfully.")

root = tk.Tk()
root.title("Login or Sign Up")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
full_screen_size = f"{screen_width}x{screen_height}"
root.geometry(full_screen_size)

path = r"C:\Users\Admin\Desktop\Vaishu\SKILL SPHERE\1.png"
original_image = Image.open(path)

# Resize the image to fit the initial window size
initial_width = root.winfo_width()
initial_height = root.winfo_height()
resized_image = original_image.resize((initial_width, initial_height))

# Create a PhotoImage object from the resized image
img = ImageTk.PhotoImage(resized_image)

# Create a label for the image
label = tk.Label(root, image=img)
#img.place(relwidth=1, relheight=1)
label.pack(fill="both", expand=True)

# Bind the resize event of the root window to resize the image
root.bind("<Configure>", resize_image)

# Create Login button
login_button = tk.Button(root, text="Login",command=open_login_window)
login_button.place(relx=0.84, rely=0.45, anchor=tk.CENTER)
login_button.config(width=19, height=2)

# Create Sign Up button
signup_button = tk.Button(root,text = "Signup" ,command=signup_clicked)
signup_button.place(relx=0.84, rely=0.64, anchor=tk.CENTER)
signup_button.config(width=19, height=2)

# Create Admin Login button
admin_login_button = tk.Button(root, text="Admin Login", command=open_admin_page)
admin_login_button.place(relx=0.84, rely=0.83, anchor=tk.CENTER)
admin_login_button.config(width=19, height=2)

root.mainloop()
