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
    <div class="row mt-2 mb-2 g-0">
        <div class="col g-0 text-center alert alert-success alert-dismissible" v-if="browserLanguageAvailable">
            <a href="#" v-on:click="sessionStore.changeLanguage(browserLanguage)">This questionnaire is also available
                in your
                language!</a>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { useSessionStore } from '../states/session';


let sessionStore = useSessionStore();
const browserLanguage = computed(() => navigator.language)
const browserLanguageAvailable = computed(() => sessionStore.session != null && Object.keys(sessionStore.session.languageCodes).indexOf(navigator.language) != -1 && !sessionStore.languageHintDismissed && sessionStore.session.languageCode != navigator.language && sessionStore.session.languageCode == sessionStore.session.defaultLanguage && sessionStore.isOnFirstPage())

</script>