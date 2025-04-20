<template>

    <div class="mb-3">

        <div v-if="['radio', 'checkbox'].indexOf(type) == -1">
            <label :for="id" class="form-label">
                <LanguageTranslation :translation-key="id" />
            </label>
            <input  :value="formValue"
            class="form-control" :type="type" :id="id"
            v-on:change="updateValue($event)">
        </div>

        <div v-else class="form-check">   
            <label class="form-check-label" :for="id">
                <LanguageTranslation :translation-key="id" />
            </label>
            <input v-on:change="updateValue($event)" :checked="formValue.length > 0" class="form-check-input"
                :type="type" :id="id">
         
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useState } from 'nuxt/app';
import { useSessionStore } from '../../../states/session';
import { computed } from 'vue';



interface MetaFilterCellProps {
    cellString: string;
}
const props = defineProps<MetaFilterCellProps>();

const type = computed(() => props.cellString.split('.')[0])
const id = computed(() => props.cellString.split('.')[1])

const formValue = useState(props.cellString, () => "")

// TODO: Add checkbox support
const store = useSessionStore();


const updateValue = (e: Event) => {
    const el = (e.target as HTMLInputElement)
    let value = ["radio", "checkbox"].indexOf(el.getAttribute("type")) == -1 ? el.value : "" + el.checked;

    const key = el.getAttribute("id")
    if ((value.length) == 0) {
        const oldId = store.metaValues.filter(m => m.key == key).map(m => m.id)
        console.log(oldId)
        store.removeMetaFilterArg(oldId)
        formValue.value = ""
    } else {
        store.updateMetaFilterArgs(key, value, store.currentPage.id)
        formValue.value = value
    }
}


</script>