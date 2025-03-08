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
  <div class="row mt-2 mb-2">
    <div class="col row" v-if="currentCategory != null">
      <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
        <div class="col-2   d-none d-sm-block"/>
        <button type="button" class="col-1 btn btn btn-outline-secondary  d-none d-sm-block" v-if="currentCategoryIndex != 0"
          v-on:click="sessionStore.selectPage(categories[currentCategoryIndex - 1].targetPage)">

          <Icon name="ion:caret-back" class="fs-3"></Icon>
        </button>
        <button type="button" class="disabled col-1 btn btn btn-outline-secondary"
          v-if="currentCategoryIndex == 0"></button>

        <div class="btn-group col-xs-12 col-xl-6  dropdown-center" role="group">
          <button type="button" class="btn btn-primary dropdown-toggle fs-5" data-bs-toggle="dropdown"
            aria-expanded="false">
            <Category :index="currentCategoryIndex" :category="currentCategory" />
          </button>
          <ul class="dropdown-menu" v-if="!sessionStore.isTranslating">
            <li v-for="(category, index) in categories" v-bind:key="index">
              <a class="dropdown-item"
                :class="{ 'dropdown-item': true, 'fw-bold': category.catalogueId == currentCategory.catalogueId }"
                href="#" v-on:click="sessionStore.selectPage(category.targetPage)">

                <Category :index="index" :category="category" />
              </a>
            </li>
          </ul>
        </div>

        <button type="button" class="col-1 btn btn btn-outline-secondary d-none d-sm-block"
          v-if="currentCategoryIndex < categories.length - 1"
          v-on:click="sessionStore.selectPage(categories[currentCategoryIndex + 1].targetPage)">
          <Icon name="ion:caret-forward"  class="fs-3"></Icon>
        </button>
        <button type="button" class="disabled col-1 btn btn btn-outline-secondary" v-else></button>

        <div class="col-2   d-none d-sm-block"/>
      </div>
    </div>
    
  </div>
  <div class="row alert alert-warning" v-if="sessionStore.session && sessionStore.isTranslating">
    <LanguageTranslation translation-key="translation-mode-description" />
  </div>
</template>
<script lang="ts" setup>
import { computed } from "vue";
import { useSessionStore } from "../states/session";
import CategoryIcon from "./CategoryIcon.vue";

let sessionStore = useSessionStore();

const categories = computed(() => sessionStore.categories);
const currentCategories = computed(() => sessionStore.categories.filter(c => sessionStore.currentPage != null && sessionStore.currentPage.id == c.targetPage))
const currentCategory = computed(() => currentCategories.value.length > 0 ? currentCategories.value[0] : null)
const currentCategoryIndex = computed(() => currentCategory != null ? categories.value.indexOf(currentCategory.value) : -1)
</script>