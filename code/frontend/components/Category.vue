<!--
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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
  <li
    v-if="props.category.targetPage"
    v-on:click="store.selectPage(props.category.targetPage)"
    class="col col-3 nav-item"
  >
    
    <a :class="'nav-link ' + (isCurrent ? 'active' : '')" aria-current="page" href="#">{{ props.category.name }} </a>
</li>
</template>
    <script lang="ts" setup>
import { computed } from "vue";
import type { Category } from "../sdk/models";
import { useSessionStore } from "../states/session";

interface CategoryProps {
  category: Category;
}

const props = defineProps<CategoryProps>();
const store = useSessionStore();
const isAnswered = computed(() => {
  return store.facetteSelections.filter(l => l.pagesOfFacettes.indexOf(props.category.targetPage) != -1).length > 0
});
const isCurrent = computed(() => {
  return store.currentPage != null && store.currentPage.id == props.category.targetPage
})
</script>