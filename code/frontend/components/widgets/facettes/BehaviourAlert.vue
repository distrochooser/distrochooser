<!--
distrochooser
Copyright (C) 2014-2026 Christoph Müller <distrochooser@chmr.eu>

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
    <Icon :title="tooltipText" class="fs-5 align-middle ms-1 me-1 weight-ribbon behaviour-alert"
        name="ion:alert-circle-sharp" v-on:click="expanded = !expanded"></Icon>
    <div v-for="(behaviour, key) in behaviours" :key="key" class="mb-2 mt-2" v-if="expanded">
        <div class="card">
            <div class="card-header">
                 {{  tooltipText }}
            </div>
            <ul class="list-group list-group-flush">
                <li class="list-group-item" v-for="(subject, subject_key) in onlySelectedFacettes(behaviour.affectedSubjects)"
                    :key="subject_key">
                    <LanguageTranslation :translation-key="subject.description" />
                </li>
                <li class="list-group-item text-center">
                    <Icon :title="tooltipText" class="fs-5 align-middle ms-1 me-1 behaviour-alert"
                        name="ion:alert-circle-sharp"></Icon> 
                </li>

                <li class="list-group-item" v-for="(object, object_key) in onlySelectedFacettes(behaviour.affectedObjects)"
                    :key="object_key">
                    
                    <LanguageTranslation :translation-key="object.description"  />
                </li>
            </ul>
        </div>
    </div>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { useSessionStore } from '../../../states/session';
import type { Facette, FacetteBehaviour, Nested } from '../../../sdk';
import LanguageTranslation from '../../LanguageTranslation.vue';


interface BehaviourAlertProps {
    behaviours: FacetteBehaviour[];
}

const expanded = ref(false);

const props = defineProps<BehaviourAlertProps>();

const sessionStore = useSessionStore();
const tooltipText = computed(() => sessionStore.__i("conflicting_answer"))

const onlySelectedFacettes = (facettes: Nested[]) => facettes.filter(f => sessionStore.facetteSelections.filter(s => s.facette == f.id).length > 0) 
</script>


<style lang="scss" scoped>
.behaviour-alert {
    color: darkred;
    animation: blink 5s infinite;
    cursor: pointer;    
}
</style>