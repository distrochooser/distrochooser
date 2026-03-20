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

    <Head>
        <PageMeta />
    </Head>
    <NuxtRouteAnnouncer />
    <main role="main" class="container">
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
                    <LanguageTranslation translation-key="exit-link" />
                </h1>
                <p>
                    <a :href="decodedUrl" class="btn btn-danger" @click="handleClick">
                        <LanguageTranslation translation-key="exit-link-text" />: {{ decodedUrl }}
                    </a>
                </p>
            </div>
        </div>
    </main>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useSessionStore } from '../../../../../states/session';


const sessionStore = useSessionStore();

const router = useRoute();
const lang: string = router.params.lang as string;
const url: string = router.params.url as string;
const id: string = router.params.id as string;
console.log(id)
onMounted(async () => {
    if (sessionStore.session == null) {
        await sessionStore.createSession(lang);
    }
});

const basePath = useRuntimeConfig().public.basePath
const decodedUrl = computed(() => decodeURI(atob(url)))
const handleClick = async (e: MouseEvent) => {
    e.preventDefault();
    if (id === "") {
        window.open(decodedUrl.value, "_blank")
    } else {
        const target = basePath + "/out/" + id.toString() + "/WEBSITE/"
        console.log(target)
        await fetch(target)
    }
}
</script>