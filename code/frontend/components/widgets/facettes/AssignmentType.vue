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

    <span
        :class="{ 'badge  rounded-pill me-3 ': true, 'less-weight-badge': assignment.weight < 0, 'more-weight-badge': assignment.weight > 0 }"
        v-if="props.displayWeigth && props.assignment.weight != null && weightText != null" :title="assignment.weight.toString() + 'x'">

        <Icon name="ion:trending-up-outline" class="me-1" v-if="props.assignment.weight > 0"></Icon>
        <Icon name="ion:trending-down-outline" class="me-1" v-if="props.assignment.weight < 0"></Icon>

        <LanguageTranslation :translation-key="weightText" />
    </span>
    <span :class="'badge  rounded-pill ' + assignmentTypeCssMap[assignment.assignmentType]
        ">
        <LanguageTranslation :translation-key="assignment.assignmentType" />
    </span>
</template>
<script setup lang="ts">
import type { FacetteAssignment } from '../../../sdk';


interface AssignmentTypeProps {
    assignment: FacetteAssignment;
    displayWeigth: boolean;
}


const assignmentTypeCssMap = {
  BLOCKING: "text-bg-dark",
  NEGATIVE: "text-bg-danger ",
  POSITIVE: "text-bg-success text-light",
  NEUTRAL: "text-bg-light",
};

const props = defineProps<AssignmentTypeProps>();
const weightText = props.assignment.weight < 1 ? "weight-less" :  (props.assignment.weight > 1 ? "weight_more" : null);

</script>

<style lang="scss" scoped>
@import "../../../style/variables.scss";
.less-weight-badge {
   background-color: $weightLessColor;
   color: $weightBadgeFontColor;
}
.more-weight-badge {
  background-color: $weightMoreColor;
  color: $weightBadgeFontColor;
}

</style>