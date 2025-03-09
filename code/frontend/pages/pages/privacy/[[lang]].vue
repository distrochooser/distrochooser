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