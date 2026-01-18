<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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

          <AssignmentType :assignment="assignment" :display-weigth="props.displayWeigth" />
          <h4>
            <LanguageTranslation :translation-key="assignment.description" />
          </h4>
        </div>
        <div class="col text-end"  v-if="queryChoosables">
          <div class="row">
            <div class="col">
              <div class="btn-group mt-3" role="group">
                <a href="#" :class='{
                  "btn btn-outline-success": true,
                  "btn-success link-light": hasPositiveVote
                }' v-on:click.prevent="async () => await store.createAssignmentFeedback(assignment.id, true)
                  ">
                  <Icon name="ion:thumbs-up"></Icon>
                  <span>({{ votes[0] }})</span>
                </a>

                <a href="#" :class='{
                  "btn btn-outline-danger": true,
                  "btn-danger link-light": hasNegativeVote
                }' v-on:click.prevent="async () => await store.createAssignmentFeedback(assignment.id, false)
                  ">
                  <Icon name="ion:thumbs-down"></Icon>
                  <span>({{ votes[1] }})</span>
                </a>

                <a href="#" v-if="hasNegativeVote || hasPositiveVote" class="btn btn-outline-primary" v-on:click.prevent="
                  store.deleteAssignmentFeedback(assignment.id)
                  ">
                  <Icon name="ion:arrow-undo"></Icon>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div v-if="queryChoosables" class="row">
      <div class="col-4" :key="index" v-for="(value, index) in allChoosables">
        <ChoosableAssignments :is-pending="newChoosables.filter(c => c.id == value).length > 0" :facette="props.facette"
          :choosable-id="value" :assignment="props.assignment" :remove-delegate="getRemovalFunc(value)" />
      </div>
    </div>
    <div v-if="queryChoosables" class="row pt-2  mt-3 border-top">

      <LanguageTranslation translation-key="add-new-choosables" />
      <NewAssignmentChoosable class="mt-2 mb-2" :removal-func="removalFunc" :new-choosables="newChoosables"
        :assignment="assignment" :facette="props.facette" />
    </div>
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
// TODO: Decide if these feedback must be persisted to be resumed after a share
const newChoosables = ref<Choosable[]>(otherUserVotes.value);
const removalFunc = (c: Choosable) => {
  newChoosables.value = newChoosables.value.filter(l => l.id != c.id)
}

const allChoosables = computed(() => props.assignment.choosables.concat(newChoosables.value.map(c => c.id)))
const getRemovalFunc = ((id: number) => props.assignment.votes.filter(v => v[0] == id).length == 0 && newChoosables.value.filter(c => c.id == id).length > 0 ? removalFunc : null)


// FIXME: The votes are not properly displayed
const hasPositiveVote = computed(() => store.assignmentFeedback.filter(a => a.assignment == props.assignment.id && a.session == store.session.id && a.isPositive).length > 0)
const hasNegativeVote = computed(() => store.assignmentFeedback.filter(a => a.assignment == props.assignment.id && a.session == store.session.id && !a.isPositive).length > 0)

const votes = computed(() => {
  const matchingvotes = store.assignmentFeedback.filter(a => a.assignment == props.assignment.id)

  return [
    matchingvotes.filter(v => v.isPositive).length,
    matchingvotes.filter(v => !v.isPositive).length
  ]
})
</script>