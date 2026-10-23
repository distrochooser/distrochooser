<template>
    <div class="row mt-2 mb-2 g-0">
        <div class="col g-0 text-center alert alert-success alert-dismissible" v-if="browserLanguageAvailable">
            <a href="#" v-on:click="sessionStore.changeLanguage(browserLanguage)">This questionnaire is also available
                in your
                language!</a>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { useSessionStore } from '../states/session';


let sessionStore = useSessionStore();
const browserLanguage = computed(() => navigator.language)
const browserLanguageAvailable = computed(() => sessionStore.session != null && Object.keys(sessionStore.session.languageCodes).indexOf(navigator.language) != -1 && !sessionStore.languageHintDismissed && sessionStore.session.languageCode != navigator.language && sessionStore.session.languageCode == sessionStore.session.defaultLanguage && sessionStore.isOnFirstPage())

</script>