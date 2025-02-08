<template>
<div>
    <div class="row" v-for="(row, row_key) in props.widget.structure" :key="row_key">
        <div class="col" v-for="(cell, col_key) in row" :key="col_key">
            {{ cell }}
            <input :id="cell.split('.')[1]" type="" v-on:change="updateValue"/>
        </div>
    </div>
</div>
</template>
<script setup lang="ts">
import type { MetaFilterWidget } from '../../sdk';
import { useSessionStore } from '../../states/session';


interface WidgetProps {
  widget: MetaFilterWidget;
}

const store = useSessionStore();

const updateValue = (e: Event) => {
    const el = (e.target as HTMLInputElement)
    let value = el.value
    const key = el.getAttribute("id")
    if ((value.length) == 0) {
        value = null;
    }
    store.updateMetaFilterArgs(key, value)
}

const props = defineProps<WidgetProps>();
</script>