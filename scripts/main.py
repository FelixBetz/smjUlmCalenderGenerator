"""convert csv files into ics files"""
import os
import csv
from datetime import datetime
from pathlib import Path

import json
from ics import Calendar, Event

from calender import OCalender, OEvent

INPUT_DIR = "../input"
OUTPUT_DIR = "../frontend/public/calenders"
JSON_NAME = "calenders.json"

INDEX_NAME = 0
INDEX_START_DATE = 1
INDEX_START_TIME = 2
INDEX_END_DATE = 3
INDEX_END_TIME = 4
INDEX_DESCRIPTION = 5
INDEX_LOCATION = 6
INDEX_CATEGORIES = 7

INDEX_CALENDER = 8


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


def string_to_date(arg_date):
    """convert date string and time string to dateime object"""
    return datetime.strptime(arg_date.strip(), '%d.%m.%Y').date()


def string_to_time(arg_time):
    """convert date string and time string to dateime object"""
    if arg_time == "":
        return None
    return datetime.strptime(arg_time.strip(), "%H:%M").time()


def csv_to_o_calender(arg_csv_path):
    """converts csv file to OCalender[]"""
    calender = []
    calender.append(OCalender("gesamt"))
    with open(arg_csv_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row_index, row in enumerate(reader):
            # parse header line
            if row_index == 0:
                for col_index in range(INDEX_CALENDER, len(row)):
                    calender.append(OCalender(row[col_index]))

            # skip empty rows
            elif row[0] == "":
                pass
            # parse events properties
            else:
                loc_start_datetime = (string_to_date(row[INDEX_START_DATE]),
                                      string_to_time(row[INDEX_START_TIME]))

                loc_end_datetime = (string_to_date(row[INDEX_END_DATE]),
                                    string_to_time(row[INDEX_END_TIME]))

                loc_event = OEvent(row[INDEX_NAME].strip(),
                                   loc_start_datetime,
                                   loc_end_datetime,
                                   )

                loc_event.location = row[INDEX_LOCATION]
                loc_event.description = row[INDEX_DESCRIPTION]
                loc_categories = []
                for cat in row[INDEX_CATEGORIES].split(","):
                    loc_categories.append(cat.strip())
                loc_event.categories = loc_categories

                calender[0].append_event(loc_event)
                for col_index in range(INDEX_CALENDER, len(row)):
                    if row[col_index] == "1":
                        event_index = 1 + col_index - INDEX_CALENDER
                        calender[event_index].append_event(loc_event)

    return calender


def write_calenders_json_file(data):
    """gernate caleners.json file"""
    # Serializing json
    json_object = json.dumps(data, indent=4)

    # Writing to sample.json
    with open(OUTPUT_DIR+"/"+JSON_NAME, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)


def generate_calenders():
    """generate calenders for each csv file"""
    # remove old output directory
    rmdir(OUTPUT_DIR)

    # create empty outpud directory
    os.makedirs(OUTPUT_DIR)

    calender_names = []

    # generate calendars for every csv file
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".csv"):

            # generate caldender output dir
            calender_name = filename.split(".")[0]
            calender_output_dir = OUTPUT_DIR + "/" + calender_name
            os.makedirs(calender_output_dir)
            path = os.path.join(INPUT_DIR, filename)

            # parse from
            calender = csv_to_o_calender(path)

            ics_names = []

            # generate ics files
            for cal in calender:
                ics_calender = Calendar(creator="SMJ Ulm/Alb/Donau")

                for o_event in cal.events:
                    event = Event()
                    event.name = o_event.name
                    event.begin = o_event.get_datetime_start()
                    event.end = o_event.get_datetime_end()
                    event.description = o_event.description
                    event.location = o_event.location
                    event.categories = o_event.categories
                    if o_event.start_datetime[1] is None or o_event.end_datetime[1] is None:
                        print("all day", o_event)
                        # event.make_all_day()
                    ics_calender.events.add(event)

                ics_file_name = filename.split(".")[0] + "__"+cal.name + ".ics"
                output_path = calender_output_dir + "/" + ics_file_name

                ics_names.append(ics_file_name)
                with open(output_path, 'w',  encoding="utf-8") as ics_file:
                    ics_file.writelines(ics_calender.serialize_iter())

            calender_names.append(
                {"name": calender_name, "calenders": ics_names})

            print("---------------------------------------------------------------")
            for cal in calender:
                print(cal)

    write_calenders_json_file(calender_names)


generate_calenders()
