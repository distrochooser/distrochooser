<template>
    <div>
        <div class="row" v-for="(row, row_key) in props.widget.structure" :key="row_key">
            <div class="col" v-for="(cell, col_key) in row" :key="col_key">
                <Cell :cell-string="cell" :widget="widget"/>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import type { MetaFilterWidget } from '../../sdk';
import Cell from './metafilter/Cell.vue';


interface WidgetProps {
    widget: MetaFilterWidget;
}
const props = defineProps<WidgetProps>();
</script>