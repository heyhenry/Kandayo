# import time

# my_time = int(input("Enter the time in seconds: "))

# for x in range(my_time, 0, -1):
#     seconds = x % 60
#     minutes = int(x / 60) % 60
#     hours = int(x / 3600)
#     print(f"{hours:02}:{minutes:02}:{seconds:02}")
#     time.sleep(1)

# print("Time's Up!")

import tkinter as tk
from time import strftime

root = tk.Tk()
root.geometry('500x350')

user_seconds = tk.StringVar()

def countdown(user_seconds : int):

    string_time = strftime('%H:%M:%S')
    countdown_display.config(text=string_time)
    countdown_display.after(1000, countdown())

    countdown_display.config(text="Time's Up")

user_lbl = tk.Label(root, text='Input Seconds Til Countdown: ')
user_lbl.grid(row=0, column=0)
user_input = tk.Entry(root, textvariable=user_seconds)
user_input.grid(row=0, column=1)
start_countdown = tk.Button(root, text='Start Countdown', command=lambda:countdown(user_seconds))
start_countdown.grid(row=0, column=2)

countdown_display = tk.Label(root, text='NOTHING')
countdown_display.grid(row=1, columnspan=3)

root.mainloop()