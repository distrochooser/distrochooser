<template>
    <div>
        FACETTE RADIO SELECTION
    </div>
</template>
<script setup lang="ts">
import type { FacetteRadioSelectionWidget } from '~/sdk';


interface WidgetProps {
  widget: FacetteRadioSelectionWidget;
}

const props = defineProps<WidgetProps>();

</script>