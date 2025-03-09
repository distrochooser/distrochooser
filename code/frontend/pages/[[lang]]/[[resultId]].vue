<!--
distrochooser
Copyright (C) 2014-2025 Christoph Müller  <mail@chmr.eu>

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
    <NuxtRouteAnnouncer />
    <main role="main" :class="{'container': true, 'rtl': sessionStore.session && sessionStore.session.isLanguageRtl}">
      <MainNavigation/>
      <div class="page mt-3  position-relative top-40">
        <div class="row text-center">
          <div class="col-4 d-none d-sm-block">
          </div>
          <div class="col-xl-3 col-sm-12">
            <Logo />
          </div>
          <div class="col col-1  d-none d-sm-block">
          </div>
        </div>
        <div class="row text-center mb-3">
          <div class="col-12">
            <Categories />
          </div>
        </div>
        <RenderField />
      </div>
    </main>
    <Progress />
    <A11y/>
  </div>
</template>
<script lang="ts" setup>
import { navigateTo } from "nuxt/app";
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useSessionStore } from "../../states/session";
import PageMeta from "../../components/PageMeta.vue";
import Progress from "../../components/Progress.vue";
import MainNavigation from "../../components/MainNavigation.vue";
import A11y from "../../components/A11y.vue";

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
<style lang="scss" scoped>
.rtl {
  direction: rtl;
}
</style>