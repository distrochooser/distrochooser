<template>
  <div>
    <div
      v-for="(widget, index) in store.currentWidgets.filter((w ) => w.row == props.row)"
      :key="index"
      :class="'col-' + widget.width"
    >
    {{  widget  }}
    <NavigationWidget v-if="widget.widgetType == 'NavigationWidget'" :widget="widget"/>
    <FacetteSelectionWidget v-if="widget.widgetType == 'FacetteSelectionWidget'" :checkbox="true" :widget="widget"/>
    <FacetteSelectionWidget v-if="widget.widgetType == 'FacetteRadioSelectionWidget'" :checkbox="false" :widget="widget"/>
    <ResultListWidget v-if="widget.widgetType == 'ResultListWidget'" :widget="widget"/>
    <ResultShareWidget v-if="widget.widgetType == 'ResultShareWidget'" :widget="widget"/>
    <HTMLWidget v-if="widget.widgetType == 'HTMLWidget'" :widget="widget"/>
    <SessionVersionWidget v-if="widget.widgetType == 'SessionVersionWidget'" :widget="widget"/>
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
import SessionVersionWidget from "./widgets/SessionVersionWidget.vue";

interface WidgetWrapperProps {
  row: Number;
}

const props = defineProps<WidgetWrapperProps>();
const store = useSessionStore();

</script>