<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
<template>
  <div>

    <Head>
      <PageMeta />
    </Head>
    <NuxtLoadingIndicator />
    <NuxtRouteAnnouncer />
    <main role="main" :class="{ 'rtl': sessionStore.session && sessionStore.session.isLanguageRtl }">
      <DarkMode />
      <div class="row">
        <div class="col-xl-3">
        </div>
        <div class="col-12 col-xl-6">
          <MainNavigation />
          <LogoContainer />
          <Navigation />
        </div>
      </div>
      <div class="row">
        <div class="col-xl-2" />
        <div class="col-xl-2 d-none d-xl-block ">
          <div class="ms-5 sticky-top">
            <SideNavigation />
          </div>
        </div>
        <div class="col-12 col-xl-4">
          <div class="page position-relative top-40 p-3">
            <RenderField />
          </div>
        </div>
      </div>

    </main>
  </div>
</template>
<script lang="ts" setup>
import { navigateTo } from "nuxt/app";
import { computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useSessionStore } from "../../states/session";
import PageMeta from "../../components/PageMeta.vue";
import MainNavigation from "../../components/MainNavigation.vue";
import Navigation from "../../components/Navigation.vue";
import { EntryPointEnum } from "../../sdk";
import SideNavigation from "../../components/SideNavigation.vue";
import LogoContainer from "../../components/LogoContainer.vue";
import DarkMode from "../../components/DarkMode.vue";

const { start, finish } = useLoadingIndicator()
const router = useRoute();
const lang: string = router.params.lang as string;

const id: string | null = (router.params.resultId as string) ?? null;

const sessionStore = useSessionStore();
onMounted(async () => {
  if (!lang) {
    // TODO: Make this more intelligent
    navigateTo("/en", {
      redirectCode: 301,
      replace: true,
    });
  } else {
    await sessionStore.createSession(lang, EntryPointEnum.Startpage, id);
  }
});

const loading = computed(() => sessionStore.isLoading)

watch(loading, (value) => {
  if (value) {
    start({ force: true })
  } else {
    finish({ force: true })
  }
})
</script>
<style lang="scss" scoped>
@import "../../style/variables.scss";

.rtl {
  direction: rtl;
}


body[data-bs-theme='dark'] {
  .page {
    background-color: $page-bg-dark;
  }
}

body[data-bs-theme='light'] {

  .page {
    background-color: #ffffff;
    padding: 1em;
    color: black;
  }
}
</style>