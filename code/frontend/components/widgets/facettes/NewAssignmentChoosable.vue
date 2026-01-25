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
    <div class="row">
        <div class="col-12">
            <select class="form-select" v-model="newChoosable">
                <option value="select"> Select</option>
                <option :key="index" v-for="(value, index) in missingChoosables" :value="value">
                    <LanguageTranslation :translation-key="value.name" />
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