

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
import { Category } from "~/sdk/models";
import { useSessionStore } from "~/states/session";

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