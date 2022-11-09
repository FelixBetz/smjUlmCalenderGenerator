"""collection of classes for an ics calender"""


class OEvent:
    """represents an ics event"""

    def __init__(self, name, start_datetime, end_datetime) -> None:
        self.name = name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.description = ""
        self.location = ""

    def __str__(self):
        return self.name + ": " + str(self.start_datetime) + " to " + str(self.end_datetime)

    def get_duration(self):
        """returns event"""
        return self.end_datetime - self.start_datetime


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
