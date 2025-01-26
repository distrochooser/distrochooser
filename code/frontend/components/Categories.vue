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
    <div class="row mt-2">
      <div class="col" v-if="currentCategory != null">
        <div class="btn-group" role="group" aria-label="Button group with nested dropdown">
          <button type="button" class="btn btn btn-outline-secondary" v-if="currentCategoryIndex != 0"  v-on:click="sessionStore.selectPage(categories[currentCategoryIndex -1].targetPage)">
            {{ currentCategoryIndex }}. 
            {{
              categories[currentCategoryIndex -1].name
            }}
          </button>

          <div class="btn-group" role="group">
            <button type="button" class="btn btn-primary dropdown-toggle fs-5" data-bs-toggle="dropdown"
              aria-expanded="false">
              {{ currentCategoryIndex +1 }}. {{ currentCategory.name }}
            </button>
            <ul class="dropdown-menu">
              <li v-for="(category, index) in categories" v-bind:key="index">
                <a class="dropdown-item" :class="{'dropdown-item': true, 'fw-bold': category.catalogueId ==currentCategory.catalogueId}" href="#" v-on:click="sessionStore.selectPage(category.targetPage)">{{ index +1 }}. {{category.name}}</a>
              </li>
            </ul>
          </div>

          <button type="button" class="btn btn btn-outline-secondary" v-if="currentCategoryIndex < categories.length - 1"  v-on:click="sessionStore.selectPage(categories[currentCategoryIndex +1].targetPage)">
            {{ currentCategoryIndex +2 }}. 
            {{
              categories[currentCategoryIndex + 1].name
            }}
          </button>
        </div>
      </div>
    </div>
</template>
<script lang="ts" setup>
import { computed } from "vue";
import { useSessionStore } from "../states/session";

let sessionStore = useSessionStore();

const categories = computed(() => sessionStore.categories);
const currentCategories = computed(() => sessionStore.categories.filter(c => sessionStore.currentPage != null && sessionStore.currentPage.id == c.targetPage))
const currentCategory = computed(() => currentCategories.value.length > 0 ? currentCategories.value[0] : null)
const currentCategoryIndex = computed(() => currentCategory != null ? categories.value.indexOf(currentCategory.value) : -1)
</script>