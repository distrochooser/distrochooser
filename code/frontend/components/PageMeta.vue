<template>
    <div v-if="store.session">
        <Title>
            {{ store.session.name }}
        </Title>
        <Meta v-for="(key, value) in store.session.meta" :key="key" :name="key" :content="value"/>
    </div>
</template>
<script setup lang="ts">

import { useSessionStore } from "../states/session";
const store = useSessionStore();
</script>