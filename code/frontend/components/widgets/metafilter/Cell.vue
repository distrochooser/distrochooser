<template>

    <div class="mb-3">

        <div v-if="['radio', 'checkbox'].indexOf(type) == -1">
            <label :for="id" class="form-label">
                <LanguageTranslation :translation-key="id" />
            </label>
            <input  :value="formValue"
            class="form-control" :type="type" :id="id"
            v-on:change="updateValue($event, type)">
        </div>

        <div v-else class="form-check">   
            <label class="form-check-label" :for="id">
                <LanguageTranslation :translation-key="id" />
            </label>
            <input v-on:change="updateValue($event, type)" :checked="formValue.length > 0" class="form-check-input"
                :type="type" :id="id">
         
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useState } from 'nuxt/app';
import { useSessionStore } from '../../../states/session';
import { computed, type ComputedRef } from 'vue';

interface MetaFilterCellProps {
    cellString: string;
}

enum MetaFilterType {
    number = "number",
    radio = "radio",
    checkbox = "checkbox"
}

const props = defineProps<MetaFilterCellProps>();

const type: ComputedRef<MetaFilterType>  = computed<MetaFilterType>(() => MetaFilterType[props.cellString.split('.')[0]])
const id: ComputedRef<string> = computed(() => props.cellString.split('.')[1])
const formValue = useState(props.cellString, () => "")

const getValue = (el: HTMLInputElement, type: MetaFilterType) : string => {
    return type == MetaFilterType.number ? el.value : "" + el.checked;
}
const store = useSessionStore();

const updateValue = (e: Event, type: MetaFilterType) => {
    const el = (e.target as HTMLInputElement)
    let value = getValue(el, type)

    const key = el.getAttribute("id")
    const oldId = store.metaValues.filter(m => m.key == key).map(m => m.id)
    /**
     * In case of checkboxes or radio buttons, in case the value is not true -> remove it from store entirely
     */
    if (type == MetaFilterType.checkbox || type  == MetaFilterType.radio) {
        const boolValue = value == "true";
        if (!boolValue){
            store.removeMetaFilterArg(oldId)
            return
        }
    }

    /** 
     * Fallback for non-checkbox/ radio elements, just update the value, if any. 
     * Otherwise, get rid of it entirely
     */
    if (value.length == 0) {
        console.log(oldId)
        store.removeMetaFilterArg(oldId)
        formValue.value = ""
    } else {
        store.updateMetaFilterArgs(key, value, store.currentPage.id)
        formValue.value = value
    }
}


</script>