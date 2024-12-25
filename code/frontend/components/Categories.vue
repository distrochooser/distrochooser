<template>
  <div> 
    <Category  v-for="(category, index) in categories"   v-bind:key="index" :category="category" />
  </div>
</template>
  <script lang="ts" setup>
import { useSessionStore } from "~/states/session";

let sessionStore = useSessionStore();

const categories = computed(() => sessionStore.categories);
</script>