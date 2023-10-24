import tkinter as tk
import sqlite3

# Function to save financial data
def save_transaction():
    description = description_entry.get()
    amount = amount_entry.get()

    if description and amount:
        conn = sqlite3.connect("financial.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS transactions (description TEXT, amount REAL)")
        cursor.execute("INSERT INTO transactions VALUES (?, ?)", (description, amount))
        conn.commit()
        conn.close()
        description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        update_summary()
    else:
        status_label.config(text="Description and amount are required.")

# Function to update the financial summary
def update_summary():
    conn = sqlite3.connect("financial.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions (description TEXT, amount REAL)")
    cursor.execute("SELECT SUM(amount) FROM transactions")
    total = cursor.fetchone()[0]
    conn.close()
    summary_label.config(text=f"Total Balance: ${total:.2f}")

# Create the main window
window = tk.Tk()
window.title("Personal Finance Manager")

# Create entry fields for description and amount
description_label = tk.Label(window, text="Description:")
description_label.pack()
description_entry = tk.Entry(window)
description_entry.pack()

amount_label = tk.Label(window, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(window)
amount_entry.pack()

# Create a button to save transactions
save_button = tk.Button(window, text="Save Transaction", command=save_transaction)
save_button.pack()

# Create labels for status and financial summary
status_label = tk.Label(window, text="", fg="red")
status_label.pack()

summary_label = tk.Label(window, text="Total Balance: $0.00")
summary_label.pack()

# Create an SQLite database to store transactions
conn = sqlite3.connect("financial.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transactions (description TEXT, amount REAL)")
conn.commit()
conn.close()

# Update the initial summary
update_summary()

# Run the application
window.mainloop()
