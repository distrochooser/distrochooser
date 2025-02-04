<template>
  <span v-if="!sessionStore.isTranslating">{{ value }}</span>
  <span v-else>
    <input class="form-control" list="datalistOptions" v-on:change="provideFeedback" v-model="valueModel">
    <datalist id="datalistOptions">
      <option :value="value" v-for="(key, value) in suggestions" :key="key"/>
    </datalist>

  </span>
</template>
<script lang="ts" setup>
import { computed, ref, watch } from 'vue';
import { useSessionStore } from '../states/session';

interface TranslationProps {
  translationKey: string;
}

const sessionStore = useSessionStore();
const props = defineProps<TranslationProps>();
const value = sessionStore.__i(props.translationKey)
const valueModel = ref(value);
const suggestions = computed(() => sessionStore.languageFeedback.filter(f => f.languageKey == props.translationKey));

const provideFeedback = async () => {
  await sessionStore.provideTranslation(props.translationKey,  valueModel.value);
}
</script>