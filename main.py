from datetime import datetime, timedelta, timezone

# func to find time remaining based on the given 2 ursus time slots
def time_until_next_ursus(utc_now):

    # define the ursus times
    ursus_time_str = '09:00:00'
    ursus_time_two_str = '18:00:00'

    # get the current time in utc
    utc_time = utc_now

    # define today's day
    today = utc_now.date()

    # create datetime objects for the triggers today
    ursus_time = datetime.combine(today, datetime.strptime(ursus_time_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    ursus_time_two = datetime.combine(today, datetime.strptime(ursus_time_two_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # determine the next trigger
    if utc_time <= ursus_time:
        next_ursus = ursus_time
    elif utc_time <= ursus_time_two:
        next_ursus = ursus_time_two
    else:
        # if the current time has passed both ursus times, next ursus is the first ursus of the next day
        next_ursus = ursus_time + timedelta(days=1)

    # calcualte time remaining
    time_remaining = next_ursus - utc_time

    # extract the components of the time_remaining obj (timedelta obj)
    days = time_remaining.days
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # format the result
    time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    # display the result
    print(f"Test Time: {utc_time}")
    print(f"Next Ursus is at {next_ursus.strftime("%H:%M:%S")}")
    print(f"Time remaining until next Ursus: {time_remaining_str}")

# define test cases
def run_tests():
    # define the time for the test cases
    test_times = [
        datetime(2024, 8, 23, 4, 0, 0, tzinfo=timezone.utc), # before the first trigger 
        datetime(2024, 8, 23, 10, 0, 0, tzinfo=timezone.utc), # before the second trigger but after the first trigger
        datetime(2024, 8, 23, 21, 0, tzinfo=timezone.utc) # after the second trigger, but before the first tigger of the next day
    ]

    for test in test_times:
        print("\nRunning test case with UTC time:", test)
        time_until_next_ursus(test)
    
run_tests()