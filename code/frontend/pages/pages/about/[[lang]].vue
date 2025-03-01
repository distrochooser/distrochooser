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
</script>