<template>
    <div>
        RESULT LIST
    </div>
</template>
<script setup lang="ts">
import type {ResultListWidget } from '~/sdk';


interface WidgetProps {
  widget: ResultListWidget;
}

const props = defineProps<WidgetProps>();

</script>