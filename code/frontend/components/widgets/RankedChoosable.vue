<template>
    <div>
        {{ props.choosable.name }}
        {{ props.choosable.meta }}
    </div>
</template>
<script setup lang="ts">
import type {  RankedChoosable } from '~/sdk';
interface WidgetProps {
  choosable: RankedChoosable;
}

const props = defineProps<WidgetProps>();
</script>