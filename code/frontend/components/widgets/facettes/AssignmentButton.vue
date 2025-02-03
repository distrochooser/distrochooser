<template>
      <span><Icon role="button" class="align-middle ms-1" name="ion:code-slash-sharp" v-on:click="props.clickHandler"></Icon></span>

</template>
<script setup lang="ts">
interface AssignmentButtonProps {
  clickHandler: () => {};
}
const props = defineProps<AssignmentButtonProps>();

</script>