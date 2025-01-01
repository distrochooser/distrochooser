<template>
    <span :class="'fi fi-'  + props.code"/>
</template>


<script lang="ts" setup>

interface FlagProps {
  code: String;
}

const props = defineProps<FlagProps>();
</script>