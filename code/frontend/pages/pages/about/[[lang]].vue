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
    <Head>
        <PageMeta />
    </Head>
    <NuxtRouteAnnouncer />
    <main role="main" class="container" v-if="sessionStore.session !== null">
        <MainNavigation />
        <div class="page mt-3  position-relative top-40">
            <div class="row text-center mb-3">
                <div class="col-4">
                </div>
                <div class="col col-3">
                    <Logo />
                </div>
                <div class="col col-1">
                </div>
            </div>
            <div class="row mb-3">
                <h1>
                    <LanguageTranslation translation-key="ABOUT_PAGE_TITLE"/>
                </h1>
                <p>
                    <LanguageTranslation translation-key="ABOUT_PAGE_TEXT"/>
                </p>
                <p>
                    <LanguageTranslation translation-key="ABOUT_PAGE_TEXT_STATS"/> {{  sessionStore.session.testCount }}
                </p>
                <h1>
                    <LanguageTranslation translation-key="ABOUT_PAGE_LICENSE_TITLE"/>
                </h1>
                <p>
                    <LanguageTranslation translation-key="ABOUT_PAGE_LICENSE_TEXT"/> <a target="_blank" href="https://github.com/distrochooser/distrochooser">GitHub</a> (<LanguageTranslation translation-key="PRIVACY_PAGE_EXTERNAL_LINK"/>)
                </p>
                <h1>
                    <LanguageTranslation translation-key="ABOUT_PAGE_OPENDATA_TITLE"/>
                </h1>
                <p>
                    <LanguageTranslation translation-key="ABOUT_PAGE_OPENDATA_TEXT"/>
                </p>
                <code>
                    GET {{openDataPath }}
                </code>
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useSessionStore } from '../../../states/session';
import { useRuntimeConfig } from 'nuxt/app';


const sessionStore = useSessionStore();
const router = useRoute();
const lang: string = router.params.lang as string;
onMounted(async () => {
    if (sessionStore.session == null) {
        await sessionStore.createSession(lang);
    }
});
const openDataPath = useRuntimeConfig().public.basePath + "/data/1"
</script>