<template>
    <div>
        <div v-if="store.session">
            <select v-model="selectedLanguage">
                <option
                v-for="(key, value, index) in Object.entries(store.session.languageCodes)" :key="index" :value="key[1]"> {{ key[0] }}</option>
            </select>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';


const store = useSessionStore();



const sessionBoundLanguage = computed(() => store.session.languageCode )
const registerChange = (e: Event) => {
    console.log(e.target.value)
}
const selectedLanguage = ref(sessionBoundLanguage.value)


watch(selectedLanguage, value => {
    if (store.session) {
        store.changeLanguage(selectedLanguage.value)
    }
}, {deep: true, immediate: true})
</script>