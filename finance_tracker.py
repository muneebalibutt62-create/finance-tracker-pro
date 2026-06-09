import json
import tkinter as tk
from tkinter import messagebox

# ================= DATA =================
Data = {
    "income": 0,
    "expense": 0,
    "transactions": []
}

# ================= LOAD =================
def load_data():
    global Data
    try:
        with open("finance_data.json", "r") as file:
            loaded = json.load(file)

        # ensure safe structure
        Data["income"] = loaded.get("income", 0)
        Data["expense"] = loaded.get("expense", 0)
        Data["transactions"] = loaded.get("transactions", [])

    except:
        Data = {
            "income": 0,
            "expense": 0,
            "transactions": []
        }

# ================= SAVE =================
def save_data():
    with open("finance_data.json", "w") as file:
        json.dump(Data, file)

# ================= LOGIC =================
def add_income(amount, description):
    Data["income"] += amount
    Data["transactions"].append(f"+ {amount} | {description}")
    save_data()

def add_expense(amount, description):
    Data["expense"] += amount
    Data["transactions"].append(f"- {amount} | {description}")
    save_data()

def get_balance():
    return Data["income"] - Data["expense"]

def delete_transaction():
    selected = transaction_list.curselection()

    if not selected:
        messagebox.showerror("Error", "Select a transaction first")
        return

    index = selected[0]

    Data["transactions"].pop(index)

    # reset totals
    Data["income"] = 0
    Data["expense"] = 0

    for t in Data["transactions"]:
        if t.startswith("+"):
            Data["income"] += int(t.split("|")[0][1:])
        else:
            Data["expense"] += int(t.split("|")[0][1:])

    save_data()
    update_ui()

# ================= UI UPDATE =================
def update_ui():
    balance_label.config(text=f"Balance: {get_balance()}")
    income_label.config(text=f"Income: {Data['income']}")
    expense_label.config(text=f"Expense: {Data['expense']}")

    transaction_list.delete(0, tk.END)
    for t in Data["transactions"]:
        transaction_list.insert(tk.END, t)

# ================= BUTTON ACTIONS =================
def income_btn():
    try:
        amount = int(amount_entry.get())
        desc = desc_entry.get().strip()

        if desc == "":
            messagebox.showerror("Missing Info", "Please enter a description (e.g. Salary, Gift, Freelance)")
            return

        add_income(amount, desc)
        update_ui()

    except:
        messagebox.showerror("Error", "Please enter a valid number")

def expense_btn():
    try:
        amount = int(amount_entry.get())
        desc = desc_entry.get().strip()

        if desc == "":
            messagebox.showerror("Missing Info", "Please enter a description (e.g. Food, Rent, Shopping)")
            return

        add_expense(amount, desc)
        update_ui()

    except:
        messagebox.showerror("Error", "Please enter a valid number")

    
# ================= APP =================
load_data()

root = tk.Tk()
root.title("💰 Finance Tracker Pro")
root.geometry("500x600")
root.config(bg="#1e1e1e")

# ================= TOP FRAME =================
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(pady=10)

balance_label = tk.Label(top_frame, text="Balance: 0", font=("Arial", 16), fg="white", bg="#1e1e1e")
balance_label.pack()

income_label = tk.Label(top_frame, text="Income: 0", fg="lightgreen", bg="#1e1e1e")
income_label.pack()

expense_label = tk.Label(top_frame, text="Expense: 0", fg="red", bg="#1e1e1e")
expense_label.pack()

# ================= INPUT FRAME =================
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10)

amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=0, column=0, padx=5)

desc_entry = tk.Entry(input_frame, width=25)
desc_entry.grid(row=0, column=1, padx=5)

# ================= BUTTON FRAME =================
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Income", bg="green", fg="white", command=income_btn).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add Expense", bg="red", fg="white", command=expense_btn).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Selected", bg="gray", fg="white", command=delete_transaction).grid(row=0, column=2, padx=5)

# ================= TRANSACTION LIST =================
list_frame = tk.Frame(root)
list_frame.pack(pady=10)

transaction_list = tk.Listbox(list_frame, width=60, height=15)
transaction_list.pack()

# ================= START =================
load_data()
update_ui()
root.mainloop()