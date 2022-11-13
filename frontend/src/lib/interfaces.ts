import type { ICalJSON } from "ical-js-parser";

export interface Event {
  name: string;
  description: string;
  startDatetime: Date;
  endDatetime: Date;
  isAllDay: boolean;
  repeatStr: string;
  repeatUntil: Date;
}

export interface Calender {
  name: string;
  url: string;
  events: Event[];
  content: string;
}

export interface IcsFile {
  content: string;
  json: ICalJSON;
}
