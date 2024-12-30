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
  <div class="row">
    <div class="col">
      <a v-if="canGoBack" href="#" v-on:click="goBack">{{
        store.__i("BTN_PREV_PAGE")
      }}</a>
    </div>
    <div class="col">
      <a v-if="canGoNext" href="#" v-on:click="goNext">
        {{ store.__i("BTN_SKIP_PAGE") }}
      </a>
    </div>
    <div class="col">
      <a v-if="canGoNext" href="#" v-on:click="goNext">
        {{ store.__i("BTN_NEXT_PAGE") }}
      </a>
    </div>
  </div>
</template>
<script setup lang="ts">
import type { NavigationWidget } from "~/sdk";
import { useSessionStore } from "../../states/session";

interface WidgetProps {
  widget: NavigationWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();
const canGoNext = computed(() => {
  return store.currentPage.nextPage != null;
});
const canGoBack = computed(() => {
  const index = store.pages.findIndex((p) => p.id == store.currentPage.id);
  return index > 0;
});
const goBack = () =>
  store.selectPage(
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) - 1]
      .id
  );
const goNext = () =>
  store.selectPage(
    store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) + 1]
      .id
  );
</script>