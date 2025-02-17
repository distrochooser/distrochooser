<template>

    <div class="btn-group mt-3" role="group">
        <span class="btn btn-outline-primary" :style="'border-color: ' +
            choosable.bgColor +
            '; '">
          <LanguageTranslation :translation-key="choosable.displayName"/>

          <Icon name="ion:chatbubbles" v-if="props.isPending"></Icon>
        </span>
        <a href="#"  :class='{
            "btn btn-outline-success": true,
            "btn-success link-light": hasFeedback(props.choosableId, true)
        }' v-on:click.prevent="
            giveFeedback(choosable, true)
            ">
            <Icon name="ion:thumbs-up"></Icon>
            <span v-if="feedbackVotes">({{feedbackVotes[1]  + (hasFeedback(props.choosableId, true) ? 1 : 0)}})</span>
        </a>

        <a href="#"
        :class='{
            "btn btn-outline-danger": true,
            "btn-danger link-light": hasFeedback(props.choosableId, false)
        }'
        v-on:click.prevent="
            giveFeedback(choosable, false)
            ">

            <Icon name="ion:thumbs-down"></Icon>
            <span v-if="feedbackVotes">({{feedbackVotes[2]+ (hasFeedback(props.choosableId, false) ? 1 : 0)}})</span>
        </a>
        <a href="#"  v-if="props.removeDelegate == null && hasAnyFeedback(choosable.id)" class="btn btn-outline-primary" v-on:click.prevent="
            removeFeedback(choosable)
            ">
            <Icon name="ion:arrow-undo"></Icon>
        </a>

        <a href="#" v-if="props.removeDelegate" class="btn btn-outline-primary" v-on:click.prevent="
           () => {
            removeFeedback(choosable)
            props.removeDelegate(choosable)
           }
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
    removeDelegate?: (c: Choosable) => void;
    isPending: boolean;
}
const store = useSessionStore();

const props = defineProps<ChoosableAssignmentProps>();
const giveFeedback = (choosable: Choosable, is_positive: boolean) =>
    store.giveFeedback(props.assignment, choosable, props.facette, is_positive);

const removeFeedback = (choosable: Choosable) =>
    store.removeFeedback(props.assignment, choosable);

const hasAnyFeedback = (choosableId: number) => store.choosableAssignmentFeedback.filter(f => f.assignment == props.assignment.id && f.choosable == choosableId).length != 0;


const hasFeedback = (choosableId: number, positive: boolean) => store.choosableAssignmentFeedback.filter(f => f.assignment == props.assignment.id && f.choosable == choosableId && f.isPositive == positive).length != 0;



const choosable = computed(() => store.choosables.filter((c) => c.id == props.choosableId)[0]);

const feedbackVotes = computed(() => props.assignment.votes.filter(vA => vA[0] == props.choosableId)).value[0] ?? 0

</script>