<template>
  <div class="row">
    <div class="col">
      <a v-if="canGoBack" href="#" v-on:click="goBack">{{
        store.__i("BTN_PREV_PAGE")
      }}</a>
    </div>
    <div class="col">
      <a v-if="canGoNext" href="#" v-on:click="goNext">
        {{ store.__i("BTN_SKIP_PAGE") }}
      </a>
    </div>
    <div class="col">
      <a v-if="canGoNext" href="#" v-on:click="goNext">
        {{ store.__i("BTN_NEXT_PAGE") }}
      </a>
    </div>
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
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) - 1]
      .id
  );
const goNext = () =>
  store.selectPage(
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) + 1]
      .id
  );
</script>