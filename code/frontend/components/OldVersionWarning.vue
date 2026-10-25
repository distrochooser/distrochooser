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
    <div class="row">
        <div class="col text-center alert alert-danger" v-if="isOldResultId && isImportedResultPresent">
            <LanguageTranslation translation-key="old-version-alert" />:
            <a target="_blank" :href="oldVersionLink">{{ isImportedResultPresent }}</a>
        </div>

        <div class="col text-center alert alert-danger" v-if="isOldResultId && !isImportedResultPresent">
            <LanguageTranslation translation-key="old-version-not-found-alert" />
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useSessionStore } from '../states/session';
import { useRoute } from 'vue-router';

const sessionStore = useSessionStore()

const router = useRoute();
const resultId: string | null = (router.params.resultId as string) ?? null;
const isOldResultId = computed(() => !resultId.startsWith("d6")) /* General: Was a result requested? */
const isImportedResultPresent = computed(() => sessionStore.previousVersionResultId !== null) /* Is an actual old result in db? */
const oldVersionLink = computed(() => isImportedResultPresent.value ? sessionStore.session.previousVersionUrl + "/" + sessionStore.session.languageCode + "/" + sessionStore.previousVersionResultId : null)
</script>