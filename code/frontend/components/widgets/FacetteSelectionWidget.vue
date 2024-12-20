<template>
    <div>
        FACETTE SELECTION
    </div>
</template>
<script setup lang="ts">
import type { FacetteSelectionWidget } from '~/sdk';


interface WidgetProps {
  widget: FacetteSelectionWidget;
}

const props = defineProps<WidgetProps>();

</script>