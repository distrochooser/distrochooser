<template>
    <span>
        {{ props.index + 1 }}. 
        <LanguageTranslation :translation-key="props.page.title"/>
        <Icon name="ion:checkmark-circle"  class="ms-1" v-if="isAnswered"></Icon>
        <Icon name="ion:bookmark" :class="{'ms-1 marked': isMarked}" v-if="isMarked"></Icon>
    </span>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import type {  Page } from '../sdk';
import { useSessionStore } from '../states/session';
import LanguageTranslation from './LanguageTranslation.vue';


interface WidgetProps {
    page: Page;
    index: number;
}

const props = defineProps<WidgetProps>();

const store = useSessionStore();
const isAnswered = computed(() => {
  return  store.facetteSelections.filter(l => l.pagesOfFacettes.indexOf(props.page.id) != -1).length > 0 || store.metaValues.filter(m => m.page == props.page.id).length > 0
});
const isMarked = computed(() => {
    return store.pageMarkings.filter(l => l.page == props.page.id).length > 0;
})
</script>
<style lang="scss" scoped>

@import "../style/variables.scss";
.marked {
    color: $orange;
}
</style>