import tkinter as tk
from datetime import datetime, timezone, timedelta

root = tk.Tk()
root.title('Daily Reset Countdown')

def daily_reset():
    
    # the new day trigger
    trigger_str = '00:00:00'
    
    # current time
    utc_time = datetime.now(timezone.utc)

    # setup timedelta obj
    today = utc_time.date()
    trigger = datetime.combine(today, datetime.strptime(trigger_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # calculate time remaining til new day
    time_remaining = (trigger + timedelta(days=1)) - utc_time

    # extract components of the time_remaining timedelta obj
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # create string format of time remaining
    time_remaining_str = f"{hours} hours, {minutes} minutes, {seconds} seconds"

    # update the label responsible for displaying the daily reset timer
    daily_reset_timer.config(text=time_remaining_str)
    # auto execute daily_reset function every second
    daily_reset_timer.after(1000, daily_reset)

# display labels for the daily reset timer
daily_reset_timer = tk.Label(root, font=('calibri', 18, 'bold'))
daily_reset_timer.pack()

# initial execution of daily reset function to jump start the loop
daily_reset()

root.mainloop()

# notes: this algorithm doesn't require and conditional statements as it is only accessing the 24 hour scope in a day