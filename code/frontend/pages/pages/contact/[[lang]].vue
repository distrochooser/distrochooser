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
    <div>
        <h1>
            <LanguageTranslation translation-key="IMPRINT_TITLE" />
        </h1>
        <pre>
                    {{ sessionStore.session.imprintData }}
                </pre>
        <h1>
            <LanguageTranslation translation-key="IMPRINT_DISCLAIMER_TITLE" />
        </h1>
        <p>
            <LanguageTranslation translation-key="IMPRINT_DISCLAIMER_TEXT" />
        </p>
    </div>
</template>
<script setup lang="ts">
import { useSessionStore } from '../../../states/session';

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
</script>