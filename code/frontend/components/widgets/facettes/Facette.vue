<template>
  <div>
    <div v-if="props.checkbox">
      {{ selected }} {{ props.facette.id}}<input
        type="checkbox"
        v-model="selected"
        v-on:change="registerChange"
        :checked="isSelected()"
      />
      {{ props.facette.selectableDescription }}
    </div>
    <div v-else>
      <pre>{{ selected }}</pre> {{ props.facette.id}}<input
        type="radio"
        v-bind:name="props.facette.topic"
        v-model="selected"
        v-on:change="registerChange"
        v-bind:value="true"
        :checked="isSelected()"
      />
      {{ props.facette.selectableDescription }} {{  isSelected() }}
    </div>
    WEIGHT:
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { onMounted } from "vue";
import { SessionApi, type Facette } from "~/sdk";
import { apiConfig, useSessionStore } from "../../../states/session";

interface CheckboxFacetteProps {
  facette: Facette;
  checkbox: boolean;
}

const props = defineProps<CheckboxFacetteProps>();
const store = useSessionStore();
const selected = useState(
  props.facette.id.toString(),
  () =>
    store.facetteSelections.filter((l) => l.facette == props.facette.id)
      .length != 0
);

const isSelected = () => store.facetteSelections.filter((l) => l.facette == props.facette.id).length !=0;

const registerChange = async () => {
  await store.updateFacetteSelections(props.facette.id, 1, selected.value, !props.checkbox);
  selected.value = store.facetteSelections.filter((l) => l.facette == props.facette.id).length != 0
};
</script>