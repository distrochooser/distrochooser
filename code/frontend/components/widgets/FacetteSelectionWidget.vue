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
  <div>
    <Behaviour v-for="(facette, index) in props.widget.facettes" v-bind:key="index"  :facette="facette"/>
    <div v-for="(facette, index) in props.widget.facettes" v-bind:key="index">
      <Facette :facette="facette" :checkbox="props.checkbox"/>
    </div>
  </div>
</template>
<script setup lang="ts">
import { type FacetteSelectionWidget } from "../../sdk";
import Facette from "./facettes/Facette.vue";
import Behaviour from "./facettes/Behaviour.vue";

interface WidgetProps {
  widget: FacetteSelectionWidget;
  checkbox: boolean;
}

const props = defineProps<WidgetProps>();
</script>