<template>
  <div>
    <NuxtRouteAnnouncer />
    <main role="main" class="container">
      <div class="text-center">
        <div class="row">
          <div class="col col-2">
            <img class="mt-2" src="https://distrochooser.de/logo.min.svg" />
          </div>
          <div class="col">
            <Categories />
          </div>
          <div class="col col-2">
            <Language v-if="sessionStore.session" />
          </div>
        </div>
      </div>
      <div class="page mt-1">
        <RenderField />
      </div>
    </main>
  </div>
</template>
<script lang="ts" setup>
import { navigateTo } from "nuxt/app";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useSessionStore } from "~/states/session";

const router = useRoute();
const lang: string = router.params.lang as string;
if (lang == "") {
  navigateTo("/en", {
    redirectCode: 301,
    replace: true,
  });
}
const id: string | null = (router.params.resultId as string) ?? null;

const sessionStore = useSessionStore();
onMounted(async () => {
  await sessionStore.createSession(lang, id);
});
</script>