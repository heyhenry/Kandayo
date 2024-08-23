# Credit for helpful resource: https://handhikayp.medium.com/generate-a-simple-digital-clock-with-python-tkinter-796a5b298872

from datetime import timezone
import datetime
import tkinter as tk

root = tk.Tk()
root.title("UTC Live Time")

def update_time():
    utc_time = datetime.datetime.now(timezone.utc)
    string_time = utc_time.strftime('%H:%M:%S')
    digital_clock.config(text=string_time)
    digital_clock.after(1000, update_time)

digital_clock = tk.Label(root, font=('calibri', 40, 'bold'), background='black', foreground='white')
digital_clock.pack(pady=20)

update_time()

root.mainloop()

