<script lang="ts">
  import { onMount } from "svelte";
  import ICalParser from "ical-js-parser";
  import type { ICalJSON } from "ical-js-parser";
  import { Styles } from "sveltestrap";
  import { Row, Button, Icon, Alert } from "sveltestrap/src";
  import JSZip from "jszip";
  import FileSaver from "file-saver";
  import type {
    Calender,
    ZipFile,
    Event,
    JsonCalender,
  } from "./lib/interfaces";
  import CCalender from "./lib/cCalender.svelte";

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
    let response = await fetch(url).then((res) => res.text());
    zipFiles.push({ name: url, content: response });
    response = response.replaceAll(';TZID="W. Europe Standard Time"', "");
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
  <h1>
    SMJ Ulm Kalender <Icon name="calendar-date" />
    {#if zipFiles.length > 0}
      <Button color="primary" on:click={generateZipFile}
        >Alle Kalender herunterladen</Button
      >
    {/if}
  </h1>
  {#if calenders.length == 0}
    <Alert color="danger">
      <h4 class="alert-heading text-capitalize">Keine Kalender gefunden</h4>
    </Alert>
  {/if}

  <Row>
    {#each calenders as calender}
      <CCalender {calender} />
    {/each}
  </Row>
</main>
