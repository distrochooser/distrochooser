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
                    <LanguageTranslation translation-key="PRIVACY"/>
                </h1>
                <p v-html="sessionStore.session.privacyData">
                </p>
                <h1>
                    <LanguageTranslation translation-key="VOTER_ID_TITLE"/>
                </h1>
                <p>
                    <LanguageTranslation translation-key="VOTER_ID_TEXT"/>
                    <a href="#" v-if="sessionStore.session && sessionStore.hasVoterId()" class="ms-1 me-1" v-on:click.prevent="sessionStore.removeVoterId"><LanguageTranslation translation-key="VOTER_ID_CLEAR"/></a>
                    <pre class="mt-3" v-if="sessionStore.session && sessionStore.hasVoterId()">{{ sessionStore.getVoterIdKey() }}: {{  sessionStore.getVoterId() }}</pre>
                    <div class="alert alert-info mt-3" v-if="sessionStore.session && !sessionStore.hasVoterId()">
                        <LanguageTranslation translation-key="NO_VOTER_ID"/>
                    </div>
                </p>
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useSessionStore } from '../../../states/session';


const sessionStore = useSessionStore();
const router = useRoute();
const lang: string = router.params.lang as string;
onMounted(async () => {
    if (sessionStore.session == null) {
        await sessionStore.createSession(lang);
    }
});
import { useRobotsRule } from '#imports'

const rule = useRobotsRule()
rule.value = 'noindex, nofollow'
</script>