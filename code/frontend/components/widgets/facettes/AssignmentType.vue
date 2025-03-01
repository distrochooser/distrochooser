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
  NEGATIVE: "text-bg-danger",
  POSITIVE: "text-bg-success",
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