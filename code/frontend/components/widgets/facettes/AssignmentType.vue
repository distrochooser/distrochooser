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

    <span
        :class="{ 'badge  me-1 ': true, 'less-weight-badge': assignment.weight < 0, 'more-weight-badge': assignment.weight > 0 }"
        v-if="props.displayWeigth && props.assignment.weight != null && weightText != null">

        <Icon :name="props.assignment.weight > 0 ? 'ion:trending-up-outline' : 'ion:trending-down-outline'"
            class="me-1 align-middle"></Icon>

        <span class="align-middle">
            <LanguageTranslation :translation-key="weightText" />
        </span>
    </span>
    <span :class="{ 'badge text-bg-primary bg me-1 ': true }" v-if="hasNegativeHandlingActive">
        <Icon name="ion:stop-circle" class="me-1 align-middle"></Icon>
        <span class="align-middle">
            <LanguageTranslation translation-key="has_negative_handling_active" />
        </span>
    </span>
    <span :class="'badge ' + assignmentTypeCssMap[assignment.assignmentType]">
        <Icon :name="assignmentTypeIconMap[assignment.assignmentType]"
            :class="'me-1 align-middle ' + assignmentTextColor[assignment.assignmentType]"></Icon>
        <span :class="'align-middle ' + assignmentTextColor[assignment.assignmentType]">
            <LanguageTranslation :translation-key="assignment.assignmentType" />
        </span>
    </span>

    <span class="ms-1 badge text-bg-light align-middle ">
        <Icon name=" ion:md-trending-up" class="align-middle" />
        <span class="align-middle">
            {{ store.session.scoreMap[assignment.assignmentType] > 0 ? "+" : "" }}{{
                store.session.scoreMap[assignment.assignmentType] }}P
        </span>
    </span>
</template>
<script setup lang="ts">
import { type AssignmentTypeEnum, type FacetteAssignment } from '../../../sdk';
import { useSessionStore } from '../../../states/session';


interface AssignmentTypeProps {
    assignment: FacetteAssignment;
    displayWeigth: boolean;
    hasNegativeHandlingActive: boolean;
}


const assignmentTypeCssMap = {
    BLOCKING: "text-bg-danger",
    NEGATIVE: "text-bg-danger",
    POSITIVE: "text-bg-success",
    NEUTRAL: "text-bg-light",
};


const assignmentTextColor = {
    BLOCKING: "text-light",
    NEGATIVE: "text-light",
    POSITIVE: "text-light",
    NEUTRAL: "text-dark",
};

const assignmentTypeIconMap: Record<AssignmentTypeEnum, string> = {
    BLOCKING: "ion:alert-circled",
    NEGATIVE: "ion:ios-minus",
    POSITIVE: "ion:ios-plus",
    NEUTRAL: "ion:information-circle-sharp"
}


const props = defineProps<AssignmentTypeProps>();
const weightText = props.assignment.weight < 1 ? "weight-less" : (props.assignment.weight > 1 ? "weight_more" : null);
const store = useSessionStore()
</script>

<style lang="scss" scoped>
@import "../../../style/variables.scss";

.less-weight-badge {
    background-color: $less-weight-color;
    color: $weight-badge-color;
}

.more-weight-badge {
    background-color: $more-weight-color;
    color: $weight-badge-color;
}
</style>