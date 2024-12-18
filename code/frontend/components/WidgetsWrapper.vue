<template>
  <div>
    <div
      v-for="(widget, index) in store.currentPage?.widgetList.filter((w ) => w.row == props.row)"
      :key="index"
      :class="'col-' + widget.width"
    >
      {{ widget }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Widget } from "~/sdk";
import { useSessionStore } from "~/states/session";

interface WidetWrapperProps {
  row: Number;
}

const props = defineProps<WidetWrapperProps>();
const store = useSessionStore();
const widgets = store.currentPage?.widgetList.filter(
  (w: Widget) => w.row == props.row
);
</script>