<template>
    <span v-if="!sessionStore.isTranslating">{{ value }}</span>
    <span v-else>{{ props.translationKey}} {{ value }}</span>
</template>
<script lang="ts" setup>
import { useSessionStore } from '../states/session';

interface TranslationProps {
  translationKey: string;
}

const sessionStore = useSessionStore();
const props = defineProps<TranslationProps>();
const value = sessionStore.__i(props.translationKey)
</script>