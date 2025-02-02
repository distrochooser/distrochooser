<!--
kuusi
Copyright (C) 2014-2025 Christoph Müller  <mail@chmr.eu>

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
  <div>
    <form>
        <div class="mb-3">
          <label for="edition" class="form-label">Questionaire edition</label>
          <select v-model="selection" class="form-select" id="edition">
            <option :value="null">Full</option>
            <option :value="version.id" v-for="version, index in props.widget.versions" :key="index">
              {{ version.text }}
            </option>
          </select>
        </div>
    </form>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import type { SessionVersionWidget } from '../../sdk';
import { useSessionStore } from '../../states/session';

// FIXME: The widget looses the availableWidgets for some reasons
interface WidgetProps {
  widget: SessionVersionWidget;
}

const props = defineProps<WidgetProps>();
const selection = ref(null)
const store = useSessionStore();
watch(selection, value => {
  if (store.session) {
    store.updateSession(selection.value)
  }
}, { deep: true, immediate: true })

</script>