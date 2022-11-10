"""collection of classes for an ics calender"""
from datetime import datetime


class OEvent:
    """represents an ics event"""

    def __init__(self, name, start_datetime, end_datetime) -> None:
        self.name = name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.description = ""
        self.location = ""
        self.categories = ""
        self.repeat = None

    def __str__(self):
        return self.name + ": " + \
            str(self.start_datetime[0]) + "," + str(self.start_datetime[1]) + " to "\
            + str(self.end_datetime[0])+"," + str(self.end_datetime[1])

    def __combine_datetime(self, arg_datetime):
        """combine date and time as datetime """
        if arg_datetime[0] is None:
            return None
        if arg_datetime[1] is None:
            return datetime.combine(arg_datetime[0], datetime.min.time()).astimezone()
        return datetime.combine(arg_datetime[0], arg_datetime[1]).astimezone()

    def get_datetime_start(self):
        """"combine date and time as datetime"""
        return self.__combine_datetime(self.start_datetime)

    def get_datetime_end(self):
        """"combine date and time as datetime"""
        return self.__combine_datetime(self.end_datetime)

    def get_repeat(self):
        """returns repeat freq"""
        return self.repeat[0]

    def get_repeat_until_str(self):
        """returns repeat until as ics date string"""
        year = str(self.repeat[1].year).zfill(4)
        month = str(self.repeat[1].month).zfill(2)
        day = str(self.repeat[1].day).zfill(2)
        return year+month+day+"T"+"235959Z"


class OCalender:
    """represents an ics calender"""

    def __init__(self, name) -> None:
        self.name = name
        self.events = []

    def __str__(self):
        ret_string = self.name + ":\n"
        for idx, event in enumerate(self.events):
            ret_string += "\t[" + str(idx)+"]: "+str(event)+"\n"
        return ret_string

    def append_event(self, arg_event):
        """append ics events to the events list"""
        self.events.append(arg_event)
