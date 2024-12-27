<template>
    <div>
        {{  metaKey }}: {{metaValue}}
    </div>
</template>
<script setup lang="ts">

interface WidgetProps {
  metaKey: String;
  metaValue: String
}

const props = defineProps<WidgetProps>();
</script>