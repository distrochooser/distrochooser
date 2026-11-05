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
    <a class="assignment-source ms-1" v-for="(source, source_key) in sources" :key="source_key"
        :title="getExternalLink(store.session.baseUrl, store.session.languageCode, choosableIdentifier, source, false).toString()"
        target="_blank"
        :href="getExternalLink(store.session.baseUrl, store.session.languageCode, choosableIdentifier, source, true).toString()">[{{
            getExternalLink(store.session.baseUrl, store.session.languageCode, choosableIdentifier, source,
                false).hostname }}]</a>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { getExternalLink } from '../../../util/links';
import { useSessionStore } from '../../../states/session';

interface AssignmentSourceProps {
    rawString: string;
    choosableIdentifier: string;
}

const store = useSessionStore()

const props = defineProps<AssignmentSourceProps>();

const sources = computed(() => {
    const parts = props.rawString.split(",")
    let sources = []
    parts.forEach(part => {
        const linePart = part.split(";")
        const name = linePart[0]
        if (name == props.choosableIdentifier) {
            sources.push(linePart[1])
        }
    })
    return sources
})

</script>