<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <mail@chmr.eu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->
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