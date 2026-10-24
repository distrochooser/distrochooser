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
  <div v-if="store.currentPage" :class="{ 'a11y-larger-larger': store.fontSizeModifier == 5 }">
    <div v-if="store.currentPage.text" class="page-text">
      <LanguageTranslation :translation-key="store.currentPage.text" :key="store.currentPage.text" />
    </div>
    <small v-if="store.currentPage.help && !store.currentPage.hideHelp" :key="store.currentPage.help"
      class="text-body-secondary mt-1 d-block fw-light page-help">
      <LanguageTranslation :translation-key="store.currentPage.help" />
    </small>
    <div class="mt-3">
      <WidgetsWrapper v-for="row in rows" :key="row" class="row" :row="row" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { useSessionStore } from "../states/session";
import LanguageTranslation from "./LanguageTranslation.vue";

const store = useSessionStore();

const rows = computed(() => {
  const min = Math.min(...store.currentWidgets.map(w => w.row))
  const max = Math.max(...store.currentWidgets.map(w => w.row))
  let range = []
  for (var i = min; i <= max; i++) {
    range.push(i)
  }
  return range
})
</script>

<style lang="scss" scoped>
@use 'sass:color';
@import "../style/variables.scss";
@import "../style/a11y.scss";

.page-text {
  font-size: larger;
}

.page-help {
  font-size: large;
}
</style>