<template>
      <span><Icon role="button" class="align-middle ms-1 assignment-button" name="ion:code-slash-sharp" v-on:click="props.clickHandler"></Icon></span>

</template>
<script setup lang="ts">
interface AssignmentButtonProps {
  clickHandler: () => {};
}
const props = defineProps<AssignmentButtonProps>();

</script>

<style lang="scss" scoped>
@import "../../../style/variables.scss";

.assignment-button {
  font-size: small;
  color: $secondary;
}
</style>