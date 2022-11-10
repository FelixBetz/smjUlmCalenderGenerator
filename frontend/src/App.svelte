<script lang="ts">
  import { onMount } from "svelte";
  import ICalParser from "ical-js-parser";
  import type { ICalJSON } from "ical-js-parser";
  import { Styles } from "sveltestrap";
  import { Col, Row, Button, Icon, Alert } from "sveltestrap/src";
  import JSZip from "jszip";
  import FileSaver from "file-saver";

  interface Event {
    name: string;
    description: string;
    startDatetime: Date;
    endDatetime: Date;
    isAllDay: boolean;
    repeatStr: string;
    repeatUntil: Date;
  }

  interface Calender {
    name: string;
    url: string;
    events: Event[];
  }

  interface JsonCalender {
    name: string;
    calenders: string[];
  }

  interface ZipFile {
    name: string;
    content: string;
  }

  const CALENDER_URL = "calenders/calenders.json";

  let calenders: Calender[] = [];
  let zipFiles: ZipFile[] = [];

  async function generateZipFile() {
    const zip = new JSZip();
    for (const file of zipFiles) {
      zip.file(file.name, file.content);
    }
    zip.generateAsync({ type: "blob" }).then(function (content) {
      FileSaver.saveAs(content, "download.zip");
    });
  }

  function repeatStringToGerman(str: string) {
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

  function dateMinusOneDay(date: Date) {
    const dayInMillisenconds = 1000 * 60 * 60 * 24; //*1000ms * 60s * 60min *24h = 1 Day
    return new Date(date.getTime() - dayInMillisenconds);
  }

  function formatTime(date: Date) {
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function icsTimestampToDate(icsTimestamp: string) {
    let year = icsTimestamp.slice(0, 4);
    let month = icsTimestamp.slice(4, 6);
    let day = icsTimestamp.slice(6, 8);

    let hour = icsTimestamp.slice(9, 11);
    let minute = icsTimestamp.slice(11, 13);
    let seconds = icsTimestamp.slice(13, 15);

    return new Date(
      Date.UTC(+year, +month - 1, +day, +hour, +minute, +seconds)
    );
  }

  async function dowloadIcsFile(url: string) {
    const response = await fetch(url).then((res) => res.text());
    zipFiles.push({ name: url, content: response });
    return ICalParser.toJSON(response);
  }

  async function getCalenderAssets() /*: Promise<TodoItem[]>*/ {
    zipFiles = [];
    const response = await fetch(CALENDER_URL)
      .then((res) => res.json())
      .then(async (res: JsonCalender[]) => {
        for (const calenderGroup of res) {
          for (const calender of calenderGroup.calenders) {
            let cal: Calender = {
              name: calender,
              url: "calenders/" + calenderGroup.name + "/" + calender,
              events: [],
            };
            let icsString: ICalJSON = await dowloadIcsFile(cal.url);

            for (let event of icsString.events) {
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
      })
      .catch((error: Error) => {
        console.log(error);
        calenders = [];
        return [];
      });
    return response;
  }

  onMount(async () => {
    await getCalenderAssets();
  });
</script>

<Styles />
<main style="padding: 50px;">
  <h1>SMJ Ulm Kalender</h1>
  <Button on:click={generateZipFile}>Alle Kalender herunterladen</Button>
  {#if calenders.length == 0}
    <Alert color="danger">
      <h4 class="alert-heading text-capitalize">Keine Kalender gefunden</h4>
    </Alert>
  {/if}

  <Row>
    {#each calenders as calender}
      <Col style=" padding: 20px;" sm="4">
        <div style="border: 1px solid black; padding: 10px">
          <h5>
            {calender.name}
            <a href={calender.url}>
              <Button>Download <Icon name="download" /></Button>
            </a>
          </h5>

          <ul>
            {#each calender.events as event}
              <li>
                <strong>{event.name}</strong>:<br />
                {event.startDatetime.toLocaleDateString()}{#if event.isAllDay}
                  {#if event.startDatetime.toLocaleDateString() != event.endDatetime.toLocaleDateString()}
                    <i>&nbsp;bis</i>
                    {dateMinusOneDay(event.endDatetime).toLocaleDateString()}
                  {/if}
                {:else if event.startDatetime.toLocaleDateString() == event.endDatetime.toLocaleDateString()}
                  , {formatTime(event.startDatetime)} <i>bis</i>
                  {formatTime(event.endDatetime)} Uhr
                {:else}
                  , {formatTime(event.startDatetime)} Uhr <i>bis</i> <br />
                  {event.endDatetime.toLocaleDateString()}, {formatTime(
                    event.endDatetime
                  )} Uhr
                {/if}
                {#if event.repeatUntil != null}
                  <br />
                  wiederholt sich {event.repeatStr}( bis {event.repeatUntil.toLocaleDateString()})
                {/if}
                {#if event.description != undefined}
                  <br />
                  <i> {event.description}</i>
                {/if}
              </li>
            {/each}
          </ul>
        </div>
      </Col>
    {/each}
  </Row>
</main>
