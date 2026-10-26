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
        <div :class="'col text-center alert ' + (ispreviousVersionUrlConfigured ? 'alert-info' : 'alert-danger')"
            v-if="isOldResultId">
            <div v-if="ispreviousVersionUrlConfigured && wasMigrated">
                <LanguageTranslation translation-key="old-version-migrated-fallback-alert" />
                <br />
                <LanguageTranslation translation-key="old-version-alert" />:
                <a target=" _blank" :href="oldVersionLink">{{ oldVersionLink }}</a>
            </div>
            <div v-else-if="ispreviousVersionUrlConfigured && !wasMigrated">
                <LanguageTranslation translation-key="old-version-alert" />:
                <a target="_blank" :href="oldVersionLink">{{ oldVersionLink }}</a>
            </div>
            <div v-else>
                <LanguageTranslation translation-key="old-version-not-found-alert" />
            </div>
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
const isOldResultId = computed(() => resultId.startsWith("d5")) /* Everything NOT prefixed with "d6" is considered old */
const wasMigrated = computed(() => sessionStore.session && sessionStore.session.importedFromSession) /* Everything NOT prefixed with "d6" is considered old */
const ispreviousVersionUrlConfigured = computed(() => sessionStore.session && sessionStore.session.previousVersionUrl) /* The backend can be configured to point to the "old" instance. If no instance is given, the error message will change */
const oldVersionLink = computed(() => sessionStore.session.previousVersionUrl ? sessionStore.session.previousVersionUrl + "/" + sessionStore.session.languageCode + "/" + resultId : null)
</script>