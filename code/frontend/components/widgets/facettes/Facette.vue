<template>
  <div>
    <div v-if="props.checkbox">
      {{ selected }} {{ props.facette.id}}<input
        type="checkbox"
        v-model="selected"
        v-on:change="registerChange"
        :checked="isSelected"
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
        :checked="isSelected"
      />
      {{ props.facette.selectableDescription }} {{  isSelected }}
    </div>
    <div>

      <input v-if="isSelected" type="range" v-model="weight" min="-2" max="2" step="1" v-on:change="registerWeightChange"/> 
    </div>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { onMounted, ref } from "vue";
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

const weight = ref(0)

const isSelected = computed(() => store.facetteSelections.filter((l) => l.facette == props.facette.id).length !=0);

const registerChange = async () => {
  await store.updateFacetteSelections(store.currentPage.id, props.facette.id, weight.value, selected.value, !props.checkbox ? 'all': '');
  selected.value = store.facetteSelections.filter((l) => l.facette == props.facette.id).length != 0
  // reset the weight also if the selection was removed
  if (!selected.value) {
    weight.value = 0
  }
};
const registerWeightChange = async() => {
  await store.updateFacetteSelections(store.currentPage.id, props.facette.id, weight.value, selected.value, 'this');
}
</script>