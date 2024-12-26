<template>
  <div>
    <NuxtRouteAnnouncer />
    <div class="grid grid-cols-12 gap-3">
      <div class="col-span-2 bg-blue-100">
        <Language v-if="sessionStore.session"/>
        <Categories />
      </div>
      <div class="col-span-10 bg-red-100">
        <RenderField />
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { useSessionStore } from "~/states/session";

const router = useRoute();
const lang: string = (router.params.lang as string);
if (lang == "") {
   navigateTo("/en", {
    redirectCode: 301,
    replace: true
  })
}
const id: string | null = (router.params.id as string) ?? null;

const sessionStore = useSessionStore();
onMounted(async () => {
  await sessionStore.createSession(lang, id);
});
</script>