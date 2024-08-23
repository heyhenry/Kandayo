# credit to chatgpt for helping understanding and finding solution

from datetime import datetime, timedelta, timezone

def time_until_next_ursus(utc_now):
    # Define the trigger times
    trigger_one_str = '09:00:00'
    trigger_two_str = '18:00:00'

    # Get current time in UTC
    utc_time = utc_now

    # Define today's date
    today = utc_time.date()

    # Create datetime objects for the triggers today
    trigger_one = datetime.combine(today, datetime.strptime(trigger_one_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    trigger_two = datetime.combine(today, datetime.strptime(trigger_two_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # Determine the next trigger
    if utc_time <= trigger_one:
        next_trigger = trigger_one
    elif utc_time <= trigger_two:
        next_trigger = trigger_two
    else:
        # If current time has passed both triggers, next trigger is the first one of the next day
        next_trigger = trigger_one + timedelta(days=1)

    # Calculate time remaining
    time_remaining = next_trigger - utc_time

    # Extract days, hours, minutes, seconds from the timedelta object
    days = time_remaining.days
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # Format the result
    time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    # Display the result
    print(f"Test Time: {utc_time}")
    print(f"Next Ursus is at {next_trigger.strftime('%H:%M:%S')}")
    print(f"Time remaining until next Ursus: {time_remaining_str}")

# Define test cases
def run_tests():
    # Define the time for the test cases
    test_times = [
        datetime(2024, 8, 23, 4, 0, 0, tzinfo=timezone.utc),    # Before the first trigger
        datetime(2024, 8, 23, 10, 0, 0, tzinfo=timezone.utc),   # Between the first and second trigger
        datetime(2024, 8, 23, 21, 0, 0, tzinfo=timezone.utc),   # After the second trigger
    ]
    
    for test_time in test_times:
        print("\nRunning test case with UTC time:", test_time)
        time_until_next_ursus(test_time)

# Run the test cases
run_tests()


