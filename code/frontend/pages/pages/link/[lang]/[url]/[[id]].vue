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
    <div class="card w-100 border border-warning">
        <div class="card-body">
            <h5 class="card-title">
                <LanguageTranslation translation-key="exit-link" />
            </h5>
            <span class="card-text">
                <LanguageTranslation translation-key="exit-link-description" />
                <span class="mt-2 d-block">
                    <LanguageTranslation translation-key="exit-link-text" />
                    <a :href="decodedUrl" class="ms-1" @click.prevent="handleClick">
                        {{ decodedUrl }}
                    </a>
                </span>
            </span>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useSessionStore } from '../../../../../states/session';
import { EntryPointEnum } from '../../../../../sdk';
import { useRoute } from 'vue-router';

declare module 'nuxt/app' {
    interface NuxtLayouts {
        'custom': unknown
    }
}
// ---cut---
definePageMeta({
    layout: 'page',
})

const sessionStore = useSessionStore()

const router = useRoute();
const lang: string = router.params.lang as string;
const url: string = router.params.url as string;
const id: string = router.params.id as string;
onMounted(async () => {
    if (sessionStore.session == null) {
        // FIXME: This session is _not_ the session the user comes from.
        await sessionStore.createSession(lang, EntryPointEnum.Outgoing);
    }
});


const basePath = useRuntimeConfig().public.basePath
const decodedUrl = computed(() => decodeURI(atob(url)))
const handleClick = async (e: MouseEvent) => {
    e.preventDefault();
    const sessionId = sessionStore.session.id
    if (id) {
        const target = basePath + "/out/" + sessionId.toString() + "/" + id.toString() + "/WEBSITE/"
        await fetch(target)
    }

    window.location.href = decodedUrl.value
}
</script>