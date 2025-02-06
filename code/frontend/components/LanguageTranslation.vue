<template>
  <span :id="props.translationKey">
    {{ computedValue }}
    <a href="#" v-on:click.prevent.stop="toggleEditing" v-if="!isEditing">
      <Icon name="ion:edit" v-if="sessionStore.isTranslating"></Icon>
    </a>
  </span>
  <span v-if="isEditing" class="d-inline-block" :title="computedValue" :style="{'width': width.toString() + 'px', 'height': height.toString() + 'px'}">
    <textarea class="col form-control d-inline-block" :style="{'width': 90 + '%', 'border-color': colorCode(computedValue)}" v-on:click.prevent.stop="() => {}" v-on:change="provideFeedback" >{{  computedValue }}</textarea>
  
    <a href="#" class="d-inline-block " v-on:click.prevent.stop="toggleEditing">
      <Icon name="ion:save-outline"></Icon>
    </a>
  </span>
</template>
<script lang="ts" setup>
import { computed, ref } from 'vue';
import { useSessionStore } from '../states/session';
import { useState } from 'nuxt/app';

interface TranslationProps {
  translationKey: string;
}

const sessionStore = useSessionStore();
const props = defineProps<TranslationProps>();
const computedValue = computed(() => sessionStore.__i(props.translationKey))
const isEditing = ref(false);
const provideFeedback = async (e: Event) => {
  const newValue = (e.target as HTMLInputElement).value;
  await sessionStore.provideTranslation(props.translationKey,  newValue);
}

const width = ref(0)
const height = ref(0)

const toggleEditing = () => {
  // get dimensions
  const element = document.querySelector("#" + props.translationKey)
  const rect= element.getBoundingClientRect()
  width.value = rect.width
  height.value = rect.height
  isEditing.value = !isEditing.value
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