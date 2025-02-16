<template>
    <div class="row">
        <div class="col-12">
            <select class="form-select" v-model="newChoosable">
                <option value="select"> Select</option>
                <option :key="index" v-for="(value, index) in missingChoosables" :value="value">
                    <LanguageTranslation :translation-key="value.displayName" />
                </option>
            </select>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref, watch, type Ref } from 'vue';
import type { Choosable, Facette, FacetteAssignment } from '../../../sdk';
import { useSessionStore } from '../../../states/session';

interface AsssignmentProps {
    assignment: FacetteAssignment;
    facette: Facette;
    newChoosables: Choosable[];
}

const store = useSessionStore();

const props = defineProps<AsssignmentProps>();


const missingChoosables = computed(() => store.choosables.filter(
    c => (
        props.assignment.choosables.filter(aC => aC == c.id).length == 0 &&
        props.newChoosables.filter(aC => aC.id == c.id).length == 0
    )
))

const newChoosable = ref<Choosable>();

watch(newChoosable, value => {
    if (value && props.newChoosables.filter(c => c.id == value.id).length == 0) {
        props.newChoosables.push(value)
        store.giveFeedback(props.assignment, value,  props.facette, true)
    }
}, { deep: true, immediate: false })

</script>