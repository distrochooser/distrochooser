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
  <div class="w-100 text-center mt-2 me-2">
    <span v-if="willBeEmpty" class="badge alert alert-warning me-2">
      <LanguageTranslation translation-key="RESULT_WILL_BE_EMPTY" />
    </span>
  </div>
  <div class="row">
    <div class="col-8 col-md-5">
      <div class="btn text-center" @click="a11yShown = !a11yShown"
        :class="a11yShown ? 'btn-secondary' : 'btn-outline-secondary'">
        <Icon class="align-middle me-1" name="ion:accessibility"></Icon>
        <LanguageTranslation translation-key="A11y" />
      </div>
    </div>
    <div class="col-4 col-md-7 text-end">
      <div class="btn-group me-2" role="group" :title="store.__i(!isMarked ? 'BTN_MARK' : 'BTN_UNMARK')"
        v-if="store.currentPage.canBeMarked">
        <a href="#" class="btn btn-outline-marking" v-on:click="toggleMarking">
          <Icon class="align-middle me-1" :name="isMarked ? 'ion:bookmark' : 'ion:bookmark-outline'"></Icon>
          <span class="d-none d-sm-inline">
            <LanguageTranslation :translation-key="!isMarked ? 'BTN_MARK' : 'BTN_UNMARK'" />
          </span>
        </a>
      </div>
      <div class="btn-group me-2" role="group" :title="store.__i('BTN_PREV_PAGE')" v-if="canGoBack">
        <a class="btn btn-secondary " href="#" v-on:click="goBack">
          <Icon class="align-middle me-1" name="ion:caret-back-circle-sharp"></Icon>
          <span class="d-none d-sm-inline">
            <LanguageTranslation translation-key="BTN_PREV_PAGE" class="" />
          </span>
        </a>
      </div>
      <div class="btn-group" role="group" :title="store.__i('BTN_NEXT_PAGE')" v-if="canGoNext">
        <a href="#" class="btn btn-primary" v-on:click="goNext">
          <span class="d-none d-sm-inline">
            <LanguageTranslation translation-key="BTN_NEXT_PAGE" />
          </span>
          <Icon class="align-middle ms-1" name="ion:chevron-forward-circle"></Icon>
        </a>
      </div>
    </div>

  </div>

  <HTMLA11y v-if="a11yShown" />
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import type { NavigationWidget } from "../../sdk";
import { useSessionStore } from "../../states/session";
import HTMLA11y from "./html/HTMLA11y.vue";

interface WidgetProps {
  widget: NavigationWidget;
}
const a11yShown = ref(false)
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
const willBeEmpty = computed(() => (store.metaValues.length + store.facetteSelections.length) == 0 && typeof store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) + 2] == 'undefined')
const goNext = () => {
  if (!store.isTranslating) {
    store.selectPage(
      store.pages[store.pages.findIndex((p) => p.id == store.currentPage.id) + 1]
        .id
    );
  }
}

const toggleMarking = async () => {
  if (!store.isTranslating) {
    store.toggleMarking()
  }
}

const isMarked = computed(() => {
  return store.pageMarkings.filter(l => l.page == store.currentPage.id).length > 0;
})
</script>
<style lang="scss" scoped>
@import "../../style/variables.scss";

.btn-outline-marking {
  border-color: $orange;
}
</style>