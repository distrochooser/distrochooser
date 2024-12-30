<template>
  <li class="list-group-item d-flex justify-content-between align-items-start">
    <div class="ms-2 me-auto">
      <div class="fw-bold">{{ assignment.catalogueId }}</div>
      <span
        :key="index"
        v-for="(value, index) in assignment.choosables"
        class="badge me-1"
        :style="
          'background-color: ' +
          store.choosables.filter((c) => c.id == value)[0].bgColor + '; ' + 
          'color: ' +
          store.choosables.filter((c) => c.id == value)[0].fgColor
        "
        :title=" store.choosables.filter((c) => c.id == value)[0].description"
      >
        {{ store.choosables.filter((c) => c.id == value)[0].displayName }}
      </span>
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