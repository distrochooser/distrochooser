<!--
kuusi
Copyright (C) 2014-2024  Christoph Müller  <mail@chmr.eu>

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
    <main role="main" class="container">
      <div class="text-center">
        <div class="row">
          <div class="col col-2">
            <Logo />
          </div>
          <div class="col">
            <Categories />
          </div>
          <div class="col col-1">
            <Language v-if="sessionStore.session" />
          </div>
        </div>
      </div>
      <div class="page mt-3">
        <RenderField />
      </div>
    </main>
  </div>
</template>
<script lang="ts" setup>
import { navigateTo } from "nuxt/app";
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import { useSessionStore } from "../../states/session";
import PageMeta from "../../components/PageMeta.vue";

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