<script lang="ts">
  import type { LatestRelease } from "./lib/interfaces";
  import { onMount } from "svelte";
  import ICalParser from "ical-js-parser";
  import type { ICalJSON } from "ical-js-parser";
  import { Styles } from "sveltestrap";
  import { Col, Row, Button, Icon } from "sveltestrap/src";

  interface Event {
    name: string;
    description: string;
    startDatetime: Date;
    endDatetime: Date;
  }

  interface Calender {
    name: string;
    url: string;
    events: Event[];
  }

  const GITHUB_URL =
    "https://api.github.com/repos/FelixBetz/smjUlmCalenderGenerator/releases/latest";

  let calenders: Calender[] = [];

  function icsTimestampToDate(icsTimestamp: string) {
    let year = icsTimestamp.slice(0, 4);
    let month = icsTimestamp.slice(6, 8);
    let day = icsTimestamp.slice(4, 6);

    let hour = icsTimestamp.slice(9, 11);
    let minute = icsTimestamp.slice(11, 13);
    let seconds = icsTimestamp.slice(13, 15);

    return new Date(+year, +month, +day, +hour, +minute, +seconds);
  }

  async function dowloadIcsFile(url: string) {
    const response = await fetch(url,{ mode: 'no-cors'}).then((res) => res.text());
    return ICalParser.toJSON(response);
  }

  async function getCalenderAssets() /*: Promise<TodoItem[]>*/ {
    const response = await fetch(GITHUB_URL)
      .then((res) => res.json())
      .then(async (res: LatestRelease) => {
        for (const asset of res.assets) {
          let cal: Calender = {
            name: asset.name,
            url: asset.browser_download_url,
            events: [],
          };
          let icsString: ICalJSON = await dowloadIcsFile(cal.url);

          for (let event of icsString.events) {
            cal.events.push({
              name: event.summary,
              description: event.description,
              startDatetime: icsTimestampToDate(event.dtstart.value),
              endDatetime: icsTimestampToDate(event.dtend.value),
            });
          }
          calenders[calenders.length] = cal;
        }
      })
      .catch((error: Error) => {
        console.log(error);
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

                {event.startDatetime.toLocaleDateString()}
                {#if event.endDatetime.getHours() != 0}
                  , {event.startDatetime.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })} Uhr{/if}
                <i>bis</i> <br />

                {event.endDatetime.toLocaleDateString()}

                {#if event.endDatetime.getHours() != 0}
                  , {event.endDatetime.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })} Uhr
                {/if}
                {#if event.description != undefined}
                  <br />
                  {event.description}
                {/if}
              </li>
            {/each}
          </ul>
        </div>
      </Col>
    {/each}
  </Row>
</main>
