<template>
    <li class="list-group-item" v-if="store.session && browserLanguageOffered">
        <Icon class="text-muted me-1" name="ion:language"></Icon>
        <LanguageTranslation translation-key="TEST_IN_OWN_LANGUAGE" />
    </li>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useSessionStore } from '../states/session';

const store = useSessionStore();
const selectedLanguage = computed(() => store.session ? store.session.languageCode : "eng")
const allLanguages = computed(() => store.session ? Object.keys(store.session.languageCodes) : [])
const browserLanguage = computed(() => import.meta.client ? navigator.language : "eng")
const browserLanguageOffered = computed(() => allLanguages.value.indexOf(browserLanguage.value) !== -1 && browserLanguage.value !== selectedLanguage.value && browserLanguage.value !== "eng")
</script>