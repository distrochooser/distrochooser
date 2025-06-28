<template>
    <span :class="{ 'text-body-secondary': !isAnswered, 'text-bold': isCurrent }"
        :title="(props.index + 1).toString() + '. ' + props.page.text">
        <div>
            
            <Icon name="ion:checkmark-circle" v-if="isAnswered"></Icon>
            <Icon name="ion:ellipse-sharp" v-else-if="isCurrent"></Icon>
            <Icon name="ion:ellipse-outline" v-else></Icon>
            <Icon name="ion:bookmark" v-if="isMarked"></Icon>
        </div>
    </span>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import type { Page } from '../sdk';
import { useSessionStore } from '../states/session';


interface WidgetProps {
    page: Page;
    index: number;
}

const props = defineProps<WidgetProps>();
/** TODO: This component is terribly redudnant with Categories */
const store = useSessionStore();
const isAnswered = computed(() => {
    return false //store.facetteSelections.filter(l => l.pagesOfFacettes.indexOf(props.category.targetPage) != -1).length > 0
});
const isMarked = computed(() => {
    return false // store.pageMarkings.filter(l => l.page == props.category.targetPage).length > 0;
})
const isCurrent = computed(() => {
    return false //store.currentPage.id == props.category.targetPage
});
</script>