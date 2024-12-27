<template>
  <div>
    {{ props.widget.facettes  }}
    <Behaviour v-for="(facette, index) in props.widget.facettes" v-bind:key="index"  :facette="facette"/>
    <div v-for="(facette, index) in props.widget.facettes" v-bind:key="index">
      <Facette :facette="facette" :checkbox="props.checkbox"/>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useAsyncData, useState } from "nuxt/app";
import { onMounted } from "vue";
import { SessionApi, type FacetteSelectionWidget } from "~/sdk";
import { apiConfig, useSessionStore } from "~/states/session";
import Facette from "./facettes/Facette.vue";
import Behaviour from "./facettes/Behaviour.vue";

interface WidgetProps {
  widget: FacetteSelectionWidget;
  checkbox: boolean;
}

const props = defineProps<WidgetProps>();
</script>