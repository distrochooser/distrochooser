<template>
    <div>
      {{  props.facette.id }}
        <input type="checkbox" v-on:change="registerChange"> {{ props.facette.selectableDescription }}
        WEIGHT:
    </div>
</template>
<script setup lang="ts">
import { useState } from 'nuxt/app';
import { onMounted } from 'vue';
import { SessionApi, type Facette } from '~/sdk';
import { apiConfig, useSessionStore } from '../../../states/session';



interface CheckboxFacetteProps {
  facette: Facette
}

const props = defineProps<CheckboxFacetteProps>();
  const store = useSessionStore();
const selected = useState(() => store.facetteSelections.filter(l => l.facette == props.facette.id).length != 0);


const registerChange = async() => {
  selected.value = !selected.value;
  await store.updateFacetteSelections(props.facette.id, 1, selected.value);
}

</script>