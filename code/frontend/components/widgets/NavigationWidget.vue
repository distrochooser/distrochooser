<template>
  <div>
    <a v-if="canGoBack" href="#" v-on:click="goBack"> Back </a>
    <a v-if="canGoNext" href="#" v-on:click="goNext"> Skip </a>
    <a v-if="canGoNext" href="#" v-on:click="goNext"> Forward </a>
  </div>
</template>
<script setup lang="ts">
import type { NavigationWidget } from "~/sdk";
import { useSessionStore } from "../../states/session";

interface WidgetProps {
  widget: NavigationWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();
const canGoNext = computed(() => {
  return store.currentPage.nextPage != null;
});
const canGoBack = computed(() => {
  const index = store.pages.findIndex((p) => p.id == store.currentPage.id);
  return index > 0;
});
const goBack = () =>
  store.selectPage(
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) - 1].id
  );
const goNext = () =>
  store.selectPage(
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) +1].id
  );
</script>