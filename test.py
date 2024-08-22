from datetime import timezone
import datetime as dt

# utc_time = dt.datetime.now(timezone.utc)
# my_time = dt.datetime.now()
# utc_time = utc_time.strftime("%H:%M:%S")
# my_time = my_time.strftime("%H:%M:%S")

# print("Current Time: " + my_time)
# print("UTC Time: " + utc_time)

# num = '12:00:00'

# utc_hour = utc_time[0]+utc_time[1]
# utc_min = utc_time[3]+utc_time[4]
# print(utc_hour, utc_min)

check_time = '24:00:00'

utc_time = dt.datetime.now(timezone.utc)
utc_time = utc_time.strftime("%H:%M")

utc_hour = utc_time[0]+utc_time[1]
utc_min = utc_time[3]+utc_time[4]

check_hour = '24'
check_min = '00'
print(utc_time)
def mafs():
    
    hours_left = int(check_hour) - int(utc_hour)
    if int(utc_min) > 0:
        hours_left = hours_left - 1
        mins_left = 60 - int(utc_min)
    print(f"{hours_left}:{mins_left}")

mafs()

# workig out the algorithm to calculate time left til new day in UTC time
