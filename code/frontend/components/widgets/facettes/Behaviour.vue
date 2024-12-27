<template>
  <div>{{ behaviours }}</div>
</template>
<script setup lang="ts">
import type { Facette } from "~/sdk";
import { useSessionStore } from "../../../states/session";

interface BehaviourProps {
  facette: Facette;
}

const props = defineProps<BehaviourProps>();
const store = useSessionStore();
const behaviours = computed((b) =>
  store.facetteBehaviours.filter(
    (fb) =>
      fb.affectedObjects.filter((ao) => ao == props.facette.id).length > 0 ||
      fb.affectedSubjects.filter((ao) => ao == props.facette.id).length > 0
  )
);
</script>