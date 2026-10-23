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
    <div class="side-navigation">
        <div v-for="(page, index) in pages" v-bind:key="index" class="mt-2 fs-5 d-block  side-navigation-item"
            :class="{ 'fw-bold': currentPage != null && page.id == currentPage.id, 'is-last-item': isLastPage(page), 'with-facette-selections': hasFacetteSelections }">
            <NavigationItem :index="index" :page="page" v-on:click="sessionStore.selectPage(page.id)" />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { useSessionStore } from '../states/session';
import type { Page } from '../sdk';


let sessionStore = useSessionStore();
const pages = computed(() => sessionStore.pages);
const currentPage = computed(() => sessionStore.currentPage == null ? null : sessionStore.currentPage)

const isLastPage = (page: Page) => {
    return sessionStore.pages.indexOf(page) === sessionStore.pages.length - 1
}

const hasFacetteSelections = computed(() => sessionStore.facetteSelections.length > 0)
</script>

<style lang="scss">
@import "../style/variables.scss";

.side-navigation {
    width: fit-content;

    .side-navigation-item {
        cursor: pointer;

        &.is-last-item {
            background-color: white;
            color: black;

            &.with-facette-selections {
                background-color: $primary !important;
                color: white;
            }

            margin-left: -1em;
            padding-top: 0.5em;
            padding-left: 1em;
            padding-bottom: 0.5em;
        }
    }
}
</style>