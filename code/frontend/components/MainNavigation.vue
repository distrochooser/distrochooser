<template>
  <div class="row">
    <div class="col-3 d-none d-sm-block"></div>
    <div class="col-xl-7 col-sm-12 text-center mt-2">
      <div class="btn-group mt-2" role="group" aria-label="Navigation" v-if="sessionStore.session">
        <div class="btn mt-2 d-block d-sm-none">
          <img class=" mobile-icon" :src="sessionStore.session.icon"/>
        </div>
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/about/' + sessionStore.session.languageCode : null"
          class="btn btn btn-outline-primary">
          <LanguageTranslation translation-key="ABOUT" />
        </NuxtLink>
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/contact/' + sessionStore.session.languageCode : null"
          class="btn btn btn-outline-primary">
          <LanguageTranslation translation-key="CONTACT" />
        </NuxtLink>
        <NuxtLink type="button"
          :to="!sessionStore.isTranslating ? '/pages/privacy/' + sessionStore.session.languageCode : null"
          class="btn btn btn-outline-primary">
          <LanguageTranslation translation-key="PRIVACY" />
        </NuxtLink>

        <div class="btn-group" role="group">
          <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown"
            aria-expanded="false">
            <LanguageTranslation translation-key="LANGUAGE" />
          </button>
          <Language v-if="sessionStore.session" />
        </div>
        <!-- Desktop translate switch -->
        <div class="form-check form-switch mt-2 ms-2 text-center d-none d-sm-block">
          <input class="form-check-input" type="checkbox" role="switch" id="toggle-translation-mode"
              v-model="sessionStore.isTranslating">
            <label class="form-check-label" for="toggle-translation-mode">
              <LanguageTranslation translation-key="IN_TRANSLATION_MODE" />
            </label>
        </div>
      </div>
    </div>
    <!-- Mobile translate switch -->
    <div class="col-xl-12 col-sm-12 d-block d-sm-none">
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
<style lang="scss">
.mobile-icon {
  height: 32px;
}

</style>