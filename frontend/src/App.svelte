<script lang="ts">
  import type { Asset, LatestRelease } from "./lib/interfaces";
  import { onMount } from "svelte";

  import { Styles } from "sveltestrap";
  import {
    Container,
    Col,
    Row,
    Card,
    CardTitle,
    CardBody,
    CardHeader,
  } from "sveltestrap/src";

  const GITHUB_URL = "latest.json";
  //"https://api.github.com/repos/FelixBetz/smjUlmCalenderGenerator/releases/latest";

  type Calender = Asset[];
  let calenders: Calender[] = [];

  async function getDatabaseTodos() /*: Promise<TodoItem[]>*/ {
    const response = await fetch(GITHUB_URL)
      .then((res) => res.json())
      .then((res: LatestRelease) => {
        calenders[0] = res.assets;
        calenders[1] = res.assets;
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

<Styles />
<main>
  <h1>SMJ Ulm Kalender</h1>

  <Container>
    {#each calenders as assets}
      <Card>
        <CardHeader>
          <CardTitle>{assets[0].name.split("_")[0]}</CardTitle>
        </CardHeader>
        <CardBody>
          <Row>
            {#each assets as asset}
              <Col>
                <a href={asset.browser_download_url}>{asset.name}</a>
              </Col>
            {/each}
          </Row>
        </CardBody>
      </Card>
    {/each}
  </Container>
</main>
