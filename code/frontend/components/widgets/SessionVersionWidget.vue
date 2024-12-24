<template>
    <div>
        {{  selection  }}
        <select v-model="selection" >
          <option :value="null">bla</option>
          <option :value="version.id" v-for="version, index in props.widget.versions" :key="index">
            {{  version.text }}
          </option>
        </select>
    </div>
</template>
<script setup lang="ts">
import type { SessionVersionWidget } from '~/sdk';
import { useSessionStore } from '../../states/session';

// FIXME: The widget looses the availableWidgets for some reasons
interface WidgetProps {
  widget: SessionVersionWidget;
}

const props = defineProps<WidgetProps>();
const selection = ref(null)
const store = useSessionStore();
watch(selection, value => {
     store.updateSession(selection.value)
}, {deep: true, immediate: true})

</script>