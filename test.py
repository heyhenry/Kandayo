# import datetime as dt

# t = dt.datetime.now()
# print(t.strftime('%H:%M:%S'))

import tkinter as tk
import datetime as dt

win = tk.Tk()
win.title("Display Current Date")
win.geometry("700x350")

date = dt.datetime.now()
label = tk.Label(win, text=f"{date:%H, %M, %S}", font="Calibri, 20")
label.pack(pady=20)

win.mainloop()