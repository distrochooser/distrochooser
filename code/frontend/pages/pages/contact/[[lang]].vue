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
                    <LanguageTranslation translation-key="IMPRINT_TITLE"/>
                </h1>
                <pre>
                    {{  sessionStore.session.imprintData }}
                </pre>
                <h1>
                    <LanguageTranslation translation-key="IMPRINT_DISCLAIMER_TITLE"/>
                </h1>
                <p>
                    <LanguageTranslation translation-key="IMPRINT_DISCLAIMER_TEXT"/>
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