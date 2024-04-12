import datetime

# Given Unix timestamp
timestamp = 1700243473

# Convert Unix timestamp to a datetime object in UTC
comment_date = datetime.datetime.utcfromtimestamp(timestamp)

# Extract hours, minutes, and seconds
hours = comment_date.hour
minutes = comment_date.minute
seconds = comment_date.second

# Print the full date and time, and the individual time components
print("Full date and time:", comment_date.strftime('%Y-%m-%d %H:%M:%S'))
print("Hour:", hours)
print("Minute:", minutes)
print("Second:", seconds)