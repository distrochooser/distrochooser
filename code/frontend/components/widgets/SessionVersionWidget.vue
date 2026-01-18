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
  <div>
    <form>
      <div class="form-check" v-for="version, index in props.widget.versions" :key="index">
        <input v-model="selection"  :checked='selection == version.id' class="form-check-input" :value="version.id" type="radio" name="flexRadioDefault" :id="'version_' +version.id">
        <label class="form-check-label" :for="'version_' +version.id">
          <LanguageTranslation :translation-key="version.description" />
        </label>
      </div>
    </form>
  </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import type { SessionVersionWidget } from '../../sdk';
import { useSessionStore } from '../../states/session';

// FIXME: The widget looses the availableWidgets for some reasons
interface WidgetProps {
  widget: SessionVersionWidget;
}

const props = defineProps<WidgetProps>();
const store = useSessionStore();
const selection = ref(store.session ? store.session.version : null)

watch(selection, value => {
  if (store.session) {
    store.updateSession(selection.value)
  }
}, { deep: true, immediate: true })

</script>