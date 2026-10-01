import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip


def generate_password():
    try:
        length = int(length_entry.get())
        quantity = int(quantity_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid input",
            "Password length and quantity must be whole numbers."
        )
        return

    if length < 4:
        messagebox.showerror(
            "Invalid length",
            "Password length must be at least 4."
        )
        return

    if quantity < 1:
        messagebox.showerror(
            "Invalid quantity",
            "Generate at least one password."
        )
        return

    characters = string.ascii_letters

    if include_numbers.get():
        characters += string.digits

    if include_symbols.get():
        characters += string.punctuation

    passwords = []

    for _ in range(quantity):
        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )
        passwords.append(password)

    password_text.delete("1.0", tk.END)
    password_text.insert(tk.END, "\n".join(passwords))

    check_password_strength(passwords[0])


def check_password_strength(password=None):
    if password is None:
        password = password_text.get("1.0", tk.END).strip().split("\n")[0]

    if not password:
        strength_label.config(text="Strength: Unknown", fg="gray")
        return

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        strength_label.config(text="Strength: Weak", fg="red")
    elif score <= 4:
        strength_label.config(text="Strength: Medium", fg="orange")
    else:
        strength_label.config(text="Strength: Strong", fg="green")


def copy_passwords():
    passwords = password_text.get("1.0", tk.END).strip()

    if not passwords:
        messagebox.showwarning(
            "Nothing to copy",
            "Generate a password first."
        )
        return

    pyperclip.copy(passwords)
    messagebox.showinfo(
        "Copied",
        "Password(s) copied to the clipboard."
    )


def clear_passwords():
    password_text.delete("1.0", tk.END)
    strength_label.config(text="Strength: Unknown", fg="gray")


# Create the main window
window = tk.Tk()
window.title("Password Generator")
window.geometry("520x500")
window.resizable(False, False)


title_label = tk.Label(
    window,
    text="Password Generator",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)

length_frame = tk.Frame(window)
length_frame.pack(pady=5)

tk.Label(
    length_frame,
    text="Password length:"
).grid(row=0, column=0, padx=5)

length_entry = tk.Entry(length_frame, width=10)
length_entry.insert(0, "16")
length_entry.grid(row=0, column=1, padx=5)


quantity_frame = tk.Frame(window)
quantity_frame.pack(pady=5)

tk.Label(
    quantity_frame,
    text="Number of passwords:"
).grid(row=0, column=0, padx=5)

quantity_entry = tk.Entry(quantity_frame, width=10)
quantity_entry.insert(0, "3")
quantity_entry.grid(row=0, column=1, padx=5)


include_numbers = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=True)

options_frame = tk.Frame(window)
options_frame.pack(pady=10)

numbers_checkbox = tk.Checkbutton(
    options_frame,
    text="Include numbers",
    variable=include_numbers
)
numbers_checkbox.grid(row=0, column=0, padx=10)

symbols_checkbox = tk.Checkbutton(
    options_frame,
    text="Include symbols",
    variable=include_symbols
)
symbols_checkbox.grid(row=0, column=1, padx=10)

# Buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=10)

generate_button = tk.Button(
    buttons_frame,
    text="Generate Passwords",
    command=generate_password,
    width=18
)
generate_button.grid(row=0, column=0, padx=5)

copy_button = tk.Button(
    buttons_frame,
    text="Copy Passwords",
    command=copy_passwords,
    width=18
)
copy_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(
    buttons_frame,
    text="Clear",
    command=clear_passwords,
    width=18
)
clear_button.grid(row=1, column=0, columnspan=2, pady=8)

password_text = tk.Text(
    window,
    height=8,
    width=55,
    font=("Courier New", 11)
)
password_text.pack(pady=10)


strength_label = tk.Label(
    window,
    text="Strength: Unknown",
    font=("Arial", 12, "bold"),
    fg="gray"
)
strength_label.pack(pady=5)

window.mainloop()
