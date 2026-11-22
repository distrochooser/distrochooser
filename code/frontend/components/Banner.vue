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
    <div class="alert alert-info alert-dismissible text-center"
        v-if="sessionStore.session && sessionStore.session.banner">
        <Icon class="icon me-1 align-middle" name="ion:megaphone-sharp"></Icon>
        <span v-for="(part, key) in parts" :key="key">
            <span v-if="part.type == 'text'">
                {{ part.content }}
            </span>
            <a v-else :href="part.content">
                {{ part.content }}
            </a>
        </span>
    </div>
</template>
<script lang="ts" setup>
import { computed } from 'vue';
import { useSessionStore } from '../states/session';


let sessionStore = useSessionStore();
interface BannerPart {
    type: "text" | "link",
    content: string;
}
const parts = computed(() => {
    let result: BannerPart[] = []
    if (!sessionStore.session || !sessionStore.session.banner) {
        return result
    }
    const pattern = /https\:\/\/[^\s]+/gm
    const actualText = sessionStore.__i(sessionStore.session.banner)

    const links = [...actualText.matchAll(pattern)];
    let rawText = actualText
    links.forEach((l) => rawText = rawText.replace(l.toString(), "#"))
    const rawParts = rawText.split("#")
    rawParts.forEach((value) => {
        if (value) {
            const nextLink = links[result.length]
            result.push({
                "type": "text",
                "content": value
            })
            if (nextLink) {
                result.push({
                    "type": "link",
                    "content": nextLink.toString()
                })
            }
        }
    })
    return result
});
</script>