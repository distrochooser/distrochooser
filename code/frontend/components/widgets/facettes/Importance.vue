<template>
    <span>
        <Icon :title="showedTooltip" class="fs-5 align-middle ms-1 me-1 weight-ribbon"
            :class="{ 'marked-important': isImportant }" :name="showedIcon" v-on:click="registerWeightChange"></Icon>
    </span>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { Facette } from '../../../sdk/models/Facette';
import { useSessionStore } from '../../../states/session';


interface ImportanceProps {
    facette: Facette;
    selected: boolean
}

const props = defineProps<ImportanceProps>();
const store = useSessionStore();

const isImportant = computed(() => {
    const matches = store.facetteSelections.filter(s => s.facette == props.facette.id)

    if (matches.length == 0) {
        return false;
    }
    return matches[0].weight > 0
});
const showedIcon = computed(() => isImportant.value ? 'ion:ribbon' : 'ion:ribbon-outline');
const showedTooltip = computed(() => isImportant.value ? store.__i("weight_more") : store.__i("weight_info"))

const registerWeightChange = async () => {
    await store.updateFacetteSelections(
        store.currentPage.id,
        props.facette.id,
        isImportant.value ? 0 : 2,
        props.selected,
        "this"
    );
};
</script>
<style lang="scss" scoped>
@import "../../../style/variables.scss";

.weight-ribbon {
    cursor: pointer;

    &.marked-important {
        animation: tilt-shaking 0.2s linear;
        color: $weightMoreColor;
    }
}
</style>