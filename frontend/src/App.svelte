<script lang="ts">
  import { onMount } from "svelte";
  import { Styles } from "sveltestrap";
  import { Button, Icon, Alert } from "sveltestrap/src";
  import JSZip from "jszip";
  import FileSaver from "file-saver";
  import type { Calender } from "./lib/interfaces";
  import { getCalenderAssets } from "./lib/api";
  import CCalender from "./lib/cCalender.svelte";

  let calenders: Calender[] = [];

  let activeTabId = 0;

  async function generateZipFile() {
    const zip = new JSZip();
    for (const calender of calenders) {
      zip.file(calender.name, calender.content);
    }
    zip.generateAsync({ type: "blob" }).then(function (content) {
      FileSaver.saveAs(content, "download.zip");
    });
  }
  function onTabClick(id: number) {
    activeTabId = id;
  }
  onMount(async () => {
    calenders = await getCalenderAssets();
  });
</script>

<Styles />

<main>
  <div style="text-align: center; margin-bottom: 30px">
    <div class="sketchy">SMJ Ulm/Alb/Donau Kalender</div>
  </div>

  <div class="row justify-content-md-center">
    {#if calenders.length > 0}
      {#each calenders as calender}
        <div class="col-md-auto tabs_wrap">
          <div class="row justify-content-md-center">
            <a href={calender.url}>
              <Button outline color="primary">
                {calender.name} <Icon name="download" /></Button
              >
            </a>
          </div>
        </div>
      {/each}
      <div class="col-md-auto tabs_wrap">
        <Button outline color="primary" on:click={generateZipFile}>
          Alle Kalender herunterladen <Icon name="download" /></Button
        >
      </div>
    {/if}
  </div>

  <hr style="12px solid black" />

  <div class="row justify-content-md-center sticky-top" style="background-color: white; padding: 10px">
    <div class="col-md-auto tabs_wrap">
      <ul>
        {#each calenders as calender, i}
          <li
            class={i == activeTabId ? "active" : ""}
            on:click={() => onTabClick(i)}
            on:keydown={() => 2 + 2}
          >
            {calender.name.split("__")[1].split(".")[0]}
          </li>
        {/each}
      </ul>
    </div>
  </div>
  <!-- Contetn begin-->
  <div>
    {#if calenders.length == 0}
      <Alert color="danger">
        <h4 class="alert-heading text-capitalize">Keine Kalender gefunden</h4>
      </Alert>
    {:else}
      {#each calenders as calender, i}
        {#if i == activeTabId}
          <CCalender {calender} style="margin-top: 50px" />
        {/if}
      {/each}
    {/if}
  </div>
</main>

<style>
  main {
    padding-left: 50px;
    padding-right: 50px;
    margin-top: 20px;
  }

  .tabs_wrap ul {
    display: flex;
    margin: 0px;
    padding: 0px;
  }

  .tabs_wrap li {
    list-style: none;
    width: 200px;
    text-align: center;
    background: #e9ecf1;
    border-right: 1px solid #c1c4c9;
    padding: 13px 15px;
    cursor: pointer;
  }

  .tabs_wrap ul li:first-child {
    border-top-left-radius: 25px;
    border-bottom-left-radius: 25px;
  }

  .tabs_wrap ul li:last-child {
    border-right: 0px;
    border-top-right-radius: 25px;
    border-bottom-right-radius: 25px;
  }

  .tabs_wrap ul li:hover,
  .tabs_wrap ul li.active {
    background: #0d6efd;
    color: #fff;
  }



  .sketchy {
    padding: 1rem 2rem;
    display: inline-block;
    border: 3px solid #333;
    font-size: 2.5rem;
    border-radius: 2% 6% 5% 4% / 1% 1% 2% 4%;
    text-transform: uppercase;
    letter-spacing: 0.3ch;
    background: #fff;
    position: relative;
  }
  .sketchy::before {
    content: "";
    border: 2px solid #353535;
    display: block;
    width: 100%;
    height: 100%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate3d(-50%, -50%, 0) scale(1.015) rotate(0.5deg);
    border-radius: 1% 1% 2% 4% / 2% 6% 5% 4%;
  }
</style>
