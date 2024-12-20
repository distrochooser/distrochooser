<template>
    <div>
        HTML
    </div>
</template>
<script setup lang="ts">
import type {HTMLWidget } from '~/sdk';


interface WidgetProps {
  widget: HTMLWidget;
}

const props = defineProps<WidgetProps>();

</script>