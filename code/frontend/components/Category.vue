

<template>
    <div>
      {{  props.category.catalogueId }}
      {{  props.category.name }}
      {{  props.category.icon }}
    </div>
  </template>
    <script lang="ts" setup>
        import { Category } from '~/sdk/models';

        interface CategoryProps {
            category: Category
        }

        const props = defineProps<CategoryProps>();
  </script>