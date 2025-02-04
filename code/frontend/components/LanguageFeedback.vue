<template>
    <a href="#" v-on:click="toggleTranslate">
        <span>
            <Icon name="ion:language" :class="{'text-success fw-bold': sessionStore.isTranslating }"></Icon>
            <LanguageTranslation class="ms-3" translation-key="help-translation"/>
        </span>
    </a>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';
import LanguageTranslation from './LanguageTranslation.vue';
const sessionStore = useSessionStore();
const toggleTranslate = () => sessionStore.toggleTranslateFeedback()
</script>
<style lang="scss" scoped>

</style>