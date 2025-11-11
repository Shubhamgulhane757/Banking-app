from tkinter import *
from tkinter.messagebox import *
import sqlite3
from datetime import datetime


def create_table(conn):
    cur = conn.cursor()

  
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accmaster (
            accno INTEGER PRIMARY KEY,
            name TEXT,
            balance INTEGER
        )
    """)

    
    


    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accno INTEGER,
            action TEXT,
            amount INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()

def log_transaction(accno, action, amount):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions (accno, action, amount, timestamp) VALUES (?, ?, ?, ?)",
                (accno, action, amount, timestamp))
    conn.commit()


def openAaccount_ds(conn, accno, name, balance):
    try:
        accno = int(accno.strip())
        balance = int(balance.strip())
        name = name.strip()
        if not name:
            showerror("Input Error", "Name cannot be empty")
            return
        query = "INSERT INTO accmaster VALUES (?, ?, ?)"
        cur = conn.cursor()
        cur.execute(query, [accno, name, balance])
        conn.commit()
        showinfo("Bank", "Account created successfully")
    except ValueError:
        showerror("Input Error", "Enter valid numeric values")
    except sqlite3.IntegrityError:
        showerror("Bank", "Account number already exists")

def checkbalance_ds(conn, accno):
    try:
        accno = int(accno.strip())
        query = "SELECT * FROM accmaster WHERE accno=?"
        cur = conn.cursor()
        cur.execute(query, [accno])
        row = cur.fetchone()
        if row is None:
            showerror("Bank", "Account Number not found")
        else:
            showinfo("Bank", f"Account No: {row[0]}\nName: {row[1]}\nBalance: ₹{row[2]}")
    except ValueError:
        showerror("Input Error", "Enter a valid account number")

def Deposit_ds(conn, accno, amount):
    try:
        accno = int(accno.strip())
        amount = int(amount.strip())
        query = "UPDATE accmaster SET balance = balance + ? WHERE accno = ?"
        cur = conn.cursor()
        cur.execute(query, [amount, accno])
        conn.commit()
        if cur.rowcount > 0:
            log_transaction(accno, "Deposit", amount)
            showinfo("Bank", "Amount deposited successfully")
        else:
            showerror("Bank", "Account not found")
    except ValueError:
        showerror("Input Error", "Enter valid numeric values")

def Withdraw_ds(conn, accno, amount):
    try:
        accno = int(accno.strip())
        amount = int(amount.strip())
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accmaster WHERE accno=?", [accno])
        row = cur.fetchone()
        if row is None:
            showerror("Bank", "Account not found")
            return
        if row[0] < amount:
            showerror("Bank", "Insufficient balance")
            return
        cur.execute("UPDATE accmaster SET balance = balance - ? WHERE accno = ?", [amount, accno])
        conn.commit()
        log_transaction(accno, "Withdraw", amount)
        showinfo("Bank", "Amount withdrawn successfully")
    except ValueError:
        showerror("Input Error", "Enter valid numeric values")

def close_ds(conn, accno):
    try:
        accno = int(accno.strip())
        cur = conn.cursor()
        cur.execute("SELECT balance FROM accmaster WHERE accno=?", [accno])
        row = cur.fetchone()
        if row:
            log_transaction(accno, "Account Closed", row[0])
        cur.execute("DELETE FROM accmaster WHERE accno=?", [accno])
        conn.commit()
        if cur.rowcount > 0:
            showinfo("Bank", "Account closed successfully")
        else:
            showerror("Bank", "Account not found")
    except ValueError:
        showerror("Input Error", "Enter a valid account number")

def clear():
    for item in win.winfo_children():
        item.destroy()

def exit_app():
    win.destroy()



def mainbank():
    clear()
    Label(win, text="Welcome to Bank", font="arial 20 bold", bg="pink").pack()
    Button(win, text="Open Account", width=20, command=openAccount, fg="green").pack(pady=3)
    Button(win, text="Check Balance", width=20, command=check_balance).pack(pady=3)
    Button(win, text="Deposit Amount", width=20, command=deposit_Amount).pack(pady=3)
    Button(win, text="Withdraw Amount", width=20, command=Withdraw_Amount).pack(pady=3)
    Button(win, text="Close Account", width=20, command=remove_account).pack(pady=3)
    Button(win, text="View History", width=20, command=view_history).pack(pady=3)
    Button(win, text="Exit", width=20, command=exit_app, fg="red").pack(pady=3)
    
def openAccount():
    clear()
    Label(win, text="Open Account", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Enter Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=5)
    Label(win, text="Enter Name", bg="pink").pack(pady=5)
    e2 = Entry(win)
    e2.pack(pady=5)
    Label(win, text="Enter Balance", bg="pink").pack(pady=5)
    e3 = Entry(win)
    e3.pack(pady=5)
    Button(win, text="Create Account", width=20,
           command=lambda: openAaccount_ds(conn, e1.get(), e2.get(), e3.get())).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

def check_balance():
    clear()
    Label(win, text="Check Balance", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Enter Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=3)
    Button(win, text="Check", width=20, command=lambda: checkbalance_ds(conn, e1.get())).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

def deposit_Amount():
    clear()
    Label(win, text="Deposit Amount", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Enter Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=3)
    Label(win, text="Enter Amount", bg="pink").pack(pady=3)
    e2 = Entry(win)
    e2.pack(pady=3)
    Button(win, text="Deposit", width=20, command=lambda: Deposit_ds(conn, e1.get(), e2.get())).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

def Withdraw_Amount():
    clear()
    Label(win, text="Withdraw Amount", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Enter Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=3)
    Label(win, text="Enter Amount", bg="pink").pack(pady=3)
    e2 = Entry(win)
    e2.pack(pady=3)
    Button(win, text="Withdraw", width=20, command=lambda: Withdraw_ds(conn, e1.get(), e2.get())).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

def remove_account():
    clear()
    Label(win, text="Close Account", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Enter Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=5)
    Button(win, text="Close Account", width=20, command=lambda: close_ds(conn, e1.get())).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

def view_history():
    clear()
    Label(win, text="Transaction History", font="arial 20 bold", bg="pink").pack()
    Label(win, text="Ent er Account Number", bg="pink").pack(pady=5)
    e1 = Entry(win)
    e1.pack(pady=3)

    def show_log():
        try:
            accno = int(e1.get().strip())
        except:
            showerror("Input Error", "Enter valid account number")
            return
        cur = conn.cursor()
        cur.execute("SELECT action, amount, timestamp FROM transactions WHERE accno=? ORDER BY id DESC", [accno])
        rows = cur.fetchall()
        if not rows:
            showinfo("Transactions", "No transactions found for this account.")
            return
        result = ""
        for action, amount, ts in rows:
            result += f"{ts} - {action}: ₹{amount}\n"
        showinfo("Transactions", result)

    Button(win, text="Show History", width=20, command=show_log).pack(pady=3)
    Button(win, text="Back", width=20, command=mainbank).pack(pady=3)

conn = sqlite3.connect("Bank_Data.db")
create_table(conn)
cur=conn.cursor()

conn.commit()
win = Tk()
win.configure(bg="pink")
win.geometry("300x500")
win.title("Bank App")
mainbank()

win.mainloop()


