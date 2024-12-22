

<template>
  <div>
    <div v-if="sessionStore.categories.length != 0">
        <span v-for="(category, index) in sessionStore.categories" v-bind:key="index">
           <Category :category="category"/>
        </span>
    </div>
    <div v-else>
        <Loading/>
    </div>
  </div>
</template>
  <script lang="ts" setup>


import { onMounted } from "vue";
import { useSessionStore } from "~/states/session";

let sessionStore = useSessionStore();
</script>