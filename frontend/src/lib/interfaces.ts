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
}

export interface JsonCalender {
  name: string;
  calenders: string[];
}

export interface ZipFile {
  name: string;
  content: string;
}
