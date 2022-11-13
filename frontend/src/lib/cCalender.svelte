<script lang="ts">
  import { Col, Row} from "sveltestrap/src";
  import type { Calender, Event } from "./interfaces";

  export let calender: Calender = null;
  export let style = "";

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

  function isMultiday(event: Event): boolean {
    return (
      event.startDatetime.toLocaleDateString() !=
      event.endDatetime.toLocaleDateString()
    );
  }

  function dayStringByDate(date: Date) {
    const weekday = [
      "Sonntag",
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag",
    ];
    return weekday[date.getDay()];
  }
</script>

<div {style}>
  {#each calender.events as event}
    <Row>
      <Col sm="3">
        <strong>{event.name}</strong>
      </Col>
      <Col sm="3">
        <strong>{event.startDatetime.toLocaleDateString()}</strong>,
        {dayStringByDate(event.startDatetime)}

        {#if isMultiday(event)}
          {#if event.isAllDay}
            -<br />
            <strong>
              {dateMinusOneDay(event.endDatetime).toLocaleDateString()}
            </strong>,
            {dayStringByDate(dateMinusOneDay(event.endDatetime))}
          {:else}
            -<br />
            <strong>
              {event.endDatetime.toLocaleDateString()}
            </strong>,
            {dayStringByDate(event.endDatetime)}
          {/if}
        {/if}
        {#if event.repeatUntil != null}
          <br />
          <i>
            (wiederholt sich {event.repeatStr} bis {event.repeatUntil.toLocaleDateString()})
          </i>
        {/if}
      </Col>

      <Col sm="2">
        {#if event.isAllDay}
          Ganztägig
        {:else if isMultiday(event)}
          Beginn: {formatTime(event.startDatetime)} Uhr <br />
          Ende: {formatTime(event.endDatetime)} Uhr
        {:else}
          {formatTime(event.startDatetime)} -
          {formatTime(event.endDatetime)} Uhr
        {/if}
      </Col>
      <Col sm="4">
        {#if event.description != undefined}
          {event.description}
        {/if}
      </Col>
      <Col />
    </Row>

    <hr />
  {/each}
</div>
