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
  <li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
      <div class="fw-bold">{{ assignment.description }}</div>
      <div v-if="queryChoosables">
        <span
          :key="index"
          v-for="(value, index) in assignment.choosables"
          class="badge me-1"
          :style="
            'background-color: ' +
            store.choosables.filter((c) => c.id == value)[0].bgColor +
            '; ' +
            'color: ' +
            store.choosables.filter((c) => c.id == value)[0].fgColor
          "
          :title="store.choosables.filter((c) => c.id == value)[0].description"
        >
          {{ store.choosables.filter((c) => c.id == value)[0].displayName }}
        </span>
      </div>
    </div>
    <span
      :class="
        'badge  rounded-pill ' + assignmentTypeCssMap[assignment.assignmentType]
      "
      >{{ assignment.assignmentType }}</span
    >
  </li>
</template>
  <script setup lang="ts">
import { AssignmentTypeEnum, type FacetteAssignment } from "~/sdk";
import { useSessionStore } from "../../../states/session";

interface AsssignmentProps {
  assignment: FacetteAssignment;
  queryChoosables: Boolean;
}

const assignmentTypeCssMap = {
  BLOCKING: "text-bg-dark",
  NEGATIVE: "text-bg-danger",
  POSITIVE: "text-bg-success",
  NEUTRAL: "text-bg-light",
};
const store = useSessionStore();

const props = defineProps<AsssignmentProps>();
</script>