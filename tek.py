import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Database connection function
def get_db_connection():
    return sqlite3.connect('data.db')

# Initialize database with users, income, and expenses tables
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
    c.execute('''CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount DECIMAL(10,2),
        description TEXT,
        Date TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount DECIMAL(10,2),
        description TEXT,
        Date TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

# Login page function (unchanged)
def login_page():
    def validate_login():
        email = entry_login_email.get()
        password = entry_login_password.get()

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            user_id = user[0]
            login_win.withdraw()
            open_dashboard(user_id)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials", parent=login_win)

    global login_win, entry_login_email, entry_login_password
    login_win = tk.Tk()
    login_win.title("Login Page")
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

# Register page function (unchanged)
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
    registration_win.title(" Registration Page")
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

# Dashboard function (unchanged except for compare button)
def open_dashboard(user_id):
    global dashboard, income_button, expenses_button, table, entry_amount, entry_description, profile_button, compare_button, balance_label
    dashboard = tk.Toplevel()
    dashboard.title(" Dashboard")
    try:
        dashboard.iconbitmap("logi.ico")
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    dashboard.attributes('-fullscreen', True)
    dashboard.configure(bg="#f0f0f0")

    profile_button = tk.Button(dashboard, text="👤", font=("Arial", 14), command=lambda: open_profile_edit(user_id),
                              bg="#f0f0f0", fg="black", bd=0)
    profile_button.place(x=dashboard.winfo_screenwidth() - 40, y=10)

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT (SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id=?) - (SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id=?) AS balance", (user_id, user_id))
    balance = c.fetchone()[0]
    conn.close()
    
    balance_label = tk.Label(dashboard, text=f"Balance: RS{balance:.2f}", font=("Arial", 14), bg="#f0f0f0", fg="black")
    balance_label.place(x=dashboard.winfo_screenwidth() - 200, y=40)

    tk.Label(dashboard, text="Welcome, Admin!", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    button_frame = tk.Frame(dashboard, bg="#f0f0f0")
    button_frame.pack(pady=10)

    income_button = tk.Button(button_frame, text="Income", command=lambda: show_income(user_id), 
                              bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5)
    income_button.grid(row=0, column=0, padx=10)

    expenses_button = tk.Button(button_frame, text="Expenses", command=lambda: show_expenses(user_id), 
                                bg="#FF5733", fg="white", font=("Arial", 12), padx=20, pady=5)
    expenses_button.grid(row=0, column=1, padx=10)

    # Yo button click garda compare khulcha
    compare_button = tk.Button(button_frame, text="Compare", command=lambda: open_compare_dashboard(user_id), 
                              bg="#2196F3", fg="white", font=("Arial", 12), padx=20, pady=5)
    compare_button.grid(row=0, column=2, padx=50)

    # Yo table ho
    table = ttk.Treeview(dashboard, columns=("ID", "Amount", "Description", "Date"), show="headings", height=10)
    table.heading("ID", text="ID")
    table.heading("Amount", text="Amount")
    table.heading("Description", text="Description")
    table.heading("Date", text="Date")
    table.column("ID", width=50)
    table.column("Amount", width=100)
    table.column("Description", width=200)
    table.column("Date", width=150)
    table.pack(pady=20, padx=10, fill="both", expand=True)

    entry_frame = tk.Frame(dashboard, bg="#f0f0f0")
    entry_frame.pack(pady=10)

    tk.Label(entry_frame, text="Amount:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5)
    entry_amount = tk.Entry(entry_frame, font=("Arial", 12))
    entry_amount.grid(row=0, column=1, padx=5)

    tk.Label(entry_frame, text="Description:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=5)
    entry_description = tk.Entry(entry_frame, font=("Arial", 12))
    entry_description.grid(row=0, column=3, padx=5)

    add_button = tk.Button(entry_frame, text="Add", command=lambda: add_entry(user_id), 
                           bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5)
    add_button.grid(row=0, column=4, padx=10)

    tk.Button(dashboard, text="Logout", command=lambda: logout(dashboard), bg="#FF5733", fg="white", 
              font=("Arial", 12), padx=10, pady=5).pack(pady=20)

    show_income(user_id)

def show_income(user_id):
    global table, income_button, expenses_button
    income_button.config(relief="sunken")
    expenses_button.config(relief="raised")
    table.delete(*table.get_children())
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, amount, description, Date FROM income WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    for row in rows:
        table.insert("", "end", values=row)

def show_expenses(user_id):
    global table, income_button, expenses_button
    expenses_button.config(relief="sunken")
    income_button.config(relief="raised")
    table.delete(*table.get_children())
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, amount, description, Date FROM expenses WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    for row in rows:
        table.insert("", "end", values=row)

def add_entry(user_id):
    global entry_amount, entry_description, income_button, dashboard
    amount = entry_amount.get().strip()
    description = entry_description.get().strip()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not amount or not description:
        messagebox.showerror("Error", "Amount and Description are required!", parent=dashboard)
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!", parent=dashboard)
        return

    conn = get_db_connection()
    c = conn.cursor()

    if income_button.cget('relief') == "sunken":
        c.execute("INSERT INTO income (user_id, amount, description, Date) VALUES (?, ?, ?, ?)",
                  (user_id, amount, description, current_date))
        conn.commit()
        show_income(user_id)
        update_balance(user_id)
    else:
        c.execute("INSERT INTO expenses (user_id, amount, description, Date) VALUES (?, ?, ?, ?)",
                  (user_id, amount, description, current_date))
        conn.commit()
        show_expenses(user_id)
        update_balance(user_id)

    conn.close()
    entry_amount.delete(0, "end")
    entry_description.delete(0, "end")

def logout(dashboard):
    dashboard.destroy()
    login_win.deiconify()

def open_profile_edit(user_id):
    def save_changes():
        first_name, last_name = entry_name.get().strip().split(maxsplit=1) if entry_name.get().strip() else ("", "")
        ph_no = entry_phone.get().strip()
        address = entry_address.get("1.0", "end-1c").strip()
        email = entry_email.get().strip()
        password = entry_password.get().strip()

        if not all([first_name, ph_no, address, email, password]):
            messagebox.showerror("Error", "All fields are required!", parent=profile_win)
            return

        if not re.match(r"^\d{10}$", ph_no):
            messagebox.showerror("Error", "Phone number must be 10 digits!", parent=profile_win)
            return

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            messagebox.showerror("Error", "Invalid email format!", parent=profile_win)
            return

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("UPDATE users SET Name=?, email=?, address=?, phone_number=?, password=? WHERE id=?",
                      (f"{first_name} {last_name}", email, address, ph_no, password, user_id))
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!", parent=profile_win)
            profile_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already in use!", parent=profile_win)
        finally:
            conn.close()

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT Name, email, address, phone_number, password FROM users WHERE id=?", (user_id,))
    user_data = c.fetchone()
    conn.close()

    if not user_data:
        messagebox.showerror("Error", "User not found!", parent=dashboard)
        return

    name, email, address, phone, password = user_data

    global profile_win, entry_name, entry_phone, entry_address, entry_email, entry_password
    profile_win = tk.Toplevel(dashboard)
    profile_win.title("Edit Profile")
    try:
        profile_win.iconbitmap("logi.ico")
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    profile_win.geometry("500x600")
    profile_win.configure(bg="#f4f4f4")

    form_frame = tk.Frame(profile_win, bg="white", bd=5, padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_frame, text="Edit Profile", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(form_frame, text="Full Name:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
    entry_name = tk.Entry(form_frame, font=("Arial", 12))
    entry_name.grid(row=1, column=1, pady=5, padx=10)
    entry_name.insert(0, name)

    tk.Label(form_frame, text="Phone Number:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5)
    entry_phone = tk.Entry(form_frame, font=("Arial", 12))
    entry_phone.grid(row=2, column=1, pady=5, padx=10)
    entry_phone.insert(0, phone)

    tk.Label(form_frame, text="Address:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", pady=5)
    entry_address = tk.Text(form_frame, font=("Arial", 12), height=4, width=30)
    entry_address.grid(row=3, column=1, pady=5, padx=10)
    entry_address.insert("1.0", address)

    tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w", pady=5)
    entry_email = tk.Entry(form_frame, font=("Arial", 12))
    entry_email.grid(row=4, column=1, pady=5, padx=10)
    entry_email.insert(0, email)

    tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=5, column=0, sticky="w", pady=5)
    entry_password = tk.Entry(form_frame, font=("Arial", 12), show="*")
    entry_password.grid(row=5, column=1, pady=5, padx=10)
    entry_password.insert(0, password)

    tk.Button(form_frame, text="Save Changes", command=save_changes, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=20)

    profile_win.transient(dashboard)
    profile_win.grab_set()

def open_compare_dashboard(user_id):
    compare_dashboard = tk.Toplevel()
    compare_dashboard.title("Compare Dashboard")
    try:
        compare_dashboard.iconbitmap("logi.ico")
    except tk.TclError:
        print("Icon file not found or invalid. Skipping icon setting.")
    compare_dashboard.geometry("800x600")
    compare_dashboard.configure(bg="#f0f0f0")

    tk.Label(compare_dashboard, text="Income vs Expenses", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

    # Yo frame ma buttons rakheko cha
    button_frame = tk.Frame(compare_dashboard, bg="#f0f0f0")
    button_frame.pack(pady=10)

    # Canvas variable to hold the graph
    canvas = None

    def plot_graph(days):
        nonlocal canvas
        if canvas:
            canvas.get_tk_widget().destroy()  # Purano graph hataucha

        # Time range calculate garne
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

        # Database bata data lincha
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT Date, amount FROM income WHERE user_id=? AND Date BETWEEN ? AND ? ORDER BY Date", 
                  (user_id, start_date_str, end_date_str))
        income_data = c.fetchall()
        c.execute("SELECT Date, amount FROM expenses WHERE user_id=? AND Date BETWEEN ? AND ? ORDER BY Date", 
                  (user_id, start_date_str, end_date_str))
        expenses_data = c.fetchall()
        conn.close()

        # Cumulative data prepare garne
        dates = [start_date]  # Period ko suru dekhi
        income_totals = [0.0]  # Suruma zero
        expenses_totals = [0.0]  # Suruma zero
        balance_totals = [0.0]  # Suruma zero (income - expenses)

        # Income process garne
        for date_str, amount in income_data:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date > dates[-1]:
                dates.append(date)
                income_totals.append(income_totals[-1])
                expenses_totals.append(expenses_totals[-1])
                balance_totals.append(balance_totals[-1])
            income_totals[-1] += float(amount)
            balance_totals[-1] = income_totals[-1] - expenses_totals[-1]  # Balance update garne

        # Expenses process garne
        for date_str, amount in expenses_data:
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date > dates[-1]:
                dates.append(date)
                income_totals.append(income_totals[-1])
                expenses_totals.append(expenses_totals[-1])
                balance_totals.append(balance_totals[-1])
            expenses_totals[-1] += float(amount)
            balance_totals[-1] = income_totals[-1] - expenses_totals[-1]  # Balance update garne

        # Graph end date samma puryaucha
        if dates[-1] < end_date:
            dates.append(end_date)
            income_totals.append(income_totals[-1])
            expenses_totals.append(expenses_totals[-1])
            balance_totals.append(balance_totals[-1])

        # Graph banaucha
        fig = plt.Figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.plot(dates, income_totals, 'g-', label='Income', linewidth=2)  # Green line income ko lagi
        ax.plot(dates, expenses_totals, 'r-', label='Expenses', linewidth=2)  # Red line expenses ko lagi
        ax.plot(dates, balance_totals, 'k-', label='Balance', linewidth=2)  # Black line balance ko lagi
        ax.set_xlabel('Time')
        ax.set_ylabel('Amount (RS)')
        ax.set_title(f'Income vs Expenses vs Balance (Last {"Month" if days == 30 else "Week"})')
        ax.legend()
        ax.grid(True)
        fig.autofmt_xdate()  # Date labels rotate garne

        # Tkinter ma embed garne
        canvas = FigureCanvasTkAgg(fig, master=compare_dashboard)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20, fill="both", expand=True)

    # Yo button click garda last month ko graph dekhaucha
    tk.Button(button_frame, text="Last Month", command=lambda: plot_graph(30), 
              bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5).grid(row=0, column=0, padx=10)
    # Yo button click garda last week ko graph dekhaucha
    tk.Button(button_frame, text="Last Week", command=lambda: plot_graph(7), 
              bg="#FF5733", fg="white", font=("Arial", 12), padx=20, pady=5).grid(row=0, column=1, padx=10)

    tk.Button(compare_dashboard, text="Close", command=compare_dashboard.destroy, 
              bg="#FF5733", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=20)

    # Default ma last month dekhaucha
    plot_graph(30)

def update_balance(user_id):
    global balance_label
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT (SELECT COALESCE(SUM(amount), 0) FROM income WHERE user_id=?) - (SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id=?) AS balance", (user_id, user_id))
    balance = c.fetchone()[0]
    conn.close()
    balance_label.config(text=f"Balance: RS{balance:.2f}")

if __name__ == "__main__":
    init_db()
    login_page()