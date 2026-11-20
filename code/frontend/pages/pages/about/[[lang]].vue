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
            <LanguageTranslation translation-key="ABOUT_PAGE_TITLE" />
        </h1>
        <p>
            <LanguageTranslation translation-key="ABOUT_PAGE_TEXT" />
        </p>
        <p>
            <LanguageTranslation translation-key="about_page_text_stats_results" />

            <span class="badge rounded-pill text-bg-light ms-1">
                ~{{ sessionStore.session.testCount }}
            </span>
        </p>
        <p>
            <LanguageTranslation translation-key="about_page_text_stats_visitors" />

            <span class="badge rounded-pill text-bg-light ms-1">
                {{ sessionStore.session.visitorCount }}
            </span>
        </p>
        <h1>
            <LanguageTranslation translation-key="ABOUT_PAGE_LICENSE_TITLE" />
        </h1>
        <p>
            <LanguageTranslation translation-key="ABOUT_PAGE_LICENSE_TEXT" /> <a target="_blank"
                href="https://codeberg.org/distrochooser/distrochooser">Codeberg</a>/ <a target="_blank"
                href="https://github.com/distrochooser/distrochooser">GitHub</a> (
            <LanguageTranslation translation-key="PRIVACY_PAGE_EXTERNAL_LINK" />)
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