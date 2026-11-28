<template>
    <form class="mt-3">
        <b class="mb-2 d-block">

            <Icon class="me-1 align-middle" name="ion:list"></Icon>
            <LanguageTranslation translation-key="result_list_filter_config_title" />
        </b>
        <div class="form-check">
            <input :key="store.mustHavePositiveMatch ? 'mustHavePositiveMatch' : ''" class="form-check-input"
                type="checkbox" id="mustHavePositiveMatch" v-model="store.mustHavePositiveMatch"
                :checked="store.mustHavePositiveMatch">
            <label class="form-check-label" for="mustHavePositiveMatch">
                <LanguageTranslation translation-key="must_have_positive_match" />
            </label>
        </div>
    </form>
</template>

<script setup lang="ts">
import { useSessionStore } from '../../states/session';


const store = useSessionStore();
</script>