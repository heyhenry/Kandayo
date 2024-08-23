import tkinter as tk
from datetime import datetime, timedelta, timezone

root = tk.Tk()
root.title('Ursus Next When?')

def time_until_next_ursus():

    uto_start_str = '01:00:00'
    uto_end_str = '05:00:00'

    utt_start_str = '18:00:00'
    utt_end_str = '22:00:00'

    utc_time = datetime.now(timezone.utc)
    today = utc_time.date()

    uto_start = datetime.combine(today, datetime.strptime(uto_start_str, "%H:%M:%S").time(), tzinfo=timezone.utc)
    uto_end = datetime.combine(today, datetime.strptime(uto_end_str, "%H:%M:%S").time(), tzinfo=timezone.utc)

    utt_start = datetime.combine(today, datetime.strptime(utt_start_str, "%H:%M:%S").time(), tzinfo=timezone.utc)
    utt_end = datetime.combine(today, datetime.strptime(utt_end_str, "%H:%M:%S").time(), tzinfo=timezone.utc)

    if utc_time >= uto_start and utc_time <= uto_end:
        ursus_lbl.config(text="It's Ursus Time NOW! (Round 1)")
        ursus_lbl.after(1000, time_until_next_ursus)
    elif utc_time >= utt_start and utc_time <= utt_end:
        ursus_lbl.config(text="It's Ursus Time NOW! (Round 2)")
        ursus_lbl.after(1000, time_until_next_ursus)
    else:
        if utc_time <= uto_start:
            next_ursus = uto_start
        elif utc_time <= utt_start:
            next_ursus = utt_start
        else:
            next_ursus = uto_start + timedelta(days=1)

    time_remaining = next_ursus - utc_time

    days = time_remaining.days
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    ursus_lbl.config(text=f"Next Ursus is at {next_ursus.strftime("%H:%M:%S")} & Time Remaining until next Ursus: {time_remaining_str}")
    ursus_lbl.after(1000, time_until_next_ursus)

ursus_lbl = tk.Label(root, font=('Kozuka Gothic Pro B', 12))
ursus_lbl.pack()

time_until_next_ursus()

root.mainloop()