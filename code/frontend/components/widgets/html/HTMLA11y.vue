<template>
    <div class="row mb-3">
        <hr>
        <div class="d-none d-sm-block col-xl-3">

        </div>
        <div class="col-xl-6 col-sm-12">
            <h5>
                <LanguageTranslation translation-key="A11y" />
            </h5>
            <div class="form-check mb-3">
                <input class="form-check-input" type="checkbox" value="" id="bwMode" v-model="store.isBWMode">
                <label class="form-check-label" for="bwMode">
                    <LanguageTranslation translation-key="BLACKWHITE_MODE" />
                </label>
            </div>
            <div class="form-check mb-3">
                <input :key="store.isDarkMode ? 'dark-mode-render-trigger' : ''" class="form-check-input"
                    type="checkbox" id="darkMode" v-model="store.isDarkMode" :checked="store.isDarkMode">
                <label class="form-check-label" for="darkMode">
                    Dark Mode
                </label>
            </div>
            <div class="form-check mb-3">
                <input :key="store.mustHaveAssignment ? 'must-have-assignment' : ''" class="form-check-input"
                    type="checkbox" id="mustHaveAssignment" v-model="store.mustHaveAssignment"
                    :checked="store.mustHaveAssignment">
                <label class="form-check-label" for="mustHaveAssignment">
                    <LanguageTranslation translation-key="must_have_assignment" />
                </label>
            </div>
            <select class="form-select" v-model.number="store.fontSizeModifier">
                <option value="1">1x Font</option>
                <option value="5">5x Font</option>
            </select>
        </div>
    </div>

</template>

<script setup lang="ts">
import { useSessionStore } from '../../../states/session';

const store = useSessionStore();
</script>