<template>

    <div class="mb-3">
        <label :for="props.cellString.split('.')[1]" class="form-label">
            <LanguageTranslation :translation-key="props.cellString.split('.')[1]" />
        </label>
        {{ cellString }}

        <input v-if="['radio', 'checkbox'].indexOf(props.cellString.split('.')[0]) == -1" :value="formValue"
            class="form-control" :type="props.cellString.split('.')[0]" :id="props.cellString.split('.')[1]"
            v-on:change="updateValue($event)" />

        <input v-else 
           :type="props.cellString.split('.')[0]" :id="props.cellString.split('.')[1]"
            v-on:change="updateValue($event)" :checked="formValue.length > 0" />
    </div>
</template>
<script lang="ts" setup>
import { useState } from 'nuxt/app';
import { useSessionStore } from '../../../states/session';



interface MetaFilterCellProps {
    cellString: string;
}
const props = defineProps<MetaFilterCellProps>();

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
        store.updateMetaFilterArgs(key, value)
        formValue.value = value
    }
}


</script>