import datetime
from time import timezone


def calc_time_offsets(self, schedule):
    """regimen : A yaml object that includes this:
       schedule: {group: [optional], type: [optional], days: [], times: [], actions: <<list of actions or name of sequence>>}
       OR
       schedule: {group: [optional], type: [optional], every: 4, unit: "minutes/hours/days/weeks/months/years", max: 10, actions: <<list of actions or name of sequence>>}
       returns : a list of integers that are time_offset(s) for CeleryScript"""
    time_offsets = []
    if "days" in schedule:
        days = schedule["days"]
        times = []
        for time in schedule["times"]:
            times.append(int(time[0:2]) * 60 * 60 * 1000 + int(time[3:]) * 60 * 1000)
        now = datetime.datetime.now()
        for day in days:
            begin = (day - 1) * 24 * 60 * 60 * 1000
            for time in times:
                time_offsets.append(begin + time)
    elif "every" in schedule:
        every = schedule["every"]
        unit = schedule["unit"]
        period = 0
        if unit == "minutes":
            period = every * 60 * 1000
        elif unit == "hours":
            period = every * 60 * 60 * 1000
        elif unit == "days":
            period = every * 24 * 60 * 60 * 1000
        elif unit == "weeks":
            period = every * 7 * 24 * 60 * 60 * 1000
        elif unit == "months":
            period = every * 30 * 24 * 60 * 60 * 1000
        elif unit == "years":
            period = every * 365 * 24 * 60 * 60 * 1000
        for i in range(0, schedule["max"]):
            time_offsets.append(i * period)
    return time_offsets


def format_time(self, time):
    """time: DD/MM/YYYY 23:00
       returns: YYYY-MM-DDT23:00:00.000Z aka ISO 8601 date representation, local time."""
    string = time[6:10]+"-"+time[3:5]+"-"+time[0:2]+"T"+time[11:]+":00"
    tz = int(timezone / 3600.0)
    if tz < 0:
        return string + str(tz) + ":00"
    else:
        return string + "+" + str(tz) + ":00"