
# learnt how to do clock arithmetics
from datetime import datetime

trigger_time_str = '12:00:00'
running_time_str = '14:00:00'

format_str = '%H:%M:%S'
trigger_time = datetime.strptime(trigger_time_str, format_str)
running_time = datetime.strptime(running_time_str, format_str)

result = running_time - trigger_time

print(result)
