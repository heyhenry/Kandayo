from datetime import timezone, timedelta
import datetime as dt

trigger_time_str = '09:00:00'
today = dt.datetime.now(timezone.utc).date()

custom_trigger = dt.datetime.combine(today, dt.datetime.strptime(trigger_time_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

utc_time = dt.datetime.now(timezone.utc)
# string_time = utc_time.strftime('%H:%M:%S %p')
# print(string_time)

if utc_time > custom_trigger:
    custom_trigger += timedelta(days=1)

time_diff = custom_trigger - utc_time

# extract the components of timedelta
days = time_diff.days
seconds = time_diff.seconds
hours = seconds // 3600
minutes = (seconds % 3600) // 60
seconds = (seconds % 3600) % 60

if time_diff.total_seconds() > 0:
    print(f"Not pass yet: Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds}, seconds")
elif time_diff.total_seconds() < 0:
    time_diff = dt.datetime.strftime()
    print(f"Time has passed already: Time elapsed: {time_diff}")
else:
    print("it's currently the time of zer trigger")

print("Overview:")
print(f"Current Time: {utc_time}")
print(f"Trigger Time: {custom_trigger}")