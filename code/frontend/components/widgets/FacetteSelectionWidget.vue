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
  <div>
    <div v-for="(facette, index) in facettes" v-bind:key="index">
      <Facette :facette="facette" :checkbox="props.checkbox" :topic="props.widget.topic" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { type FacetteSelectionWidget } from "../../sdk";
import { useSessionStore } from "../../states/session";
import Facette from "./facettes/Facette.vue";

interface WidgetProps {
  widget: FacetteSelectionWidget;
  checkbox: boolean;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();

/** Facettes will be filtered client sided, see ADR 0029 for details */

const facettes = computed(() => {
  const version = store.session.version
  if (version) {
    const versionId = version;
    return props.widget.facettes.filter(f => !f.notInVersions || f.notInVersions.indexOf(versionId) === -1)
  } else {
    return props.widget.facettes
  }
})


</script>