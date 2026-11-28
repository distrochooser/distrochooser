<template>
    <span class="badge pill text-bg-warning ms-1" v-if="clickRank.rank == 1">
        <Icon name="ion:flame" class="align-middle me-1" />
        <span class="align-middle">
            <LanguageTranslation translation-key="most_clicks_this_month" />
        </span>
    </span>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import type { RankedChoosable } from '../sdk';

interface WidgetProps {
    choosable: RankedChoosable;
    all: RankedChoosable[]
}

interface ClickRank {
    rank: number;
    clicks: number;
}
const props = defineProps<WidgetProps>();

const clickRank = computed((): ClickRank => {
    const sortedClicks = props.all.sort((a, b) => b.clicksThisMonth - a.clicksThisMonth)

    return {
        rank: sortedClicks.indexOf(props.choosable) + 1,
        clicks: props.choosable.clicksThisMonth
    }
})
</script>