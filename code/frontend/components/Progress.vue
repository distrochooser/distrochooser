<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

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
    <div class="fixed-top">
        <div class="progress" role="progressbar" :aria-valuenow="percent" aria-valuemin="0" aria-valuemax="100"
            style="height: 1vh">
            <div class="progress-bar" :style="'width: ' + percent + '%'"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSessionStore } from '../states/session';


const sessionStore = useSessionStore();
const categories = null // computed(() => sessionStore.categories);
const currentCategory = null //computed(() => sessionStore.categories.filter(c => sessionStore.currentPage != null && sessionStore.currentPage.id == c.targetPage)[0])
const currentCategoryIndex = -1 // computed(() => categories.value.indexOf(currentCategory.value))

const maxIndex = -1 // computed(() => categories.value.length - 1)
const percent = -1 // computed(() => 100 / (maxIndex.value / currentCategoryIndex.value))
</script>