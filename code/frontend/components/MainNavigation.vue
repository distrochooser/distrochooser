<template>
  <div  :class="{'a11y-larger-main-menu': sessionStore.fontSizeModifier == 5, 'row': true}">
    <div class="col-3 d-none d-sm-block"></div>
    <div v-if="sessionStore.session" :class="{'col-sm-12 text-center mt-2': true,  'col-xl-6' : !sessionStore.session.isTranslationModeEnabled,  'col-xl-7': sessionStore.session.isTranslationModeEnabled}">
      <div class="btn-group mt-2" role="group" aria-label="Navigation" v-if="sessionStore.session">
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/about/' + sessionStore.session.languageCode : null"
          class="btn">
          <LanguageTranslation translation-key="ABOUT" />
        </NuxtLink>
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/contact/' + sessionStore.session.languageCode : null"
          class="btn">
          <LanguageTranslation translation-key="CONTACT" />
        </NuxtLink>
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/privacy/' + sessionStore.session.languageCode : null"
          class="btn">
          <LanguageTranslation translation-key="PRIVACY" />
        </NuxtLink>

        <div class="btn-group" role="group">
          <button type="button" class="btn dropdown-toggle" data-bs-toggle="dropdown"
            aria-expanded="false">
            <LanguageTranslation translation-key="LANGUAGE" />
          </button>
          <Language v-if="sessionStore.session" />
        </div>
        <!-- Desktop translate switch -->
        <div class="form-check form-switch mt-2 ms-2 text-center d-none d-sm-block" v-if="sessionStore.session.isTranslationModeEnabled">
          <input class="form-check-input" type="checkbox" role="switch" id="toggle-translation-mode"
              v-model="sessionStore.isTranslating">
            <label class="form-check-label" for="toggle-translation-mode">
              <LanguageTranslation translation-key="IN_TRANSLATION_MODE" />
            </label>
        </div>
      </div>
    </div>
    <!-- Mobile translate switch -->
    <div class="col-xl-12 col-sm-12 d-block d-sm-none"  v-if="sessionStore.session.isTranslationModeEnabled">
      <div class="row form-check form-switch mt-3 ms-2 text-center">
        <div class="col-1">
          <input class="form-check-input" type="checkbox" role="switch" id="toggle-translation-mode"
            v-model="sessionStore.isTranslating">
        </div>
        <div class="col-11 text-center">
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
<style lang="scss" scoped>
@import "../style/a11y.scss";
</style>