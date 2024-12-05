from datetime import datetime

# Checks to see is the date matches the date_filter
def match_date(timestamp, date_filter):
    date = timestamp.split("T")[0]
    parts = date.split("-")
    filter_parts = date_filter.split("-")

    for i in range(len(parts)):
        if filter_parts[i] != "*" and filter_parts[i] != parts[i]:
            return False
    return True

# Checks to see if the timestamp matches the time_filter
def match_time(timestamp, time_filter):
    time = int(timestamp.split("T")[1].split(":")[0])
    return time_filter  == "*" or time == int(time_filter)

# Checks to see is a record matches the filter_string
def match_filters(record, filter_string):
    filters = filter_string.split(";")
    for f in filters:
        key, value = f.split("=")
        if str(record.get(key)) != value:
            return False

    return True

def filter_data(data, date_filter, time_filter, filter_string):
    filtered = []
    for record in data:
        if match_date(record["timestamp"], date_filter) and \
           match_time(record["timestamp"], time_filter) and \
           match_filters(record, filter_string):
            filtered.append(record)
    return filtered

# Wrote before break, forgot what I was trying to do
def process_data(data, filters):
    if not filters:
        return data

    filtered = []
    for item in data:
        isMatch = True
        for key, val in filters.items():
            if str(item.get(key, "")).lower() != str(val).lower():
                isMatch = False
                break

        if isMatch:
            filtered.append(item)
    return filtered
