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
  <li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
      <div class="fw-bold">
        <LanguageTranslation :translation-key="assignment.description"/>
        <span class="badge text-bg-info"
          v-if="props.choosable && store.assignmentFeedback.filter(l => l.assignment == assignment.id && props.choosable && props.choosable.id == l.choosable).length > 0">Feedback
          received</span>
      </div>
      <div v-if="queryChoosables">
        <span :key="index" v-for="(value, index) in assignment.choosables" class="badge me-1" :style="'background-color: ' +
          store.choosables.filter((c) => c.id == value)[0].bgColor +
          '; ' +
          'color: ' +
          store.choosables.filter((c) => c.id == value)[0].fgColor
          " :title="store.choosables.filter((c) => c.id == value)[0].description">
          {{ store.choosables.filter((c) => c.id == value)[0].displayName }} {{ hasFeedback(value) }}
          <a href="#" v-on:click="
            giveFeedback(store.choosables.filter((c) => c.id == value)[0], true)
            ">+1</a>

          <a href="#" v-on:click="
            giveFeedback(store.choosables.filter((c) => c.id == value)[0], false)
            ">-1</a>
          <a href="#" v-on:click="
            removeFeedback(store.choosables.filter((c) => c.id == value)[0])
            ">DEL</a>
        </span>
      </div>
    </div>
    <span
      :class="{ 'badge  rounded-pill me-3 ': true, 'text-bg-light': assignment.weight < 0, 'text-bg-dark': assignment.weight > 0 }"
      v-if="props.displayWeigth && props.assignment.weight != null" :title="assignment.weight.toString() + 'x'">
      
      <Icon name="ion:chevron-up-sharp" v-if="props.assignment.weight > 0"></Icon>
      <Icon name="ion:chevron-down-sharp" v-if="props.assignment.weight < 0"></Icon>
      
      <LanguageTranslation :translation-key="weightText"/>
      </span>
    <span :class="'badge  rounded-pill ' + assignmentTypeCssMap[assignment.assignmentType]
      ">
       <LanguageTranslation :translation-key="assignment.assignmentType"/>
          
  </span>
  </li>
</template>
<script setup lang="ts">
import {
  type Choosable,
  type Facette,
  type FacetteAssignment,
} from "../../../sdk";
import { useSessionStore } from "../../../states/session";

interface AsssignmentProps {
  assignment: FacetteAssignment;
  queryChoosables: Boolean;
  facette: Facette;
  choosable?: Choosable;
  displayWeigth: boolean;
}

const assignmentTypeCssMap = {
  BLOCKING: "text-bg-dark",
  NEGATIVE: "text-bg-danger",
  POSITIVE: "text-bg-success",
  NEUTRAL: "text-bg-light",
};


const store = useSessionStore();

const props = defineProps<AsssignmentProps>();
const weightText = props.assignment.weight < 0 ? "weight-less" : "weight_more";

const giveFeedback = (choosable: Choosable, is_positive: boolean) =>
  store.giveFeedback(props.assignment, choosable, props.facette, is_positive);

const removeFeedback = (choosable: Choosable) =>
  store.removeFeedback(props.assignment, choosable);

const hasFeedback = (choosableId: number) => store.assignmentFeedback.filter(f => f.assignment == props.assignment.id && f.choosable == choosableId).length != 0;
</script>