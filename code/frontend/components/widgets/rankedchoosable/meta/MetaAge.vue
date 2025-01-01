<template>
    <span>
    {{ diff }}
    </span>

</template>


<script lang="ts" setup>

interface AgeProps {
  start: string;
}

const props = defineProps<AgeProps>();
const now = Date.now();
const diff = Math.floor((now - Date.parse(props.start)) / 1000 / 60 / 60 / 24 / 365)
</script>