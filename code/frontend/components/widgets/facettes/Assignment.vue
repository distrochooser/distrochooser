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

          <span class="badge text-bg-info"
            v-if="props.choosable && store.assignmentFeedback.filter(l => l.assignment == assignment.id && props.choosable && props.choosable.id == l.choosable).length > 0">Feedback
            received</span>

          <AssignmentType :assignment="assignment" :display-weigth="props.displayWeigth" />
        </div>
      </div>
    </div>


    <div v-if="queryChoosables" class="row">
      <div class="col-4" :key="index" v-for="(value, index) in assignment.choosables">
        <ChoosableAssignments :facette="props.facette" :choosable-id="value" :assignment="props.assignment" />
      </div>
    </div>
    <LanguageTranslation translation-key="add-new-choosables" />
    <NewAssignmentChoosable :assignment="assignment" :facette="props.facette"/>
  </li>
</template>
<script setup lang="ts">
import {
  type Choosable,
  type Facette,
  type FacetteAssignment
} from "../../../sdk";
import { useSessionStore } from "../../../states/session";
import AssignmentType from "./AssignmentType.vue";
import ChoosableAssignments from "./ChoosableAssignments.vue";
import NewAssignmentChoosable from "./NewAssignmentChoosable.vue";

interface AsssignmentProps {
  assignment: FacetteAssignment;
  queryChoosables: Boolean;
  facette: Facette;
  choosable?: Choosable;
  displayWeigth: boolean;
}

const store = useSessionStore();

const props = defineProps<AsssignmentProps>();
</script>