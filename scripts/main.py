"""convert csv files into ics files"""
import os
import csv
from datetime import datetime
from pathlib import Path

from ics import Calendar, Event

from calender import OCalender, OEvent

INPUT_DIR = "input"
OUTPUT_DIR = "output"


INDEX_NAME = 0
INDEX_START_DATE = 1
INDEX_START_TIME = 2
INDEX_END_DATE = 3
INDEX_END_TIME = 4

INDEX_CALENDER_CATEGORY = 5


def rmdir(directory):
    """remove directory recursive"""
    if os.path.exists(directory):
        directory = Path(directory)
        for item in directory.iterdir():
            if item.is_dir():
                rmdir(item)
            else:
                item.unlink()
        directory.rmdir()


def string_to_datetime(arg_date, arg_time):
    """convert date string and time string to dateime object"""
    date = datetime.strptime(arg_date, '%m.%d.%Y').date()
    if arg_time == "":
        return date
    time = datetime.strptime(arg_time, "%H:%M").time()
    return datetime.combine(date, time)


def csv_to_o_calender(arg_csv_path):
    """converts csv file to OCalender[]"""
    calender = []
    calender.append(OCalender("gesamt"))
    with open(arg_csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row_index, row in enumerate(reader):
            # parse header line
            if row_index == 0:
                for col_index in range(INDEX_CALENDER_CATEGORY, len(row)):
                    calender.append(OCalender(row[col_index]))
            # parse events properties
            else:
                loc_name = row[INDEX_NAME].strip()

                start_datetime = string_to_datetime(
                    row[INDEX_START_DATE].strip(),
                    row[INDEX_START_TIME].strip())

                end_startime = string_to_datetime(
                    row[INDEX_END_DATE].strip(),
                    row[INDEX_END_TIME].strip())

                loc_event = OEvent(loc_name, start_datetime, end_startime)

                calender[0].append_event(loc_event)
                for col_index in range(INDEX_CALENDER_CATEGORY, len(row)):
                    if row[col_index] == "1":
                        event_index = 1 + col_index - INDEX_CALENDER_CATEGORY
                        calender[event_index].append_event(loc_event)
    return calender


def generate_calenders():
    """generate calenders for each csv file"""
    # remove old output directory
    rmdir(OUTPUT_DIR)

    # create empty outpud directory
    os.makedirs(OUTPUT_DIR)

    # generate calendars for every csv file
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".csv"):

            # generate caldender output dir
            calender_output_dir = OUTPUT_DIR + "/" + filename.split(".")[0]
            os.makedirs(calender_output_dir)
            path = os.path.join(INPUT_DIR, filename)

            # parse from
            calender = csv_to_o_calender(path)

            # generate ics files
            for cal in calender:
                print(cal)
                ics_calender = Calendar()
                for event in cal.events:
                    o_event = Event()
                    o_event.name = event.name
                    o_event.begin = event.start_datetime
                    o_event.end = event.end_datetime
                    ics_calender.events.add(o_event)

                ics_file_name = calender_output_dir + "/" + \
                    filename.split(".")[0] + "__"+cal.name + ".ics"
                with open(ics_file_name, 'w',  encoding="utf-8") as ics_file:
                    ics_file.writelines(ics_calender.serialize_iter())


generate_calenders()
