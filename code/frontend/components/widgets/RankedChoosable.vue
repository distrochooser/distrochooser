<template>
    <div>
        {{ props.choosable.name }}
        <ChoosableMeta v-for="(key, value, index) in props.choosable.meta" :key="index" :metaKey="key" :metaValue="value"/>
    </div>
</template>
<script setup lang="ts">
import type {  RankedChoosable } from '~/sdk';
import ChoosableMeta from './rankedchoosable/ChoosableMeta.vue';
interface WidgetProps {
  choosable: RankedChoosable;
}

const props = defineProps<WidgetProps>();
</script>