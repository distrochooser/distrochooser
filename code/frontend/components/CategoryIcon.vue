<template>
    <span :class="{ 'text-body-secondary': !isAnswered, 'text-bold': isCurrent }"
        :title="(props.index + 1).toString() + '. ' + props.category.name">
        <div v-on:mouseover="toggleTextDisplay">
            
            <Icon name="ion:checkmark-circle" v-if="isAnswered"></Icon>
            <Icon name="ion:ellipse-sharp" v-else-if="isCurrent"></Icon>
            <Icon name="ion:ellipse-outline" v-else></Icon>
            <Icon name="ion:bookmark" v-if="isMarked"></Icon>
        </div>
    </span>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import type { Category } from '../sdk';
import { useSessionStore } from '../states/session';


interface WidgetProps {
    category: Category;
    index: number;
}

const props = defineProps<WidgetProps>();
/** TODO: This component is terribly redudnant with Categories */
const store = useSessionStore();
const isAnswered = computed(() => {
    return store.facetteSelections.filter(l => l.pagesOfFacettes.indexOf(props.category.targetPage) != -1).length > 0
});
const isMarked = computed(() => {
    return store.pageMarkings.filter(l => l.page == props.category.targetPage).length > 0;
})
const isCurrent = computed(() => {
    return store.currentPage.id == props.category.targetPage
});
</script>