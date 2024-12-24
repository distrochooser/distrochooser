

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
import { Category } from "~/sdk/models";
import { useSessionStore } from "~/states/session";

interface CategoryProps {
  category: Category;
}

const props = defineProps<CategoryProps>();
const store = useSessionStore();
const isAnswered = computed(() => {
  return store.answeredPages.indexOf(props.category.targetPage) != -1
})

</script>