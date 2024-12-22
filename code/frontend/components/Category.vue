

<template>
  <div>
    {{ props.category.catalogueId }}
    {{ props.category.name }}
    {{ props.category.icon }}
    {{ props.category.targetPage }}
    {{  isAnswered }}
    <div
      v-if="props.category.targetPage"
      v-on:click="store.selectPage(props.category.targetPage)"
    >
      test
    </div>
  </div>
</template>
    <script lang="ts" setup>
import type { Facette, FacetteRadioSelectionWidget, FacetteSelection, Page } from "~/sdk";
import { Category } from "~/sdk/models";
import { useSessionStore } from "~/states/session";
import FacetteSelectionWidget from "./widgets/FacetteSelectionWidget.vue";

interface CategoryProps {
  category: Category;
}

const props = defineProps<CategoryProps>();
const store = useSessionStore();

const isAnswered = computed(() => {
  const targetPageId = props.category.targetPage
  const targetPages: Page[] = store.pages.filter(p => p.id == targetPageId)
  if (targetPages.length == 0){
    return false
  }
  const targetPage = targetPages[0]
  const facetteSelections: FacetteSelection[] = store.facetteSelections
  if (!targetPage){
    return false;
  }
  let allFacettesWithinPage: Facette[] = []
  targetPage.widgetList.filter(w => w.widgetType == "FacetteSelectionWidget" || w.widgetType == "FacetteRadioSelectionWidget").forEach((w: (FacetteSelectionWidget | FacetteRadioSelectionWidget)) => {
    allFacettesWithinPage = allFacettesWithinPage.concat(w.facettes)
  });
  console.log(allFacettesWithinPage)
  const facettesWithinPage = facetteSelections.filter(s => allFacettesWithinPage.filter(f => f.id == s.facette).length != 0)
  return facettesWithinPage.length != 0
})
</script>