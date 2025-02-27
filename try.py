import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Added for Treeview
import re  # For email and phone number validation
import sqlite3

# Database connection function
def get_db_connection():
    return sqlite3.connect('data.db')

# Initialize database with users table
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(255),
        email VARCHAR(255) UNIQUE,
        address TEXT,
        phone_number VARCHAR(20),
        password VARCHAR(255),
        balance DECIMAL(10,2) DEFAULT 0
    )''')
    conn.commit()
    conn.close()

# Login page function with all logic and GUI
def login_page():
    def validate_login():
        email = entry_login_email.get()
        password = entry_login_password.get()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            login_win.withdraw()
            open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials", parent=login_win)

    global login_win, entry_login_email, entry_login_password
    login_win = tk.Tk()
    login_win.title("Admin Login Page")
    try:
        login_win.iconbitmap("logi.ico")
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    login_win.geometry("900x500")
    login_win.configure(bg="#f4f4f4")

    frame = tk.Frame(login_win, bg="white", padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Email:", font=("Arial", 12), bg="white").grid(row=0, column=0, pady=10, sticky="e")
    entry_login_email = tk.Entry(frame, font=("Arial", 12))
    entry_login_email.grid(row=0, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), bg="white").grid(row=1, column=0, pady=10, sticky="e")
    entry_login_password = tk.Entry(frame, font=("Arial", 12), show="*")
    entry_login_password.grid(row=1, column=1, pady=10)

    tk.Button(frame, text="Login", command=validate_login, bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5).grid(row=2, column=0, columnspan=2, pady=20)

    tk.Label(frame, text="Don't have an account?", font=("Arial", 10), bg="white").grid(row=3, column=0, pady=5, sticky="e")
    tk.Button(frame, text="Sign up here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2", 
              command=lambda: [login_win.withdraw(), register_page()]).grid(row=3, column=1, sticky="w")

    login_win.mainloop()

# Registration page function with all logic and GUI
def register_page():
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email)

    def validate_phone_number(phone_number):
        pattern = r"^\d{10}$"
        return re.match(pattern, phone_number)

    def register_user():
        first_name = entry_first_name.get().strip()
        last_name = entry_last_name.get().strip()
        ph_no = entry_ph_no.get().strip()
        address = entry_address.get().strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()
        confirm_password = entry_confirm_password.get().strip()

        if not all([first_name, last_name, ph_no, address, email, password, confirm_password]):
            messagebox.showerror("Error", "All fields are required!", parent=registration_win)
            return

        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format!", parent=registration_win)
            return

        if not validate_phone_number(ph_no):
            messagebox.showerror("Error", "Phone number must be 10 digits!", parent=registration_win)
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!", parent=registration_win)
            return

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (Name, email, address, phone_number, password) VALUES (?, ?, ?, ?, ?)",
                      (f"{first_name} {last_name}", email, address, ph_no, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!\nRedirecting to login page...", parent=registration_win)
            registration_win.withdraw()
            login_win.deiconify()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", f"{email} is already registered!", parent=registration_win)
        finally:
            conn.close()

    global registration_win, entry_first_name, entry_last_name, entry_ph_no, entry_address, entry_email, entry_password, entry_confirm_password
    registration_win = tk.Toplevel()
    registration_win.title("Admin Registration Page")
    try:
        registration_win.iconbitmap("logi.ico")
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    registration_win.geometry("850x500")
    registration_win.configure(bg="#f4f4f4")

    form_frame = tk.Frame(registration_win, bg="white", bd=5, padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Admin Registration", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    labels = ["First Name:", "Last Name:", "Phone Number:", "Address:", "Email:", "Password:", "Confirm Password:"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(row=i+1, column=0, sticky="w", pady=5)
        entry = tk.Entry(form_frame, font=("Arial", 12), show="*" if "Password" in label else "")
        entry.grid(row=i+1, column=1, pady=5, padx=10)
        entries.append(entry)

    entry_first_name, entry_last_name, entry_ph_no, entry_address, entry_email, entry_password, entry_confirm_password = entries

    tk.Button(form_frame, text="Register", command=register_user, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=len(labels)+1, column=0, columnspan=2, pady=20)

    tk.Label(form_frame, text="Already a member?", font=("Arial", 10), bg="white").grid(row=len(labels)+2, column=0, pady=5, sticky="e")
    tk.Button(form_frame, text="Login Here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2", 
              command=lambda: [registration_win.withdraw(), login_win.deiconify()]).grid(row=len(labels)+2, column=1, sticky="w")

# Function to open the dashboard
def open_dashboard():
    global dashboard  # Declare dashboard as global to make it accessible in add_entry
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

    # Income and Expenses buttons frame
    button_frame = tk.Frame(dashboard, bg="#f0f0f0")
    button_frame.pack(pady=10)

    global income_button, expenses_button, table, entry_amount, entry_description, entry_date
    global income_data, expenses_data
    income_data = []
    expenses_data = []

    income_button = tk.Button(button_frame, text="Income", command=lambda: [income_button.config(state='active'), expenses_button.config(state='normal'), show_income()], 
                            bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5)
    income_button.grid(row=0, column=0, padx=10)

    expenses_button = tk.Button(button_frame, text="Expenses", command=lambda: [expenses_button.config(state='active'), income_button.config(state='normal'), show_expenses()], 
                              bg="#FF5733", fg="white", font=("Arial", 12), padx=20, pady=5)
    expenses_button.grid(row=0, column=1, padx=10)

    # Table to display income/expenses details
    table = ttk.Treeview(dashboard, columns=("S.No", "Amount", "Description", "Date"), show="headings", height=10)
    table.heading("S.No", text="S.No")
    table.heading("Amount", text="Amount")
    table.heading("Description", text="Description")
    table.heading("Date", text="Date")
    table.column("S.No", width=50)
    table.column("Amount", width=100)
    table.column("Description", width=200)
    table.column("Date", width=100)
    table.pack(pady=20, padx=10, fill="both", expand=True)

    # Add new entry frame
    entry_frame = tk.Frame(dashboard, bg="#f0f0f0")
    entry_frame.pack(pady=10)

    tk.Label(entry_frame, text="Amount:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
    entry_amount = tk.Entry(entry_frame, font=("Arial", 12))
    entry_amount.grid(row=0, column=1, padx=5)

    tk.Label(entry_frame, text="Description:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=5)
    entry_description = tk.Entry(entry_frame, font=("Arial", 12))
    entry_description.grid(row=0, column=3, padx=5)

    tk.Label(entry_frame, text="Date:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=4, padx=5)
    entry_date = tk.Entry(entry_frame, font=("Arial", 12))
    entry_date.grid(row=0, column=5, padx=5)

    add_button = tk.Button(entry_frame, text="Add", command=lambda: add_entry(), 
                         bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5)
    add_button.grid(row=0, column=6, padx=10)

    # Logout button
    tk.Button(dashboard, text="Logout", command=lambda: logout(dashboard), bg="#FF5733", fg="white", 
             font=("Arial", 12), padx=10, pady=5).pack(pady=20)

    # Set initial state and show income by default
    income_button.config(state='active')
    expenses_button.config(state='normal')
    show_income()

def show_income():
    global table, income_data
    table.delete(*table.get_children())  # Fixed typo: changed tableergy to table
    for i, entry in enumerate(income_data):
        table.insert("", "end", values=(i+1, entry["amount"], entry["description"], entry["date"]))

def show_expenses():
    global table, expenses_data
    table.delete(*table.get_children())
    for i, entry in enumerate(expenses_data):
        table.insert("", "end", values=(i+1, entry["amount"], entry["description"], entry["date"]))

def add_entry():
    global entry_amount, entry_description, entry_date, income_data, expenses_data, income_button, dashboard
    amount = entry_amount.get().strip()
    description = entry_description.get().strip()
    date = entry_date.get().strip()

    if not amount or not description or not date:
        messagebox.showerror("Error", "All fields are required!", icon='error', parent=dashboard)
        return

    if income_button['state'] == 'active':
        income_data.append({"amount": amount, "description": description, "date": date})
        show_income()
    else:
        expenses_data.append({"amount": amount, "description": description, "date": date})
        show_expenses()

    entry_amount.delete(0, "end")
    entry_description.delete(0, "end")
    entry_date.delete(0, "end")

def logout(dashboard):
    dashboard.destroy()
    login_win.deiconify()

if __name__ == "__main__":
    init_db()
    login_page()