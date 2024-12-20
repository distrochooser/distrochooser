<template>
  <div>
    <div
      v-for="(widget, index) in store.currentPage?.widgetList.filter((w ) => w.row == props.row)"
      :key="index"
      :class="'col-' + widget.width"
    >
    <NavigationWidget v-if="widget.widgetType == 'NavigationWidget'" :widget="widget"/>
    <FacetteSelectionWidget v-if="widget.widgetType == 'FacetteSelectionWidget'" :widget="widget"/>
    <FacetteRadioSelectionWidget v-if="widget.widgetType == 'FacetteRadioSelectionWidget'" :widget="widget"/>
    <ResultListWidget v-if="widget.widgetType == 'ResultListWidget'" :widget="widget"/>
    <ResultShareWidget v-if="widget.widgetType == 'ResultShareWidget'" :widget="widget"/>
    <HTMLWidget v-if="widget.widgetType == 'HTMLWidget'" :widget="widget"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Component } from "vue";
import type { Widget } from "~/sdk";
import { useSessionStore } from "~/states/session";
import FacetteSelectionWidget from "./widgets/FacetteSelectionWidget.vue";
import NavigationWidget from "./widgets/NavigationWidget.vue";
import FacetteRadioSelectionWidget from "./widgets/FacetteRadioSelectionWidget.vue";
import ResultListWidget from "./widgets/ResultListWidget.vue";
import ResultShareWidget from "./widgets/ResultShareWidget.vue";
import HTMLWidget from "./widgets/HTMLWidget.vue";

interface WidgetWrapperProps {
  row: Number;
}

const props = defineProps<WidgetWrapperProps>();
const store = useSessionStore();
const widgets = store.currentPage?.widgetList.filter(
  (w: Widget) => w.row == props.row
);


</script>