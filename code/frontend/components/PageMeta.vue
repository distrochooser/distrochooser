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
import { computed, watch } from "vue";

const router = useRoute();
const store = useSessionStore();
// TODO: Replace with proper TS mapping
const { data } = await useAsyncData("post", async () => {
  return await $fetch(useRuntimeConfig().public.basePath + "/rest/metatags?lang=" + router.params.lang);
});
const metatags = data.value.meta
metatags["title"] = data.value.name
useSeoMeta(metatags)

const isTranslating = computed(() => store.session && store.isTranslating)

watch(isTranslating, value => {
    if (import.meta.client) {
        const haystack = document.getElementsByTagName("body")
        if (haystack.length > 0) {
            if (store.isTranslating) {
                haystack[0].classList.add("is-translating")
            } else {
                haystack[0].classList.remove("is-translating")
            }
        }
    }
}, { deep: true, immediate: true })


</script>
<style lang="scss">
@import "../style/global.scss"
</style>