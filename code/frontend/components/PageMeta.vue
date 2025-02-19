<template>
    <div v-if="store.session">
        <Title>
            {{ store.session.name }}
        </Title>
        <link rel="icon" type="image/x-icon" :href="store.session.icon" v-if="store.session.icon" />
    </div>
</template>
<script setup lang="ts">
import { useRoute } from "vue-router";
import { useSessionStore } from "../states/session";

const router = useRoute();
const store = useSessionStore();
const { data } = await useAsyncData("post", async () => {
  return await $fetch(useRuntimeConfig().public.basePath + "/rest/metatags?lang=" + router.params.lang);
});
const metatags = data.value.meta
metatags["title"] = data.value.name
useSeoMeta(metatags)

</script>