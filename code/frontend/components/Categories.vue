<template>
  <div>
    <div v-if="categories.length != 0">
      <span
        v-for="(category, index) in categories"
        v-bind:key="index"
      >
        <Category :category="category" />
      </span>
    </div>
    <div v-else>
      <Loading />
    </div>
  </div>
</template>
  <script lang="ts" setup>
import { useSessionStore } from "~/states/session";

let sessionStore = useSessionStore();

const categories = computed(() => sessionStore.categories);
</script>