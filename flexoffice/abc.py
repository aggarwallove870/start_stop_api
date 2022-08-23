from datetime import datetime
import calendar
date = datetime.now()



number_of_days = calendar.monthrange(date.year, 3)[1]
print(number_of_days)