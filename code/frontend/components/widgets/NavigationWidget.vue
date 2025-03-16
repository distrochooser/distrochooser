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
  <div :class="{ 'a11y-larger-text': store.fontSizeModifier == 5, 'text-center mt-3 border-top pt-3 ': true }">
    <div class="btn-group" role="group">
      <a v-if="store.currentPage.canBeMarked" href="#" class="btn btn-outline-marking" v-on:click="toggleMarking">
        <LanguageTranslation :translation-key="!isMarked ? 'BTN_MARK' : 'BTN_UNMARK'" />
      </a>
      <a v-if="canGoBack" class="btn btn-secondary" href="#" v-on:click="goBack">
        <LanguageTranslation translation-key="BTN_PREV_PAGE" />
      </a>
      <a v-if="canGoNext" href="#" class="btn btn-primary" v-on:click="goNext">
        <LanguageTranslation translation-key="BTN_NEXT_PAGE" />
      </a>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import type { NavigationWidget } from "../../sdk";
import { useSessionStore } from "../../states/session";
import Language from "../Language.vue";

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
const goBack = () => {
  if (!store.isTranslating) {
    store.selectPage(
      store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) - 1]
        .id
    );
  }
}
const goNext = () => {
  if (!store.isTranslating) {
    store.selectPage(
      store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) + 1]
        .id
    );
  }
}

const toggleMarking = async () => {
  store.toggleMarking()
}

const isMarked = computed(() => {
  return store.pageMarkings.filter(l => l.page == store.currentPage.id).length > 0;
})
</script>
<style lang="scss" scoped>
@import "../../style/variables.scss";
@import "../../style/a11y.scss";

.btn-outline-marking {
  border-color: $orange;
}
</style>