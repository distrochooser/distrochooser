<template>
  <div>
    <div v-for="(facette, index) in facettes" v-bind:key="index">
      <Facette :facette="facette"/>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { onMounted } from "vue";
import { SessionApi, type FacetteSelectionWidget } from "~/sdk";
import { apiConfig, useSessionStore } from "~/states/session";
import Facette from "./facettes/Facette.vue";

interface WidgetProps {
  widget: FacetteSelectionWidget;
}

const props = defineProps<WidgetProps>();

const sessionApi = new SessionApi(apiConfig);
const sessionStore = useSessionStore();

const facettes = useState("facettes", () => []);
const selectedFacettes = useState("selectedFacettes", () => []);


onMounted(async () => {
    facettes.value = sessionStore.session?.resultId
    ? await sessionApi.sessionFacetteList({
        sessionPk: sessionStore.session?.resultId,
        topic: props.widget.topic,
      })
    : []
})
</script>