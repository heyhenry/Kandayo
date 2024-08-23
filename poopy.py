from datetime import date, time, timedelta, timezone
import datetime as dt

now = dt.datetime.now()
current_time = datetime(now.hour, now.minute, now.second)

format_str = '%H:%M:%S'
trigger_time_str = '12:00:00'
trigger_time = dt.datetime.strptime(trigger_time_str, format_str)
print(current_time - trigger_time)