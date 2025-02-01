<!--
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
<template>
  <div>
    <div class="form-check" v-if="props.checkbox">
      <input class="form-check-input" v-model="selected" v-on:change="registerChange" :checked="isSelected"
        type="checkbox" :id="facette.id.toString()">
      <label class="form-check-label" :for="facette.id.toString()">
        {{ props.facette.selectableDescription }}
      </label>
      <BehaviourButton :title="store.__i('why')" :click-handler="toggleExpand"/>
    </div>
    <div class="form-check" v-else>
      <input v-on:click="registerClick" class="form-check-input" type="radio" v-bind:name="props.facette.topic"
        v-model="selected" v-on:change="registerChange" v-bind:value="true" :checked="isSelected"
        :id="facette.id.toString()">
      <label v-on:click="registerClick"  class="form-check-label" :for="facette.id.toString()">
        {{ props.facette.selectableDescription }}
      </label>
      
      <BehaviourButton :title="store.__i('why')" :click-handler="toggleExpand"/>
    </div>

    <div v-if="isExpanded.valueOf()">
      <ul class="list-group">
        <Assignment :assignment="key" v-for="(key, index) in props.facette.assignments" :key="index"
          :query-choosables="true" :facette="props.facette" />
      </ul>
    </div>
    <div>
      <input v-if="isSelected" type="range" v-model="weight" min="-2" max="2" step="1"
        v-on:change="registerWeightChange" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { computed, ref } from "vue";
import { type Facette } from "../../../sdk";
import { useSessionStore } from "../../../states/session";
import Assignment from "./Assignment.vue";
import BehaviourButton from "./BehaviourButton.vue";

interface CheckboxFacetteProps {
  facette: Facette;
  checkbox: boolean;
  topic: string;
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
const registerClick = async () => {
  if (isSelected.value) {
    await store.updateFacetteSelections(
      store.currentPage.id,
      props.facette.id,
      0,
      false,
      !props.checkbox ? "all" : ""
    )
  }
}
const registerChange = async () => {
  // FIXME: For Radio facettes: They can never be unchecked
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
