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
  <div v-if="behaviours.length > 0">
    <div class="alert alert-info">
      {{  behaviours }}
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import type { Facette } from "../../../sdk";
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