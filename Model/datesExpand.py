import calendar


def expand_dates(date: str) -> list:
    dates = date.split("-")

    start_day, start_month, = dates[0].split(":")
    end_day, end_month = dates[1].split(":")

    end_day = int(end_day)
    end_month = int(end_month)
    start_day = int(start_day)
    start_month = int(start_month)
    day = int(start_day)
    month = int(start_month)

    dates_list = [f"{start_month}:{start_day}"]

    while True:
        if day < calendar.monthrange(2024, month)[1]:
            day += 1
            dates_list.append(f"{day}:{month}")

        if day >= calendar.monthrange(2024, month)[1]:
            day = 1
            month += 1
            dates_list.append(f"{day}:{month}")

        if month >= end_month and day >= end_day:
            break

    return dates_list


example = expand_dates("28:01-3:02")
print(example)
