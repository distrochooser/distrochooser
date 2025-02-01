<template>
    <span>
        {{ props.index + 1 }}. {{ props.category.name }}
        <Icon name="ion:checkmark-circle" v-if="isAnswered"></Icon>
        <Icon name="ion:bookmark" v-if="isMarked"></Icon>
    </span>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import type { Category } from '../sdk';
import { useSessionStore } from '../states/session';


interface WidgetProps {
    category: Category;
    index: number;
}

const props = defineProps<WidgetProps>();

const store = useSessionStore();
const isAnswered = computed(() => {
  return store.facetteSelections.filter(l => l.pagesOfFacettes.indexOf(props.category.targetPage) != -1).length > 0
});
const isMarked = computed(() => {
    return store.pageMarkings.filter(l => l.page == props.category.targetPage).length > 0;
})
</script>