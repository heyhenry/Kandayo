from datetime import datetime, timedelta, timezone

# define trigger times
trigger_time_str = '09:00:00'
trigger_time_two_str = '18:00:00'

# get current time in utc
utc_time = datetime.now(timezone.utc)

# define today's date and create datetime objects for the triggers
today = utc_time.date()
custom_trigger = datetime.combine(today, datetime.strptime(trigger_time_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
custom_trigger_two = datetime.combine(today, datetime.strptime(trigger_time_two_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

# adjust for crossing midnight
if utc_time > custom_trigger_two:
    custom_trigger += timedelta(days=1)
    custom_trigger_two += timedelta(days=1)
elif utc_time > custom_trigger:
    # if the current time has passed the first trigger but not the second trigger
    custom_trigger_two += timedelta(days=1)

# determine which trigger to use
if utc_time > custom_trigger_two:
    # if passed both triggers, calculate time until next day's first trigger
    custom_trigger = custom_trigger_two + timedelta(days=1)
    time_diff = custom_trigger - utc_time
    print(f"Not passed yet: Time remaining until next day's first trigger: {time_diff}")
else:
    # calculate time difference to the closest trigger
    if utc_time < custom_trigger:
        time_diff = custom_trigger - utc_time
        print(f"Not passed yet: Time remaining: {time_diff}")
    else:
        time_diff = custom_trigger_two - utc_time
        if time_diff.total_seconds() > 0:
            print(f"Not passed yet: Time remaining until second trigger: {time_diff}")
        else:
            print("It's currently the tiem of the second trigger (18:00)")

# print overview
print("Overview:")
print(f"Current Time: {utc_time}")
print(f"First Trigger Time: {custom_trigger}")
print(f"Second Trigger Time: {custom_trigger_two}")

