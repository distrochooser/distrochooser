<!--
distrochooser
Copyright (C) 2014-2025 Christoph Müller  <mail@chmr.eu>

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
  <div class="row">
    <div class="col-lg-12 col-xl-9">
      <div :class="{'form-check mb-2 fs-6': true, 'a11y-larger-text': store.fontSizeModifier == 5}" v-if="props.checkbox">
        <input class="form-check-input" v-model="selected" v-on:change="registerChange" :checked="isSelected"
          type="checkbox" :id="facette.id.toString()" v-show="!store.isTranslating">
        <label class="form-check-label" :for="facette.id.toString()">
          <LanguageTranslation :translation-key="props.facette.selectableDescription"/>
        </label>
        <BehaviourButton :click-handler="toggleExpand" v-show="!store.isTranslating" />
      </div>
      <div :class="{'form-check mb-2 fs-6': true, 'a11y-larger-text': store.fontSizeModifier == 5}" v-else>
        <input v-on:click="registerClick"  v-show="!store.isTranslating" class="form-check-input" type="radio" v-bind:name="props.facette.topic"
          v-model="selected" v-on:change="registerChange" v-bind:value="true" :checked="isSelected"
          :id="facette.id.toString()">
        <label v-on:click="registerClick" class="form-check-label" :for="facette.id.toString()">
          <LanguageTranslation :translation-key="props.facette.selectableDescription"/>
        </label>

        <BehaviourButton :click-handler="toggleExpand" v-show="!store.isTranslating"/>
      </div>
    </div>
    <div class="col-lg-12 col-xl-3 row mb-2" v-if="isSelected" >
      <Icon class="col fs-2 less-weight-icon" name="ion:chevron-down-circle-sharp"></Icon>
      <div class="col">
        <input :id="'importance-'+ props.facette.id" type="range" v-model="weight" min="-2" max="2" step="1" class="align-middle"  v-on:change="registerWeightChange" />
      </div>
      <Icon class="col fs-2 more-weight-icon" name="ion:chevron-up-circle-sharp"></Icon>
    </div>
  </div>

  <div v-if="isExpanded.valueOf()">
      <ul class="list-group">
        <li v-if="props.facette.assignments.length == 0"
          class="list-group-item d-flex justify-content-between align-items-start">
          <LanguageTranslation translation-key="no-mappings-for-this-facette"/>
        </li>
        <Assignment :display-weigth="false" :assignment="key" v-for="(key, index) in props.facette.assignments" :key="index"
          :query-choosables="true" :facette="props.facette" />
      </ul>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { computed, ref } from "vue";
import { type Facette } from "../../../sdk";
import { useSessionStore } from "../../../states/session";
import Assignment from "./Assignment.vue";
import BehaviourButton from "./AssignmentButton.vue";
import LanguageTranslation from "../../LanguageTranslation.vue";

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
const weight = useState(
  props.facette.id.toString() + "_weight",
  () => selected.value ? store.facetteSelections.filter((l) => l.facette == props.facette.id)[0].weight : 0
)
const isExpanded = useState(
  props.facette.id.toString() + "_expanded",
  () => false
);
const toggleExpand = async () =>  {
  isExpanded.value = !isExpanded.value
  if (isExpanded.value) {
    await store.getAssignmentFeedback() 
  }
};

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
<style scoped lang="scss">
@import "../../../style/variables.scss";
@import "../../../style/a11y.scss";
.less-weight-icon {
  color: $weightLessColor;
}
.more-weight-icon {
  color: $weightMoreColor;
}
</style>