from datetime import timezone, timedelta
import datetime as dt

# first custom date wanted
trigger_time_str = '09:00:00'
today = dt.datetime.now(timezone.utc).date()
custom_trigger = dt.datetime.combine(today, dt.datetime.strptime(trigger_time_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

# second custom date wanted
trigger_time_two_str = '18:00:00'
today = dt.datetime.now(timezone.utc).date()
custom_trigger_two = dt.datetime.combine(today, dt.datetime.strptime(trigger_time_two_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

# current time in utc
utc_time = dt.datetime.now(timezone.utc)

# to account for cross day - midnight
if utc_time > custom_trigger or utc_time > custom_trigger_two:
    custom_trigger += timedelta(days=1)

time_diff = custom_trigger - utc_time

# extract the components of timedelta
days = time_diff.days
seconds = time_diff.seconds
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = (seconds % 3600) % 60

# logic to see if time remaining or time elapsed
if time_diff.total_seconds() > 0:
    print(f"Not pass yet: Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds}, seconds")
elif time_diff.total_seconds() < 0:
    second_time_diff = custom_trigger_two - utc_time

    days = second_time_diff.days
    seconds = second_time_diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    if second_time_diff.total_seconds() > 0:
        print(f"Not pass yet: Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds}, seconds")
    else:
        print("It's currently the time of the trigger (18:00)")

    # print(f"Time has passed already: Time elapsed: {time_diff}")
else:
    print("it's currently the time of zer trigger")

print("Overview:")
print(f"Current Time: {utc_time}")
print(f"Trigger Time: {custom_trigger}")