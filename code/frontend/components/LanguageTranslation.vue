<template>
  <span v-if="!sessionStore.isTranslating">{{ computedValue }}</span>
  <span class="w-100" v-else>
    <input class="form-control w-100" v-on:change="provideFeedback" :value="computedValue">
  </span>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { useSessionStore } from '../states/session';

interface TranslationProps {
  translationKey: string;
}

const sessionStore = useSessionStore();
const props = defineProps<TranslationProps>();
const computedValue = computed(() => sessionStore.__i(props.translationKey))

const provideFeedback = async (e: Event) => {
  const newValue = (e.target as HTMLInputElement).value;
  await sessionStore.provideTranslation(props.translationKey,  newValue);
}

</script>