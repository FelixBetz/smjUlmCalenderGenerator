import type { IcsFile, Calender, Event } from "./interfaces";
import ICalParser from "ical-js-parser";

interface JsonCalender {
  name: string;
  calenders: string[];
}

const CALENDER_URL = "calenders/calenders.json";

export function repeatStringToGerman(str: string) {
  switch (str) {
    case "DAILY":
      return "täglich";
    case "WEEKLY":
      return "wöchentlich";
    case "MONTHLY":
      return "monatlich";
    case "YEARLY":
      return "jährlich";
    default:
      return "";
  }
}

export function icsTimestampToDate(icsTimestamp: string) {
  let year = icsTimestamp.slice(0, 4);
  let month = icsTimestamp.slice(4, 6);
  let day = icsTimestamp.slice(6, 8);

  let hour = icsTimestamp.slice(9, 11);
  let minute = icsTimestamp.slice(11, 13);
  let seconds = icsTimestamp.slice(13, 15);

  return new Date(Date.UTC(+year, +month - 1, +day, +hour, +minute, +seconds));
}

async function dowloadIcsFile(url: string): Promise<IcsFile> {
  let response = await fetch(url).then((res) => res.text());
  let rawContent = response;
  response = response.replaceAll(';TZID="W. Europe Standard Time"', "");
  return { content: rawContent, json: ICalParser.toJSON(response) };
}

export async function getCalenderAssets(): Promise<Calender[]> {
  let calenders: Calender[] = [];
  const response = await fetch(CALENDER_URL)
    .then((res) => res.json())
    .then(async (res: JsonCalender[]) => {
      for (const calenderGroup of res) {
        for (const calender of calenderGroup.calenders) {
          let cal: Calender = {
            name: calender,
            url: "calenders/" + calenderGroup.name + "/" + calender,
            events: [],
            content: "",
          };
          let icsString: IcsFile = await dowloadIcsFile(cal.url);

          for (let event of icsString.json.events) {
            if (event.dtend == undefined) {
              event.dtend = event.dtstart;
            }

            let repeatStr = "";
            let repeatUntil = null;
            if (event.rrule != undefined) {
              //format of rrule: FREQ=MONTHLY;UNTIL=20230201T235959Z
              let repeatSplit = event.rrule.split(";");
              repeatStr = repeatStringToGerman(repeatSplit[0].split("=")[1]);
              repeatUntil = icsTimestampToDate(repeatSplit[1].split("=")[1]);
            }

            cal.events.push({
              name: event.summary,
              description: event.description,
              startDatetime: icsTimestampToDate(event.dtstart.value),
              endDatetime: icsTimestampToDate(event.dtend.value),
              isAllDay: event.dtstart.isAllDay,
              repeatStr: repeatStr,
              repeatUntil: repeatUntil,
            });
          }

          //sort events by startDatetime
          cal.events.sort((a: Event, b: Event) =>
            a.startDatetime < b.startDatetime ? -1 : 1
          );

          calenders[calenders.length] = cal;
        }
      }
      return calenders;
    })
    .catch((error: Error) => {
      console.log(error);
      return [];
    });
  return response;
}
