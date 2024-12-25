<template>
    <div>
        <div v-if="store.session">
            <select>
                <option
                v-for="(key, value, index) in Object.entries(store.session.languageCodes)" :key="index" :value="key[1]"> {{ key[0] }}</option>
            </select>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useSessionStore } from '../states/session';


const store = useSessionStore();
</script>