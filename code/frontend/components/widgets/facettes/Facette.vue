<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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
  <div v-if="props.facette.imagePath" class="d-inline align-middle text-center mb-3" :class="{
    'col-4': !imageFacetteLarge, 'col-12':
      imageFacetteLarge
  }">
    <div :class="{ 'border border-primary  border-3': isSelected, 'p-3': true }">
      <img :title="'Credit: ' + props.facette.imageCredit" :src="props.facette.imagePath" class="w-100 mt-3"
        @click="registerImageClick" />
      <div class="image-facette-label mt-2">
        <a href="#" @click.prevent="imageFacetteLarge = !imageFacetteLarge" class="btn btn-primary btn-sm">
          <Icon :name="imageFacetteLarge ? 'ion:arrow-shrink' : 'ion:arrow-expand'" class="align-middle me-1" />
          <LanguageTranslation :translation-key="imageFacetteLarge ? 'image-make-smaller' : 'image-make-larger'" />
        </a>
        <div class="mt-2 text-start">
          <FacetteLabel :facette="facette" :on-click="registerImageClick" />
        </div>
      </div>
    </div>
  </div>
  <div class="mt-2" v-else>
    <div :class="{ 'form-check mb-2': true }">
      <input v-if="props.checkbox" class="form-check-input" v-model="selected" v-on:change="registerChange"
        :checked="isSelected" type="checkbox" :id="facette.id.toString()" v-show="!store.isTranslating">
      <input v-else v-on:click="registerClick" v-show="!store.isTranslating" class="form-check-input" type="radio"
        v-bind:name="props.facette.topic" v-model="selected" v-on:change="registerChange" v-bind:value="true"
        :checked="isSelected" :id="facette.id.toString()">
      <FacetteLabel :facette="facette" />
    </div>
  </div>

  <div v-if="isExpanded.valueOf()">
    <ul class="list-group">
      <li v-if="props.facette.assignments.length == 0"
        class="list-group-item d-flex justify-content-between align-items-start">
        <LanguageTranslation translation-key="no-mappings-for-this-facette" />
      </li>
      <Assignment :display-weigth="false" :assignment="key" v-for="(key, index) in props.facette.assignments"
        :key="index" :query-choosables="true" :facette="props.facette" />
    </ul>
  </div>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import { computed, ref } from "vue";
import { type Facette, type FacetteBehaviour } from "../../../sdk";
import { useSessionStore } from "../../../states/session";
import Assignment from "./Assignment.vue";
import LanguageTranslation from "../../LanguageTranslation.vue";
import FacetteLabel from "./FacetteLabel.vue";

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
const isNegativeHandlingActive = useState(
  props.facette.id.toString() + "_is_negative_handling_active",
  () => selected.value ? store.facetteSelections.filter((l) => l.facette == props.facette.id)[0].negativeHandlingActive : false
)
const isExpanded = useState(
  props.facette.id.toString() + "_expanded",
  () => false
);

const isSelected = computed(
  () =>
    store.facetteSelections.filter((l) => l.facette == props.facette.id)
      .length != 0
);

const registerImageClick = async () => {
  await store.updateFacetteSelections(
    store.currentPage.id,
    props.facette.id,
    0,
    false,
    store.facetteSelections.filter(s => s.facette === props.facette.id).length === 0,
    props.checkbox ? "" : "all"
  )
}

const imageFacetteLarge = ref(false)

const registerClick = async () => {
  if (isSelected.value) {
    await store.updateFacetteSelections(
      store.currentPage.id,
      props.facette.id,
      0,
      false,
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
    isNegativeHandlingActive.value,
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
</script>
<style scoped lang="scss">
@import "../../../style/variables.scss";

.less-weight-icon {
  color: $less-weight-color;
}

.more-weight-icon {
  color: $more-weight-color
}

.image-facette-label {
  font-size: smaller;
}
</style>