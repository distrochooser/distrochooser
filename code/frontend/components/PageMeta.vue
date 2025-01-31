<template>
    <div v-if="store.session">
        <Title>
            {{ store.session.name }}
        </Title>
        <Meta v-for="(key, value) in store.session.meta" :key="key" :name="key" :content="value"/>
        <link rel="icon" type="image/x-icon" :href="store.session.icon" v-if="store.session.icon" />
    </div>
</template>
<script setup lang="ts">

import { useSessionStore } from "../states/session";
const store = useSessionStore();
</script>