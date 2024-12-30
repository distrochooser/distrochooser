<template>
  <div>
    <div v-if="props.checkbox">
      {{ selected }} {{ props.facette.id
      }}<input
        type="checkbox"
        v-model="selected"
        v-on:change="registerChange"
        :checked="isSelected"
      />
      {{ props.facette.selectableDescription }}
    </div>
    <div v-else>
      <pre>{{ selected }}</pre>
      {{ props.facette.id
      }}<input
        type="radio"
        v-bind:name="props.facette.topic"
        v-model="selected"
        v-on:change="registerChange"
        v-bind:value="true"
        :checked="isSelected"
      />
      {{ props.facette.selectableDescription }} {{ isSelected }}
    </div>
    <a href="#" v-on:click="toggleExpand">Why</a>
    <div v-if="isExpanded.valueOf()">
      <ul class="list-group">
        <Assignment :assignment="key"  v-for="(key, index) in props.facette.assignments" :key="index" :query-choosables="true" />
      </ul>
    </div>
    <div>
      <input
        v-if="isSelected"
        type="range"
        v-model="weight"
        min="-2"
        max="2"
        step="1"
        v-on:change="registerWeightChange"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { onMounted, ref } from "vue";
import { SessionApi, type Facette } from "~/sdk";
import { apiConfig, useSessionStore } from "../../../states/session";
import Assignment from "./Assignment.vue";

interface CheckboxFacetteProps {
  facette: Facette;
  checkbox: boolean;
}

const props = defineProps<CheckboxFacetteProps>();
const store = useSessionStore();
const selected = useState(
  props.facette.id.toString() + "_selected",
  () =>
    store.facetteSelections.filter((l) => l.facette == props.facette.id)
      .length != 0
);

const weight = ref(0);
const isExpanded = useState(
  props.facette.id.toString() + "_expanded",
  () => false
);
const toggleExpand = () => (isExpanded.value = !isExpanded.value);

const isSelected = computed(
  () =>
    store.facetteSelections.filter((l) => l.facette == props.facette.id)
      .length != 0
);

const registerChange = async () => {
  await store.updateFacetteSelections(
    store.currentPage.id,
    props.facette.id,
    weight.value,
    selected.value,
    !props.checkbox ? "all" : ""
  );
  selected.value =
    store.facetteSelections.filter((l) => l.facette == props.facette.id)
      .length != 0;
  // reset the weight also if the selection was removed
  if (!selected.value) {
    weight.value = 0;
  }
  await store.updateBehaviours();
};
const registerWeightChange = async () => {
  await store.updateFacetteSelections(
    store.currentPage.id,
    props.facette.id,
    weight.value,
    selected.value,
    "this"
  );
};
</script>