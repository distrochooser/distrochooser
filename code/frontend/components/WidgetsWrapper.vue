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
  <div>
    <div
      v-for="(widget, index) in store.currentWidgets.filter((w ) => w.row == props.row)"
      :key="index"
      :class="'col col-' + widget.width"
    >
    <NavigationWidget v-if="widget.widgetType == 'NavigationWidget'" :widget="widget"/>
    <FacetteSelectionWidget v-if="widget.widgetType == 'FacetteSelectionWidget'" :checkbox="true" :widget="widget"/>
    <FacetteSelectionWidget v-if="widget.widgetType == 'FacetteRadioSelectionWidget'" :checkbox="false" :widget="widget"/>
    <ResultListWidget v-if="widget.widgetType == 'ResultListWidget'" :widget="widget"/>
    <ResultShareWidget v-if="widget.widgetType == 'ResultShareWidget'" :widget="widget"/>
    <HTMLWidget v-if="widget.widgetType == 'HTMLWidget'" :widget="widget"/>
    <SessionVersionWidget v-if="widget.widgetType == 'SessionVersionWidget'" :widget="widget"/>
    <MetaFilterWidget v-if="widget.widgetType == 'MetaFilterWidget'" :widget="widget"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSessionStore } from "../states/session";
import FacetteSelectionWidget from "./widgets/FacetteSelectionWidget.vue";
import NavigationWidget from "./widgets/NavigationWidget.vue";
import ResultListWidget from "./widgets/ResultListWidget.vue";
import ResultShareWidget from "./widgets/ResultShareWidget.vue";
import HTMLWidget from "./widgets/HTMLWidget.vue";
import SessionVersionWidget from "./widgets/SessionVersionWidget.vue";
import MetaFilterWidget from "./widgets/MetaFilterWidget.vue";

interface WidgetWrapperProps {
  row: Number;
}

const props = defineProps<WidgetWrapperProps>();
const store = useSessionStore();

</script>