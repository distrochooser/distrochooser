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
        <div id="" ref="html-banner-content"></div>

    </div>
</template>

<script setup lang="ts">
import { onMounted, useTemplateRef, watch } from 'vue';
import { useSessionStore } from '../../../states/session';

interface HTMLBannerProps {
    catalogueId: string;
}
const props = defineProps<HTMLBannerProps>();
const store = useSessionStore();


const nuxtWelcomeRef = useTemplateRef('html-banner-content')


onMounted(() => {
    if (import.meta.client) {
        const banner = document.createElement("div")
        banner.id = "banner-ad"
        banner.style = "width: 700px; height: 250px"
        nuxtWelcomeRef.value.appendChild(banner)
        const scriptTag = document.createElement("script")
        scriptTag.src = "https://securepubads.g.doubleclick.net/tag/js/gpt.js"
        scriptTag.async = true
        scriptTag.crossOrigin = "anonymous"

        const scriptTag2 = document.createElement("script")
        scriptTag2.innerHTML = `
        window.googletag = window.googletag || { cmd: [] };
        googletag.cmd.push(() => {
            googletag.defineSlot("/6355419/Travel/Europe/France/Paris", [700, 250], "banner-ad").addService(googletag.pubads());
            googletag.enableServices();
        });
        `
        const scriptTag3 = document.createElement("script")
        scriptTag3.innerHTML = `
        googletag.cmd.push(() => {
            googletag.display("banner-ad");
        });
        `
        nuxtWelcomeRef.value.appendChild(scriptTag)

        //nuxtWelcomeRef.value.appendChild(scriptTag2)

        const style = document.createElement("style")
        nuxtWelcomeRef.value.appendChild(style)


        ///nuxtWelcomeRef.value.appendChild(scriptTag3)
    }
})
</script>

<style lang="scss">
.html-banner-child {
    width: 100%;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
}
</style>