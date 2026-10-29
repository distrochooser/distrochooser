<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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
    <span class="mb-1 fs-6">
        <span>
            <Icon :title="showedTooltip" class="align-middle weight-ribbon" :class="{ 'marked-important': isImportant }"
                :name="showedIcon" v-on:click="() => {
                    isImportant = !isImportant;
                    registerWeightChange()
                }">
            </Icon>
        </span>
        <span>
            <span class="ms-1" v-on:click="() => {
                hasNegativeHandlingActive = !hasNegativeHandlingActive;
                registerWeightChange()
            }">
                <Icon :title="showedTooltipNegativeHandling" class="align-middle negative-handling"
                    :class="{ 'negative-handling-active': hasNegativeHandlingActive }"
                    :name="showedIconNegativeHandling" />
                <b class="align-middle ms-1" v-if="hasNegativeHandlingActive">{{ showedTooltipNegativeHandling
                }}</b>
            </span>
        </span>
    </span>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import type { Facette } from '../../../sdk/models/Facette';
import { useSessionStore } from '../../../states/session';


interface ImportanceProps {
    facette: Facette;
    selected: boolean
}

const props = defineProps<ImportanceProps>();
const store = useSessionStore();

const isImportant = ref(false)
const hasNegativeHandlingActive = ref(false)

onMounted(() => {
    const matches = store.facetteSelections.find(s => s.facette == props.facette.id)

    hasNegativeHandlingActive.value = matches !== undefined ? matches.negativeHandlingActive : false
    isImportant.value = matches !== undefined ? matches.weight > 0 : false
})

const showedIcon = computed(() => isImportant.value ? 'ion:ribbon' : 'ion:ribbon-outline');
const showedTooltip = computed(() => hasNegativeHandlingActive.value ? store.__i("marked_weight") : store.__i("mark_weight"))


// See ADR-0035
const showedIconNegativeHandling = computed(() => hasNegativeHandlingActive.value ? 'ion:stop-circle' : 'ion:stop-circle-outline');
const showedTooltipNegativeHandling = computed(() => hasNegativeHandlingActive.value ? store.__i("negative_handling_active") : store.__i("negative_handling"))


const registerWeightChange = async () => {
    await store.updateFacetteSelections(
        store.currentPage.id,
        props.facette.id,
        isImportant.value ? 2 : 0,
        hasNegativeHandlingActive.value,
        props.selected,
        "this"
    );
};

</script>
<style lang="scss" scoped>
@import "../../../style/variables.scss";

.weight-ribbon,
.negative-handling {
    cursor: pointer;

    &.marked-important {
        animation: tilt-shaking 0.2s linear;
        color: $more-weight-color;
    }


    &.negative-handling-active {
        animation: tilt-shaking 0.2s linear;
        color: $negative-handling-active-color;
    }
}
</style>