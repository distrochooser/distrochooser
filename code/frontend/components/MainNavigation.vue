<template>
    <div class="row">
        <div class="col text-center mt-2">
          <div class="btn-group" role="group" aria-label="Navigation" v-if="sessionStore.session">
            <NuxtLink type="button" :to="'/pages/about/'+sessionStore.session.languageCode" class="btn btn btn-outline-primary">
                <LanguageTranslation translation-key="ABOUT" /> 
            </NuxtLink>
            <NuxtLink type="button" :to="'/pages/contact/'+sessionStore.session.languageCode" class="btn btn btn-outline-primary">
                <LanguageTranslation translation-key="CONTACT" /> 
            </NuxtLink>

            <div class="btn-group" role="group">
              <button type="button" class="btn btn-outline-primary dropdown-toggle" data-bs-toggle="dropdown"
                aria-expanded="false">
                <LanguageTranslation translation-key="LANGUAGE" /> 
              </button>
              <Language v-if="sessionStore.session" />
            </div>
          </div>
        </div>
      </div>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';


const sessionStore = useSessionStore();
</script>