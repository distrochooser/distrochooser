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