<template>
    <ClientOnly>
        <div class="main container mt-3">
            <h1>
                <span class="badge text-bg-danger align-middle me-1">
                    {{ store.hardSessionFail.response.status }}
                </span> Stop.
            </h1>
            <p>
            </p>
            <p>
                We are sorry, but whe can not continue your request. A reason was given:
            </p>
            <pre class="text-wrap">
                {{ text }}
            </pre>
        </div>
    </ClientOnly>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useSessionStore } from '../states/session';
const text = ref("")
onMounted(() => {
    store.hardSessionFail.response.text().then((value) => text.value = value)
})
const store = useSessionStore()
</script>