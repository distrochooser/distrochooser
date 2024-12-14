<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div>
</template>
<script lang="ts" setup>

import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useSessionStore } from '~/states/session';

const router = useRoute();
const lang: string = (router.params.lang as string) ?? "en"
const id: string | null = (router.params.id as string) ?? null;



onMounted(async () => {
  const sessionStore = useSessionStore();
  await sessionStore.createSession(lang, id);
  const got = sessionStore.session;
  console.log(got)
});
</script>