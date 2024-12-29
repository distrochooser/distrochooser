<template>
   <ul class="nav nav-pills row">
    <Category  v-for="(category, index) in categories"   v-bind:key="index" :category="category" />
   </ul>
</template>
  <script lang="ts" setup>
import { useSessionStore } from "~/states/session";

let sessionStore = useSessionStore();

const categories = computed(() => sessionStore.categories);
</script>