<template>
    <div>
        RESULT SHARE
        {{  shareUrl }}
    </div>
</template>
<script setup lang="ts">
import type {ResultShareWidget } from '~/sdk';
import { useSessionStore } from '../../states/session';


interface WidgetProps {
  widget: ResultShareWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();
const {resultId, languageCode} = store.session
const shareUrl = computed(() => store.session.baseUrl + "/" + languageCode + "/" + resultId)
</script>