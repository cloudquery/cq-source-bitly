from dateutil.relativedelta import relativedelta
from datetime import datetime

# # Current date
# current_date = datetime.now()

# # Parse relative date string
# relative_date_string = "-1 month"
# delta = relativedelta(months=1) if "month" in relative_date_string else relativedelta(days=1) if "day" in relative_date_string else None

# if delta:
#     new_date = current_date + delta
#     print(new_date)
# else:
#     print("Invalid relative date string.")

def get_date(input: str):
    # check if the input is a date
    try:
        return datetime.strptime(input, "%Y-%m-%d")
    except ValueError:
        pass
    if " " not in input:
        raise ValueError("Invalid relative date string.") 

    parts = input.split(" ")
    try:
        value = int(parts[0])
    except ValueError:
        raise ValueError("Invalid relative date string.")

    unit = parts[1]
    
    if unit in ["day", "days"]:
        return (datetime.now() + relativedelta(days=int(value)))
    
    if unit in ["week", "weeks"]:
        return (datetime.now() + relativedelta(weeks=int(value)))
    
    raise ValueError("Invalid relative date string.")
