<template>
    <div>
        RESULT SHARE
    </div>
</template>
<script setup lang="ts">
import type {ResultShareWidget } from '~/sdk';


interface WidgetProps {
  widget: ResultShareWidget;
}

const props = defineProps<WidgetProps>();

</script>