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
  <div class="row mt-2 mb-2 g-0">
    <div class="col g-0 text-center alert alert-success alert-dismissible" v-if="browserLanguageAvailable">
      <a href="#" v-on:click="sessionStore.changeLanguage(browserLanguage)">This questionnaire is also available in your language!</a>
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  </div>
  <div class="row mt-2 mb-2 g-0">

    <div class="col row g-0 " v-if="currentPage != null">
      <div class="btn-group row col-12 text-center g-0" role="group">
        <div class="col-2   d-none d-xl-block" />
        <button type="button" class="col-1 btn btn btn-outline-secondary d-none d-xl-block" v-if="currentPageIndex != 0"
          v-on:click="sessionStore.selectPage(pages[currentPageIndex - 1].id)">

          <Icon name="ion:caret-back" class="fs-3"></Icon>
        </button>
        <button type="button" class="disabled col-1 btn btn d-none d-xl-block btn-outline-secondary"
          v-if="currentPageIndex == 0"></button>

        <div class="btn-group col-xs-12 col-xl-6  dropdown-center" role="group">
          <button type="button" class="btn btn-primary dropdown-toggle fs-5" data-bs-toggle="dropdown"
            aria-expanded="false">
            <NavigationItem :index="currentPageIndex" :page="currentPage" />
          </button>
          <ul class="dropdown-menu" v-show="!sessionStore.isTranslating">
            <li v-for="(page, index) in pages" v-bind:key="index">
              <a class="dropdown-item"
                :class="{ 'dropdown-item': true, 'fw-bold': currentPage != null && page.id == currentPage.id }" href="#"
                v-on:click="sessionStore.selectPage(page.id)">

                <NavigationItem :index="index" :page="page" />
              </a>
            </li>
          </ul>
        </div>

        <button type="button" class="col-1 btn btn btn-outline-secondary d-none d-xl-block"
          v-if="currentPageIndex < pages.length - 1"
          v-on:click="sessionStore.selectPage(pages[currentPageIndex + 1].id)">
          <Icon name="ion:caret-forward" class="fs-3"></Icon>
        </button>
        <button type="button" class="disabled col-1 d-none d-sm-block b btn btn btn-outline-secondary" v-else></button>

        <div class="col-2   d-none d-xl-block" />
      </div>
    </div>

  </div>
  <div class="row alert alert-warning text-start" v-if="sessionStore.session && sessionStore.isTranslating">
    <div class="row">
      <div class="col-1 text-center">

        <Icon name="ion:chatbubbles" class="fs-1"></Icon>
      </div>
      <div class="col-11">
        <b class="me-1">
          <LanguageTranslation translation-key="translation-mode-description-title" />
        </b>
        <LanguageTranslation translation-key="translation-mode-description" />
        <span class="ms-1">
          <LanguageTranslation translation-key="language-vote-privacy" />
        </span>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed } from "vue";
import { useSessionStore } from "../states/session";
import NavigationItem from "./NavigationItem.vue";

let sessionStore = useSessionStore();

const browserLanguage = computed(() => navigator.language)
const browserLanguageAvailable = computed(() => sessionStore.session != null && Object.keys(sessionStore.session.languageCodes).indexOf(navigator.language) != -1 && !sessionStore.languageHintDismissed && sessionStore.session.languageCode != navigator.language && sessionStore.session.languageCode == sessionStore.session.defaultLanguage)
const pages = computed(() => sessionStore.pages);
const currentPage = computed(() => sessionStore.currentPage == null ? null : sessionStore.currentPage)
const currentPageIndex = computed(() => currentPage != null ? pages.value.indexOf(currentPage.value) : -1)
</script>