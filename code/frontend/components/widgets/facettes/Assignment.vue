<template>
    <div>{{ assignment }}</div>
  </template>
  <script setup lang="ts">
  import type { FacetteAssignment } from "~/sdk";
  
  interface AsssignmentProps {
    assignment: FacetteAssignment;
  }

const props = defineProps<AsssignmentProps>();
  </script>