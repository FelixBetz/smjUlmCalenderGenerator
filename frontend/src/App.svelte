<script lang="ts">
  import type { Asset, LatestRelease } from "./lib/interfaces";
  import { onMount } from "svelte";

  const GITHUB_URL =
    "https://api.github.com/repos/FelixBetz/smjUlmCalenderGenerator/releases/latest";

  let assets: Asset[] = [];

  async function getDatabaseTodos() /*: Promise<TodoItem[]>*/ {
    const response = await fetch(GITHUB_URL)
      .then((res) => res.json())
      .then((res: LatestRelease) => {
        console.log(res.assets);
        assets = res.assets;
      })
      .catch((error: Error) => {
        console.log(error);
        return [];
      });
    return response;
  }

  onMount(async () => {
    await getDatabaseTodos();
  });
</script>

<main>
  <h1>SMJ Ulm Kalender</h1>
  <ul>
    {#each assets as asset}
      <li><a href={asset.browser_download_url}>{asset.name}</a></li>
    {/each}
  </ul>
</main>
