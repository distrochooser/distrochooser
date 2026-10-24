<template>
    <div class="mt-3">
        <div class="form-check mb-3">
            <input class="form-check-input" type="checkbox" value="" id="bwMode" v-model="store.isBWMode">
            <label class="form-check-label" for="bwMode">
                <LanguageTranslation translation-key="BLACKWHITE_MODE" />
            </label>
        </div>
        <div class="form-check mb-3">
            <input :key="store.isDarkMode ? 'dark-mode-render-trigger' : ''" class="form-check-input" type="checkbox"
                id="darkMode" v-model="store.isDarkMode" :checked="store.isDarkMode">
            <label class="form-check-label" for="darkMode">
                Dark Mode
            </label>
        </div>
        <label for="font-size" class="form-label">Font: {{ store.fontSize }}x</label>
        <input id="font-size" type="range" min="1" max="5" step="0.1" @change="alignFontSize()" class="form-range"
            v-model="store.fontSize" />
    </div>

</template>

<script setup lang="ts">
import { useSessionStore } from '../../../states/session';

const store = useSessionStore();
const alignFontSize = () => {
    document.body.style.setProperty("--bs-body-font-size", `${store.fontSize}rem`)
}
</script>