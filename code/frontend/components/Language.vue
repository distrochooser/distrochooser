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
    <div>
        <div v-if="store.session" class="mt-2">
            <select v-model="selectedLanguage">
                <option
                v-for="(key, value, index) in Object.entries(store.session.languageCodes)" :key="index" :value="key[1]"> {{ key[0] }}</option>
            </select>
        </div>
    </div>
</template>
<script setup lang="ts">
import { watch } from 'vue';
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