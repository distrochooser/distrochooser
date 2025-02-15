<template>

    <div class="btn-group mt-3" role="group">
        <span class="btn btn-outline-primary" :style="'border-color: ' +
            choosable.bgColor +
            '; '">
          <LanguageTranslation :translation-key="choosable.displayName"/>
        </span>
        <a href="#" :class='{
            "btn btn-outline-primary": true,
            "btn-primary link-light": hasFeedback(props.choosableId, true)
        }' v-on:click.prevent="
            giveFeedback(choosable, true)
            ">
            <Icon name="ion:thumbs-up"></Icon>
        </a>

        <a href="#" 
        :class='{
            "btn btn-outline-primary": true,
            "btn-primary link-light": hasFeedback(props.choosableId, false)
        }'
        v-on:click.prevent="
            giveFeedback(choosable, false)
            ">

            <Icon name="ion:thumbs-down"></Icon>
        </a>
        <a href="#" class="btn btn-outline-primary" v-on:click.prevent="
            removeFeedback(choosable)
            ">
            <Icon name="ion:arrow-undo"></Icon>
        </a>

        <a href="#" v-if="props.removeDelegate" class="btn btn-outline-primary" v-on:click.prevent="
            props.removeDelegate(choosable)
            ">
            <Icon name="ion:remove-circle"></Icon>
        </a>
    </div>

</template>
<script setup lang="ts">
import { computed } from 'vue';
import type { Choosable, Facette, FacetteAssignment } from '../../../sdk';
import { useSessionStore } from '../../../states/session';


interface ChoosableAssignmentProps {
    choosableId: number;
    assignment: FacetteAssignment;
    facette: Facette;
    removeDelegate?: (c: Choosable) => void
}
const store = useSessionStore();

const props = defineProps<ChoosableAssignmentProps>();
const giveFeedback = (choosable: Choosable, is_positive: boolean) =>
    store.giveFeedback(props.assignment, choosable, props.facette, is_positive);

const removeFeedback = (choosable: Choosable) =>
    store.removeFeedback(props.assignment, choosable);

const hasFeedback = (choosableId: number, positive: boolean) => store.assignmentFeedback.filter(f => f.assignment == props.assignment.id && f.choosable == choosableId && f.isPositive == positive).length != 0;



const choosable = computed(() => store.choosables.filter((c) => c.id == props.choosableId)[0]);

</script>