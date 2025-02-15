<template>
    <div class="row">
        <div class="col-12">
            <select class="form-select" v-model="newChoosable">
                <option :key="index" v-for="(value, index) in missingChoosables" :value="value">
                    <LanguageTranslation :translation-key="value.displayName" />
                </option>
            </select>
        </div>
        <div class="col-4" :key="index" v-for="(value, index) in newChoosables">
            <ChoosableAssignments
                :remove-delegate="(value) => { newChoosables = newChoosables.filter(c => c.id != value.id) }"
                :facette="props.facette" :choosable-id="value.id" :assignment="props.assignment" />
        </div>

    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import type { Choosable, Facette, FacetteAssignment } from '../../../sdk';
import { useState } from 'nuxt/app';
import { useSessionStore } from '../../../states/session';


import ChoosableAssignments from "./ChoosableAssignments.vue";
interface AsssignmentProps {
    assignment: FacetteAssignment;
    facette: Facette;
}

const store = useSessionStore();

const props = defineProps<AsssignmentProps>();

const newChoosables = useState<Choosable[]>("new-choosable-feedback-" + props.assignment.id, () => [])

const missingChoosables = computed(() => store.choosables.filter(
    c => (
        props.assignment.choosables.filter(aC => aC == c.id).length == 0
    )
))

const newChoosable = ref<Choosable>();

watch(newChoosable, value => {
    if (newChoosables.value.filter(c => c.id == value.id).length == 0) {
        newChoosables.value.push(value)
    }
}, { deep: true, immediate: false })

</script>