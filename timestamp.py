from datetime import date
from datetime import datetime

today = date.today()
midnight = datetime.combine(today, datetime.min.time())

timestamp = midnight.timestamp()
print(timestamp)