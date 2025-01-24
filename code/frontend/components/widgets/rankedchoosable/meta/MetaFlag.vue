<template>
    <span :class="'fi fi-'  + props.code"/>
</template>


<script lang="ts" setup>

interface FlagProps {
  code: string;
}

const props = defineProps<FlagProps>();
</script>