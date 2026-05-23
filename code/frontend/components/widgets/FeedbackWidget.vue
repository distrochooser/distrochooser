<template>
    <div class="row">
        <div class="col-12 col-sm-12">
            <div class="row mb-2">
                <div class="col">
                    <div class="card">
                        <div class="card-header">
                            <LanguageTranslation translation-key="GIVE_YOUR_FEEDBACK" />
                        </div>
                        <form class="card-body">
                            <div class="mb-3">
                                <label for="feedbacktext" class="form-label">
                                    <LanguageTranslation translation-key="give_your_feedback" />
                                </label>
                                <textarea class="form-control" rows="5" id="feedbacktext" v-model="givenFeedback"
                                    v-on:change="store.resetGivenFeedbackInStore()" v-on:keypress="store.resetGivenFeedbackInStore()"></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary" v-on:click.prevent="updateFeedback" :disabled="givenFeedbackThere">
                                <LanguageTranslation translation-key="SAVE_FEEDBACK" />
                            </button>
                            <span class="ms-2 badge  rounded-pill text-bg-success text-light"
                                v-if="givenFeedbackThere">

                                <Icon name="ion:ios-save" class="align-bottom me-1"></Icon>
                                <LanguageTranslation translation-key="THANK_YOU_FOR_YOUR_FEEDBACK" />
                            </span>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import type { FeedbackWidget } from '../../sdk';
import { useSessionStore } from '../../states/session';

const store = useSessionStore();
const givenFeedback = ref(store.givenFeedback)
const givenFeedbackThere = computed(() => store.givenFeedback !== null && store.givenFeedback !== '')
interface WidgetProps {
    widget: FeedbackWidget;
}
const props = defineProps<WidgetProps>();
const updateFeedback = () => {
    store.givenFeedback = givenFeedback.value
    store.updateGivenFeedback()
}
</script>
