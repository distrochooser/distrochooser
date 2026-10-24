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
        <label class="form-check-label" for="font">
            Font
        </label>
        <div id="font">
            <span v-for="n in 3">
                <button type="button" class="btn btn-outline-primary me-2" :style="'font-size: ' + n + 'rem'"
                    @click="alignFontSize(n)"> {{ n }}x</button>
                <button type="button" class="btn btn-outline-primary me-2" :style="'font-size: ' + (n + 0.5) + 'rem'"
                    @click="alignFontSize(n + 0.5)"> {{ n + 0.5 }}x</button>
            </span>

        </div>
    </div>

</template>

<script setup lang="ts">
import { useSessionStore } from '../../../states/session';

const store = useSessionStore();
const alignFontSize = (size) => {
    store.fontSize = size
    document.body.style.setProperty("--bs-body-font-size", `${store.fontSize}rem`)
}
</script>