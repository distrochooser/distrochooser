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
  <li class="list-group-item">
    <div class="row">
      <div class="col row">
        <div class="col">

          <LanguageTranslation :translation-key="assignment.description" />
        </div>
        <div class="col text-end">
          <AssignmentType :assignment="assignment" :display-weigth="props.displayWeigth" />
        </div>
      </div>
    </div>


    <div v-if="queryChoosables" class="row">
      <div class="col-4" :key="index" v-for="(value, index) in allChoosables">
        <ChoosableAssignments :is-pending="newChoosables.filter(c => c.id == value).length > 0" :facette="props.facette" :choosable-id="value" :assignment="props.assignment"
          :remove-delegate="getRemovalFunc(value)" />
      </div>
    </div>
    <LanguageTranslation translation-key="add-new-choosables" />
    <NewAssignmentChoosable :removal-func="removalFunc" :new-choosables="newChoosables" :assignment="assignment"
      :facette="props.facette" />
  </li>
</template>
<script setup lang="ts">
import { useState } from "nuxt/app";
import {
  type Choosable,
  type Facette,
  type FacetteAssignment
} from "../../../sdk";
import { useSessionStore } from "../../../states/session";
import AssignmentType from "./AssignmentType.vue";
import ChoosableAssignments from "./ChoosableAssignments.vue";
import NewAssignmentChoosable from "./NewAssignmentChoosable.vue";
import { computed, ref } from "vue";

interface AsssignmentProps {
  assignment: FacetteAssignment;
  queryChoosables: Boolean;
  facette: Facette;
  choosable?: Choosable;
  displayWeigth: boolean;
}

const store = useSessionStore();

const props = defineProps<AsssignmentProps>();

const otherUserVotes = computed(() => {
  const ids = props.assignment.votes.map(v => v[0])
  const allChoosables = store.choosables;
  const choosablesOutsideAssignment = allChoosables.filter(c => props.assignment.choosables.indexOf(c.id) == -1)
  const choosablesOutsideAssignmentWithVotes = choosablesOutsideAssignment.filter(c => ids.indexOf(c.id) != -1)
  return choosablesOutsideAssignmentWithVotes
})
console.log(otherUserVotes.value)
// TODO: Decide if these feedback must be persisted to be resumed after a share
const newChoosables = ref<Choosable[]>(otherUserVotes.value);
const removalFunc = (c: Choosable) => {
  newChoosables.value = newChoosables.value.filter(l => l.id != c.id)
}

const allChoosables = computed(() => props.assignment.choosables.concat(newChoosables.value.map(c => c.id)))
const getRemovalFunc = ((id: number) => props.assignment.votes.filter(v => v[0] == id).length == 0 && newChoosables.value.filter(c => c.id == id).length > 0 ? removalFunc : null)
</script>