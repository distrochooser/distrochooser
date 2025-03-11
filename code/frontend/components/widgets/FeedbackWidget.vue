<template>
    <div class="row">
        <div class="col-12 col-sm-12">
            <div class="row mb-2">
                <div class="col">
                    <div class="card">
                        <div class="card-header">
                            <LanguageTranslation translation-key="GIVE_YOUR_FEEDBACK" />

                            <span class="ms-2 badge  rounded-pill text-bg-success text-light" v-if="store.givenFeedback !== null && store.givenFeedback !== ''">
                                <LanguageTranslation translation-key="THANK_YOU_FOR_YOUR_FEEDBACK" />
                            </span>
                        </div>
                        <ul class="list-group list-group-flush mt-2">
                            <li class="list-group-item">

                                <div class="mb-3">
                                    <textarea class="form-control"  rows="5" v-model="givenFeedback" @change="updateFeedback"></textarea>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import type { FeedbackWidget } from '../../sdk';
import { useSessionStore } from '../../states/session';

const store = useSessionStore();
const givenFeedback = ref(store.givenFeedback)
interface WidgetProps {
    widget: FeedbackWidget;
}
const props = defineProps<WidgetProps>();
const updateFeedback = () => {
    store.givenFeedback = givenFeedback.value
    store.updateGivenFeedback()
}
</script>