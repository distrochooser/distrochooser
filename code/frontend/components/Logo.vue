<!--
distrochooser
Copyright (C) 2014-2025 Christoph Müller  <mail@chmr.eu>

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
    <NuxtLink v-if="store.session && router.path.startsWith('/pages')" :to="'/' + store.session.languageCode">
        <img v-if="store.session" class="mt-2 d-none d-sm-block" :src="store.session.logo" />
    </NuxtLink>
    <a v-else-if="store.session && !router.path.startsWith('/pages')" href="#" v-on:click="store.selectPage(-1)">
        <img v-if="store.session" class="mt-2 d-none d-sm-block" :src="store.session.logo" />
    </a>
</template>
<script setup>
import { useSessionStore } from "../states/session";
const store = useSessionStore();
const router = useRoute();
</script>
