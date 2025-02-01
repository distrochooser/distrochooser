<template>
      <span :title="props.title" ><Icon role="button" class="align-middle ms-1" name="ion:code-slash-sharp" v-on:click="props.clickHandler"></Icon></span>

</template>
<script setup lang="ts">
interface BehaviourButtonProps {
  clickHandler: () => {};
  title: string;
}
const props = defineProps<BehaviourButtonProps>();

</script>