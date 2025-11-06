import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
def init_db():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Room (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_type TEXT,
        price REAL,
        status TEXT DEFAULT 'Available'
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cust_id INTEGER,
        room_id INTEGER,
        check_in TEXT,
        check_out TEXT,
        FOREIGN KEY (cust_id) REFERENCES Customer(cust_id),
        FOREIGN KEY (room_id) REFERENCES Room(room_id)
    )
    """)
    cur.execute("SELECT COUNT(*) FROM Room")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO Room (room_type, price) VALUES (?,?)",
                        [('Single',1500),('Double',2500),('Suite',5000)])
        conn.commit()
    conn.close()
def load_rooms():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM Room")
    rows = cur.fetchall()
    for item in room_table.get_children():
        room_table.delete(item)
    for r in rows:
        room_table.insert("", "end", values=r)
    conn.close()

def book_room():
    cust_name = cust_name_entry.get()
    phone = cust_phone_entry.get()
    email = cust_email_entry.get()
    room_id = room_id_entry.get()
    check_in = check_in_entry.get()
    check_out = check_out_entry.get()

    if not all([cust_name, phone, email, room_id, check_in, check_out]):
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("SELECT status FROM Room WHERE room_id=?", (room_id,))
    result = cur.fetchone()
    if not result or result[0] == "Booked":
        messagebox.showerror("Error", "Room is already booked or invalid!")
        conn.close()
        return
    cur.execute("INSERT INTO Customer (name, phone, email) VALUES (?,?,?)",
                (cust_name, phone, email))
    cust_id = cur.lastrowid
    cur.execute("INSERT INTO Booking (cust_id, room_id, check_in, check_out) VALUES (?,?,?,?)",
                (cust_id, room_id, check_in, check_out))
    cur.execute("UPDATE Room SET status='Booked' WHERE room_id=?", (room_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Room booked successfully!")
    load_rooms()

def cancel_booking():
    booking_id = booking_id_entry.get()
    if not booking_id:
        messagebox.showwarning("Warning", "Enter a Booking ID to cancel.")
        return

    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()
    cur.execute("SELECT room_id FROM Booking WHERE booking_id=?", (booking_id,))
    result = cur.fetchone()
    if not result:
        messagebox.showerror("Error", "Invalid booking ID!")
        conn.close()
        return

    room_id = result[0]
    cur.execute("DELETE FROM Booking WHERE booking_id=?", (booking_id,))
    cur.execute("UPDATE Room SET status='Available' WHERE room_id=?", (room_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Cancelled", "Booking cancelled successfully.")
    load_rooms()

root = tk.Tk()
root.title("🏨 Hotel Booking & Room Management System")
root.geometry("950x600")
root.configure(bg="#f8f9fa")

tk.Label(root, text="Hotel Booking System", font=("Helvetica", 18, "bold"), bg="#f8f9fa", fg="#007bff").pack(pady=10)

form_frame = tk.Frame(root, bg="#f8f9fa")
form_frame.pack(pady=5)

tk.Label(form_frame, text="Name:", bg="#f8f9fa").grid(row=0, column=0)
cust_name_entry = tk.Entry(form_frame)
cust_name_entry.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="Phone:", bg="#f8f9fa").grid(row=0, column=2)
cust_phone_entry = tk.Entry(form_frame)
cust_phone_entry.grid(row=0, column=3, padx=5)

tk.Label(form_frame, text="Email:", bg="#f8f9fa").grid(row=0, column=4)
cust_email_entry = tk.Entry(form_frame)
cust_email_entry.grid(row=0, column=5, padx=5)

tk.Label(form_frame, text="Room ID:", bg="#f8f9fa").grid(row=1, column=0)
room_id_entry = tk.Entry(form_frame)
room_id_entry.grid(row=1, column=1, padx=5)

tk.Label(form_frame, text="Check-in (YYYY-MM-DD):", bg="#f8f9fa").grid(row=1, column=2)
check_in_entry = tk.Entry(form_frame)
check_in_entry.grid(row=1, column=3, padx=5)

tk.Label(form_frame, text="Check-out (YYYY-MM-DD):", bg="#f8f9fa").grid(row=1, column=4)
check_out_entry = tk.Entry(form_frame)
check_out_entry.grid(row=1, column=5, padx=5)

tk.Button(root, text="Book Room", command=book_room, bg="#28a745", fg="white", width=15).pack(pady=5)

tk.Label(root, text="Cancel Booking ID:", bg="#f8f9fa").pack()
booking_id_entry = tk.Entry(root)
booking_id_entry.pack(pady=5)
tk.Button(root, text="Cancel Booking", command=cancel_booking, bg="#dc3545", fg="white", width=15).pack(pady=5)

tk.Label(root, text="Room Details", font=("Helvetica", 14, "bold"), bg="#f8f9fa").pack(pady=10)
columns = ("room_id", "room_type", "price", "status")
room_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    room_table.heading(col, text=col.capitalize())
    room_table.column(col, width=150)
room_table.pack()

tk.Button(root, text="Refresh Rooms", command=load_rooms, bg="#007bff", fg="white", width=15).pack(pady=10)

init_db()
load_rooms()
root.mainloop()
