from datetime import datetime
date = "19/Apr/2022 10:20 AM"
date = datetime.strptime(date, "%d/%b/%Y %H:%M %p")
date.strftime("%Y-%m-%d")
print(date.date())
