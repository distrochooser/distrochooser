<template>
  <div class="row">
    <div class="col text-center mt-2">
      <div class="btn-group" role="group" aria-label="Navigation" v-if="sessionStore.session">
        <NuxtLink type="button" :to="!sessionStore.isTranslating ? '/pages/about/' + sessionStore.session.languageCode : null"
          class="btn btn btn-outline-primary">
          <LanguageTranslation translation-key="ABOUT" />
        </NuxtLink>
        <NuxtLink type="button" :to="!sessionStore.isTranslating ?  '/pages/contact/' + sessionStore.session.languageCode : null"
          class="btn btn btn-outline-primary">
          <LanguageTranslation translation-key="CONTACT" />
        </NuxtLink>

        <div class="btn-group" role="group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown"
            aria-expanded="false">
            <LanguageTranslation translation-key="LANGUAGE" />
          </button>
          <Language v-if="sessionStore.session" />
        </div>
        <div class="form-check form-switch mt-2 ms-2">
          <input class="form-check-input" type="checkbox" role="switch" id="toggle-translation-mode"
            v-model="sessionStore.isTranslating">
          <label class="form-check-label" for="toggle-translation-mode">
            <LanguageTranslation translation-key="IN_TRANSLATION_MODE" />
          </label>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';


const sessionStore = useSessionStore();
</script>