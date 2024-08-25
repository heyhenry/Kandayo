from datetime import datetime, timezone, timedelta
import tkinter as tk

root = tk.Tk()
root.title('Weekly Reset Timer')

def weekly_reset():

    # getting current utc datetime and other details
    utc_time = datetime.now(timezone.utc)
    today = utc_time.date()
    current_weekday = utc_time.weekday()

    # the target day aka thursday
    target_weekday = 3

    # calculate how many days til target day
    days_until_target = (target_weekday - current_weekday + 7) % 7

    # check to see if today is target day and reset to 7 days if its today
    if days_until_target == 0:
        days_until_target = 7

    # next thursday timedelta obj
    next_thursday_date = today + timedelta(days=days_until_target)

    # target day settings 
    trigger_str = '00:00:00'
    trigger_time = datetime.strptime(trigger_str, '%H:%M:%S').time()
    
    # next thursday date time obj
    next_thursday = datetime.combine(next_thursday_date, trigger_time, tzinfo=timezone.utc)

    # check if today is the target day
    if utc_time.weekday() == 3:
        print("today's thursday cool!")
        weekly_reset_timer.after(1000, weekly_reset)
    # if its not the target day..
    else:
        # calculate time remaining til next thursday from today
        time_remaining = next_thursday - utc_time

        # extract time_remaining time delta obj's components
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60

        # format information into string
        time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        weekly_reset_timer.config(text=time_remaining_str)
        weekly_reset_timer.after(1000, weekly_reset)

# tkinter widgets
weekly_reset_timer = tk.Label(root, font=('calibri', 18, 'bold'), background='white', foreground='black')
weekly_reset_timer.pack()

# execute initial loop for weekly reset timer
weekly_reset()

root.mainloop()



