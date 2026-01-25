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