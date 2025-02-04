<template>
  <span v-if="!sessionStore.isTranslating">{{ computedValue }}</span>
  <span v-else :title="computedValue" class="w-100 d-block">
    <textarea class="form-control w-100" :style="{'border-color': colorCode(computedValue)}" v-on:click.prevent.stop="() => {}" v-on:change="provideFeedback" >{{  computedValue }}</textarea>
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

// Based upon https://gist.github.com/0x263b/2bdd90886c2036a1ad5bcf06d6e6fb37
const colorCode =  (input: string) => {
    var hash = 0;
    if (input.length === 0) return hash;
    for (var i = 0; i < input.length; i++) {
        hash = input.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash;
    }
    var rgb = [0, 0, 0];
    for (var i = 0; i < 3; i++) {
        var value = (hash >> (i * 8)) & 255;
        rgb[i] = value;
    }
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}


</script>