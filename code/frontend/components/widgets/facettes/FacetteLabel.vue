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
    <label class="form-check-label me-2" :class="{ 'fw-bold': isSelected }" :for="props.facette.id.toString()"
        @click="handleClick">
        <LanguageTranslation :translation-key="props.facette.description" />
        <Importance v-if="isSelected" :facette="props.facette" />
    </label>
    <BehaviourAlert v-if="behaviours.length > 0" :behaviours="behaviours" />

    <AssignmentButton :click-handler="toggleExpand" v-show="!store.isTranslating"
        v-if="store.session.isFeedbackModeEnabled" />
</template>
<script setup lang="ts">
import { useState } from 'nuxt/app';
import type { Facette, FacetteBehaviour } from '../../../sdk';
import { useSessionStore } from '../../../states/session';
import { computed } from 'vue';
import Importance from "../facettes/Importance.vue"
import BehaviourAlert from "../facettes/BehaviourAlert.vue"
import AssignmentButton from './AssignmentButton.vue';

interface FacetteLabelProps {
    facette: Facette;
    onClick?: () => {}
}

const props = defineProps<FacetteLabelProps>();
const store = useSessionStore()
const isExpanded = useState(
    props.facette.id.toString() + "_expanded",
    () => false
);

const handleClick = () => {
    if (props.onClick) {
        props.onClick()
    }
}

const toggleExpand = async () => {
    isExpanded.value = !isExpanded.value
    if (isExpanded.value) {
        await store.getAssignmentFeedback()
    }
};
const isSelected = computed(
    () =>
        store.facetteSelections.filter((l) => l.facette == props.facette.id)
            .length != 0
);
const behaviours = computed<FacetteBehaviour[]>((b) =>
    store.facetteBehaviours.filter(
        (fb) =>
            fb.affectedObjects.filter((ao) => ao.id == props.facette.id).length > 0 ||
            fb.affectedSubjects.filter((ao) => ao.id == props.facette.id).length > 0
    )
);
</script>