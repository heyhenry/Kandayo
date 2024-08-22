import tkinter as tk
from datetime import timezone
import datetime as dt

root = tk.Tk()
root.resizable(False, False)

# frames setup
yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nwse')
red_frame.grid(rowspan=4, column=0, sticky='nwse')
blue_frame.grid(row=1, column=1, sticky='nwse')
magenta_frame.grid(row=2, column=1, sticky='nwse')
orange_frame.grid(row=3, column=1, sticky='nwse')
green_frame.grid(row=4, column=1, sticky='nwse')

# to not ignore frame attributes when widgets are introduced
yellow_frame.grid_propagate(False)
red_frame.grid_propagate(False)

# yellow frame
co_lbl = tk.Label(yellow_frame, text='Characters Overview', font=('Kozuka Gothic Pro B', 18), bg='yellow')
co_lbl.place(relx=0.5, rely=0.5, anchor='center')

# red frame
chars_lb = tk.Listbox(red_frame, height=30)
chars_lb.place(relx=0.5, rely=0.5, anchor='center')

# blue frame

# to check if buttons are working correctly
def run(i : str):
    if i == 'add':
        print('add works')
    elif i == 'upd':
        print('update works')
    elif i == 'del':
        print('delete works')
    else:
        print('Error!')

blue_buttons = {'font':('Kozuka Gothic Pro B', 12), 'relief': 'raised'}

addchar_btn = tk.Button(blue_frame, text='Add Char', **blue_buttons, command=lambda:run('add'))
updchar_btn = tk.Button(blue_frame, text='Update Char', **blue_buttons, command=lambda:run('upd'))
delchar_btn = tk.Button(blue_frame, text='Delete Char', **blue_buttons, command=lambda:run('del'))

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)
blue_frame.grid_columnconfigure(2, weight=1)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=0, column=2)

# magenta frame

# get current utc time
utc_time = dt.datetime.now(timezone.utc)
utc_time = utc_time.strftime("%H:%M")

# split hour and min vars
utc_hour = utc_time[0]+utc_time[1]
utc_min = utc_time[3]+utc_time[4]

# hour and min for max utc
maxutc_hour = '24'
maxutc_min = '00'

# daily reset time remaining
dr_remaining = tk.StringVar()

def daily_reset_mafs():
    hours_left = int(maxutc_hour) - int(utc_hour)
    if int(utc_min) > 0:
        hours_left = hours_left - 1
        mins_left = 60 - int(utc_min)
    dr_remaining.set(f"{hours_left} hours and {mins_left} minutes til daily reset.")
    daily_reset_display.config(textvariable=dr_remaining)

# temp using blue_button params
utc_time = tk.Button(magenta_frame, text='Current Time (UTC)', **blue_buttons)
ursus_time = tk.Button(magenta_frame, text='Til Next Ursus', **blue_buttons)
daily_reset = tk.Button(magenta_frame, text='Til Daily Reset', **blue_buttons, command=daily_reset_mafs)
weekly_reset = tk.Button(magenta_frame, text='Til Weekly Reset', **blue_buttons)

utc_time_display = tk.Label(magenta_frame)
ursus_time_display = tk.Label(magenta_frame)
daily_reset_display = tk.Label(magenta_frame)
weekly_reset_display = tk.Label(magenta_frame)

magenta_frame.grid_rowconfigure(0, weight=1)
magenta_frame.grid_rowconfigure(1, weight=1)
magenta_frame.grid_rowconfigure(2, weight=1)
magenta_frame.grid_rowconfigure(3, weight=1)
magenta_frame.grid_columnconfigure(0, weight=1)
magenta_frame.grid_columnconfigure(1, weight=1)

utc_time.grid(row=0, column=0)
ursus_time.grid(row=1, column=0)
daily_reset.grid(row=2, column=0)
weekly_reset.grid(row=3, column=0)

utc_time_display.grid(row=0, column=1)
ursus_time_display.grid(row=1, column=1)
daily_reset_display.grid(row=2, column=1)
weekly_reset_display.grid(row=3, column=1)

# root configs for resizability ('can ignore for time being, may reinstate later')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

