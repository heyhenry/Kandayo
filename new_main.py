from datetime import datetime, timedelta, timezone

# func to find time remaining based on the given 2 ursus time slots
def time_until_next_ursus(utc_now):

    # ursus times
    uto_start_str = '09:00:00'
    uto_end_str = '13:00:00'
    
    utt_start_str = '18:00:00'
    utt_end_str = '22:00:00'

    # # define the ursus times
    # ursus_time_str = '09:00:00'
    # ursus_time_two_str = '18:00:00'

    # get the current time in utc
    utc_time = utc_now

    # define today's day
    today = utc_now.date()

    # create datetime objects for the triggers today
    uto_start = datetime.combine(today, datetime.strptime(uto_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    uto_end = datetime.combine(today, datetime.strptime(uto_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    utt_start = datetime.combine(today, datetime.strptime(utt_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    utt_end = datetime.combine(today, datetime.strptime(utt_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # see if its currently ursus time
    if utc_time >= uto_start and utc_time <= uto_end:
        print('its ursus time baby (first round)')
    elif utc_time >= utt_start and utc_time <= utt_end:
        print('its ursus time baby (second round)')
    else:

        # determine the next trigger
        if utc_time <= uto_start:
            next_ursus = uto_start
        elif utc_time <= utt_start:
            next_ursus = utt_start
        else:
            # if the current time has passed both ursus times, next ursus is the first ursus of the next day
            next_ursus = uto_start + timedelta(days=1)

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
        datetime(2024, 8, 23, 21, 0, tzinfo=timezone.utc), # after the second trigger, but before the first tigger of the next day
        datetime(2024, 8, 23, 10, 30, 0, tzinfo=timezone.utc),
        datetime(2024, 8, 23, 19, 15, 0, tzinfo=timezone.utc)
    ]

    for test in test_times:
        print("\nRunning test case with UTC time:", test)
        time_until_next_ursus(test)
    
run_tests()
