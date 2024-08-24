import tkinter as tk
from datetime import datetime, timezone, timedelta

root = tk.Tk()
root.title('Daily Reset Countdown')

def daily_reset():
    
    trigger_str = '00:00:00'
    
    utc_time = datetime.now(timezone.utc)

    today = utc_time.date()
    trigger = datetime.combine(today, datetime.strptime(trigger_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    time_remaining = (trigger + timedelta(days=1)) - utc_time

    days = time_remaining.days
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    daily_reset_timer.config(text=time_remaining_str)
    daily_reset_timer.after(1000, daily_reset)

daily_reset_timer = tk.Label(root, font=('calibri', 18, 'bold'))
daily_reset_timer.pack()

daily_reset()

root.mainloop()