<template>
    <div>
        {{ props.widget }}fasfsa
    </div>
</template>
<script setup lang="ts">
import type { SessionVersionWidget } from '~/sdk';

// FIXME: The widget looses the availableWidgets for some reasons
interface WidgetProps {
  widget: SessionVersionWidget;
}

const props = defineProps<WidgetProps>();
</script>