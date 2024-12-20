<template>
  <div>
    <div v-if="store.currentPage">
      {{  store.currentPage.text }}
      {{  store.currentPage.help }}
      <div v-for="row in 12" :key="row" class="grid gap-4">
        <WidgetsWrapper
          :row="row"
        />
      </div>
    </div>
    <div v-else>
      <Loading />
    </div>
  </div>
</template>
<script setup lang="ts">
import type { Widget } from "~/sdk";
import { useSessionStore } from "~/states/session";

const store = useSessionStore();
</script>