<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template>
<script lang="ts" setup>

import { onMounted } from 'vue';
import { ChoosableApi, Configuration, SessionApi } from './sdk';

onMounted(async () => {
      const api = new ChoosableApi(new Configuration({
        basePath: 'http://localhost:8000',
        headers: {
          "accept": "application/json"
        }
      }))
      const todo = await api.choosableList({
        lang: "de"
      })
      console.log(todo)
});
</script>