<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
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