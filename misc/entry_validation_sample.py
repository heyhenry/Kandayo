# https://www.geeksforgeeks.org/python-tkinter-validating-entry-widget/

# import tkinter as tk

# def callback(input):

#     if input.isdigit():
#         print(input)
#         return True
#     elif input is "":
#         print(input)
#         return True
#     else:
#         print(input)
#         return False

# root = tk.Tk()

# e = tk.Entry(root)
# e.place(x=50, y=50)
# reg = root.register(callback)
# e.config(validate='key', validatecommand=(reg, '%P'))

# root.mainloop()


# https://www.geeksforgeeks.org/validating-entry-widget-in-python-tkinter/
# import modules
import tkinter as tk
from tkinter import messagebox

# function to check valid phone number
def validate_phone(phone):
    if phone.isdigit() and len(phone) == 10:
        return True
    return False

# function called when Submit is ckicked
def on_submit():
    phone = phone_entry.get()
    if not validate_phone(phone):
        messagebox.showerror("Invalid Input",
                             "Phone number must be exactly 10 digits.")
    else:
        messagebox.showinfo("Valid Input",
                            "Phone number is valid.")

# main Tkinter application window
root = tk.Tk()
root.title("Phone Number Validation")
root.geometry("300x200")

# tkinter widgets
phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

# sumit buttion to check validity
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack()

root.mainloop()
