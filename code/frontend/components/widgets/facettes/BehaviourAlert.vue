<template>
     <Icon :title="tooltipText" class="fs-5 align-middle ms-1 me-1 weight-ribbon behaviour-alert" name="ion:alert-circle-sharp"></Icon>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useSessionStore } from '../../../states/session';


const sessionStore = useSessionStore();
const tooltipText = computed(() => sessionStore.__i("conflicting_answer"))
</script>


<style lang="scss" scoped>
.behaviour-alert {
    color: darkred;
    animation: blink 5s infinite;
}
</style>