<template>
    <a href="#" v-on:click="toggleTranslate">
        <span>
            <Icon name="ion:language" :class="{'text-success fw-bold': sessionStore.isTranslating }"></Icon>
        </span>
    </a>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';
const sessionStore = useSessionStore();
const toggleTranslate = () => sessionStore.toggleTranslate()
</script>
<style lang="scss" scoped>

</style>