import tkinter as tk
from tkinter import messagebox
import re  # For email and phone number validation

# Dictionary to store registered admin users
admin_data = {}

# Function to open the registration page
def open_registration():
    login_win.withdraw()  # Hide the login window
    registration_page()

# Function to open the login page
def open_login():
    registration_win.withdraw()  # Hide the registration window
    login_win.deiconify()  # Show the login window

# Function to validate email format
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Function to validate phone number format
def validate_phone_number(phone_number):
    pattern = r"^\d{10}$"  # Assumes a 10-digit phone number
    return re.match(pattern, phone_number)

# Function to register a new admin
def register():
    first_name = entry_first_name.get().strip()
    last_name = entry_last_name.get().strip()
    ph_no = entry_ph_no.get().strip()
    address = entry_address.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    confirm_password = entry_confirm_password.get().strip()

    # Validate all fields are filled
    if not first_name or not last_name or not ph_no or not address or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!", icon='error', parent=registration_win)
        return

    # Validate email format
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format!", icon='error', parent=registration_win)
        return

    # Validate phone number format
    if not validate_phone_number(ph_no):
        messagebox.showerror("Error", "Phone number must be 10 digits!", icon='error', parent=registration_win)
        return

    # Validate password match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!", icon='error', parent=registration_win)
        return

    # Check if email is already registered
    if email in admin_data:
        messagebox.showerror("Error", f"{email} is already registered!", icon='error', parent=registration_win)
        return

    # Store credentials
    admin_data[email] = password
    messagebox.showinfo("Success", "Registration successful!\nRedirecting to login page...", icon='info', parent=registration_win)
    open_login()

# Function to create the registration page
def registration_page():
    global registration_win, entry_first_name, entry_last_name, entry_ph_no, entry_address, entry_email, entry_password, entry_confirm_password

    registration_win = tk.Toplevel()
    registration_win.title("Admin Registration Page")
    try:
        registration_win.iconbitmap("logi.ico")  # Set window icon
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    registration_win.geometry("850x500")
    registration_win.configure(bg="#f4f4f4")  # Set grey background

    # Registration Form
    form_frame = tk.Frame(registration_win, bg="white", bd=5, padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Admin Registration", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    # Form fields
    labels = ["First Name:", "Last Name:", "Phone Number:", "Address:", "Email:", "Password:", "Confirm Password:"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(row=i+1, column=0, sticky="w", pady=5)
        if label == "Password:" or label == "Confirm Password:":
            entry = tk.Entry(form_frame, font=("Arial", 12), show="*")  # Show asterisks for password fields
        else:
            entry = tk.Entry(form_frame, font=("Arial", 12))
        entry.grid(row=i+1, column=1, pady=5, padx=10)
        entries.append(entry)

    # Assign entries to global variables
    entry_first_name, entry_last_name, entry_ph_no, entry_address, entry_email, entry_password, entry_confirm_password = entries

    # Register button
    tk.Button(form_frame, text="Register", command=register, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=len(labels)+1, column=0, columnspan=2, pady=20)

    # Already a member? Option
    tk.Label(form_frame, text="Already a member?", font=("Arial", 10), bg="white").grid(row=len(labels)+2, column=0, pady=5, sticky="e")
    btn_login = tk.Button(form_frame, text="Login Here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2", command=open_login)
    btn_login.grid(row=len(labels)+2, column=1, sticky="w")

# Function to handle login
def login():
    email = entry_login_email.get()
    password = entry_login_password.get()

    if email in admin_data and admin_data[email] == password:
        login_win.withdraw()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials", icon='error', parent=login_win)

# Function to create the login page
def login_page():
    global login_win, entry_login_email, entry_login_password

    login_win = tk.Tk()
    login_win.title("Admin Login Page")
    try:
        login_win.iconbitmap("logi.ico")  # Set window icon
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    login_win.geometry("900x500")
    login_win.configure(bg="#f4f4f4")  # Set grey background

    # Add a centered login form
    frame = tk.Frame(login_win, bg="white", padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Login form fields
    tk.Label(frame, text="Email:", font=("Arial", 12), bg="white").grid(row=0, column=0, pady=10, sticky="e")
    entry_login_email = tk.Entry(frame, font=("Arial", 12))
    entry_login_email.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, pady=10, sticky="e")
    entry_login_password = tk.Entry(frame, font=("Arial", 12), show="*")
    entry_login_password.grid(row=1, column=1, pady=10)

    tk.Button(frame, text="Login", command=login, bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5).grid(row=2, column=0, columnspan=2, pady=20)

    # Sign up option
    tk.Label(frame, text="Don't have an account?", font=("Arial", 10), bg="white").grid(row=3, column=0, pady=5, sticky="e")
    btn_signup = tk.Button(frame, text="Sign up here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2", command=open_registration)
    btn_signup.grid(row=3, column=1, sticky="w")

# Function to open the dashboard
def open_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Admin Dashboard")
    try:
        dashboard.iconbitmap("logi.ico")  # Set window icon
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    dashboard.geometry("800x600")
    dashboard.configure(bg="#f0f0f0")

    # Back arrow button in top left corner
    back_button = tk.Button(dashboard, text="←", font=("Arial", 10), command=lambda: logout(dashboard),
                           bg="#FF5733", fg="white", padx=10, pady=5)
    back_button.place(x=10, y=10)

    tk.Label(dashboard, text="Welcome, Admin!", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    tk.Button(dashboard, text="Logout", command=lambda: logout(dashboard), bg="#FF5733", fg="white", 
             font=("Arial", 12), padx=10, pady=5).pack(pady=20)

# Function to handle logout
def logout(dashboard):
    dashboard.destroy()
    login_win.deiconify()

# Start the application
if __name__ == "__main__":
    login_page()
    tk.mainloop()